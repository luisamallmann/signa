import { HandLandmarker, FilesetResolver } from
  "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14";

// ---------- configurações (iguais ao treino/teste) ----------
const SEQUENCE_LEN = 30;
const FEATURE_SIZE = 126;
const ESPELHAR = false;        // use o valor que funcionou no test_model.py com a webcam
const LIMIAR = 0.6;            // mais baixo para testar; suba se aparecer palavra errada
const MIN_FRAMES_SINAL = 10;   // menos que isso = ruído (mão passou rápido pela câmera)
const MAX_FRAMES_SINAL = 300;  // corta sinais longos demais (o maior vídeo de treino tem ~310)
const FIM_SEM_MAO_MS = 800;    // mão fora do quadro por esse tempo = fim do sinal (800 evita cortar o sinal se a detecção falhar um instante)
const WASM = "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm";

// ---------- elementos da página ----------
const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const btnIniciar = document.getElementById("btn-iniciar");
const btnReiniciar = document.getElementById("btn-reiniciar");
const placeholderCamera = document.getElementById("camera-placeholder");
const elStatus = document.getElementById("camera-status") || { textContent: "" };
const elVazio = document.getElementById("traducao-vazio");
const elTexto = document.getElementById("traducao-texto");
const rotuloBotao = btnIniciar.querySelector("span");

// ---------- estado ----------
let landmarker = null, stream = null, rodando = false;
let segmento = [], gravando = false, semMaoDesde = null;
const palavras = [];

// Mesma lógica do extrair() do Python: [esquerda(63), direita(63)]
function extrair(resultado) {
  const f = new Array(FEATURE_SIZE).fill(0);
  resultado.landmarks.forEach((mao, i) => {
    const cat = resultado.handedness[i][0];
    const lado = (cat.categoryName || cat.displayName) === "Left" ? 0 : 1;
    mao.forEach((p, j) => {
      const o = lado * 63 + j * 3;
      f[o] = p.x; f[o + 1] = p.y; f[o + 2] = p.z;
    });
  });
  return f;
}

// Mesma lógica do reamostrar() do train_model.py
function reamostrar(seq, n) {
  const out = [];
  for (let i = 0; i < n; i++) {
    out.push(seq[Math.round(i * (seq.length - 1) / (n - 1))]);
  }
  return out;
}

function mostrarTexto() {
  const tem = palavras.length > 0;
  elVazio.hidden = tem;
  elTexto.hidden = !tem;
  elTexto.textContent = palavras.join(" ");
}

function resetarSegmento() {
  segmento = []; gravando = false; semMaoDesde = null;
}

// Chamado quando o sinal termina: manda o trecho inteiro para o modelo
function finalizarSinal() {
  const seq = segmento;
  resetarSegmento();
  if (seq.length < MIN_FRAMES_SINAL) {
    elStatus.textContent = "Faça um sinal.";
    return;
  }
  predizer(seq);
}

async function predizer(seq) {
  elStatus.textContent = "Reconhecendo...";
  try {
    const r = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ frames: reamostrar(seq, SEQUENCE_LEN).map(f => f.map(v => +v.toFixed(5))) }),
    });
    const { label, confidence } = await r.json();
    console.log(`sinal com ${seq.length} frames ->`, label, confidence?.toFixed(2)); // debug

    if (label && confidence >= LIMIAR) {
      elStatus.textContent = `${label} (${(confidence * 100).toFixed(0)}%)`;
      palavras.push(label);
      mostrarTexto();
    } else {
      elStatus.textContent = "Sinal não reconhecido, tente de novo.";
    }
  } catch (e) {
    elStatus.textContent = "Erro ao falar com o servidor.";
  }
}

function loop() {
  if (!rodando) return;
  if (video.readyState >= 2) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.save();
    if (ESPELHAR) { ctx.translate(canvas.width, 0); ctx.scale(-1, 1); }
    ctx.drawImage(video, 0, 0);
    ctx.restore();

    const resultado = landmarker.detect(canvas);
    const temMao = resultado.landmarks.length > 0;
    const agora = performance.now();

    if (temMao) {
      if (!gravando) {               // mão apareceu: começa um sinal novo
        gravando = true;
        segmento = [];
        elStatus.textContent = "Gravando sinal...";
      }
      segmento.push(extrair(resultado));
      semMaoDesde = null;
    } else if (gravando) {           // mão sumiu: espera um pouco antes de encerrar
      semMaoDesde ??= agora;
      if (agora - semMaoDesde >= FIM_SEM_MAO_MS) finalizarSinal();
    }

    if (gravando && segmento.length >= MAX_FRAMES_SINAL) finalizarSinal();
  }
  requestAnimationFrame(loop);
}

async function iniciar() {
  btnIniciar.disabled = true;
  elStatus.textContent = "Carregando modelo...";
  try {
    if (!landmarker) {
      const vision = await FilesetResolver.forVisionTasks(WASM);
      landmarker = await HandLandmarker.createFromOptions(vision, {
        baseOptions: { modelAssetPath: "/static/models/hand_landmarker.task" },
        runningMode: "IMAGE",   // igual ao detector.detect() do Python
        numHands: 2,
      });
    }
    stream = await navigator.mediaDevices.getUserMedia({
      video: { width: { ideal: 1280 }, height: { ideal: 720 } }, audio: false,
    });
    video.srcObject = stream;
    await video.play();
  } catch (e) {
    console.error(e);
    elStatus.textContent = "Não foi possível iniciar a câmera ou o detector.";
    btnIniciar.disabled = false;
    return;
  }

  resetarSegmento();
  placeholderCamera.hidden = true;
  canvas.hidden = false;
  rotuloBotao.textContent = "Parar Tradução";
  btnIniciar.disabled = false;
  elStatus.textContent = "Faça um sinal.";
  rodando = true;
  loop();
}

function parar() {
  rodando = false;
  resetarSegmento();
  stream?.getTracks().forEach(t => t.stop());
  stream = null;
  canvas.hidden = true;
  placeholderCamera.hidden = false;
  rotuloBotao.textContent = "Iniciar Tradução";
  elStatus.textContent = "";
}

btnIniciar.addEventListener("click", () => (rodando ? parar() : iniciar()));

btnReiniciar.addEventListener("click", () => {
  palavras.length = 0;
  resetarSegmento();
  mostrarTexto();
});