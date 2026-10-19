import { HandLandmarker, FilesetResolver } from
  "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14";

// ---------- configurações (iguais ao treino/teste) ----------
const SEQUENCE_LEN = 30;
const FEATURE_SIZE = 126;
const ESPELHAR = false;       // use o valor que funcionou no test_model.py com a webcam
const LIMIAR = 0.8;
const PREDIZER_A_CADA = 3;    // frames entre previsões
const CONFIRMACOES = 2;       // previsões iguais seguidas para aceitar a palavra
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
let landmarker = null, stream = null, rodando = false, ocupado = false;
let buffer = [], contador = 0;
let ultimoLabel = null, repeticoes = 0, ultimaPalavra = null;
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

function mostrarTexto() {
  const tem = palavras.length > 0;
  elVazio.hidden = tem;
  elTexto.hidden = !tem;
  elTexto.textContent = palavras.join(" ");
}

async function predizer() {
  if (ocupado) return;           // não acumula requisições
  ocupado = true;
  try {
    const r = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ frames: buffer.map(f => f.map(v => +v.toFixed(5))) }),
    });
    const { label, confidence } = await r.json();

    if (label && confidence >= LIMIAR) {
      elStatus.textContent = `${label} (${(confidence * 100).toFixed(0)}%)`;
      repeticoes = label === ultimoLabel ? repeticoes + 1 : 1;
      ultimoLabel = label;
      if (repeticoes >= CONFIRMACOES && label !== ultimaPalavra) {
        palavras.push(label);
        ultimaPalavra = label;
        mostrarTexto();
      }
    } else {
      elStatus.textContent = "...";
      ultimoLabel = null; repeticoes = 0;
      ultimaPalavra = null;      // permite repetir a palavra depois de uma pausa
    }
  } catch (e) {
    elStatus.textContent = "Erro ao falar com o servidor.";
  } finally {
    ocupado = false;
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
    buffer.push(extrair(resultado));
    if (buffer.length > SEQUENCE_LEN) buffer.shift();

    if (buffer.length === SEQUENCE_LEN && ++contador % PREDIZER_A_CADA === 0) {
      predizer();
    }
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

  buffer = []; contador = 0; ultimoLabel = null; repeticoes = 0;
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
  ultimaPalavra = null; ultimoLabel = null; repeticoes = 0;
  buffer = [];
  mostrarTexto();
});