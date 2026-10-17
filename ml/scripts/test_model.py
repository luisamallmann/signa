import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # esconde avisos do TensorFlow

import time
from pathlib import Path
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ---------------- configurações ----------------
MODO = "webcam"          # "video" ou "webcam"
CAMERA_INDEX = 0
ESPELHAR = True        # no vídeo deixe False; na webcam teste True e False
LIMIAR = 0.8            # confiança mínima para mostrar o sinal
MIN_FRAMES_COM_MAO = 20 # mínimo de frames com mão detectada na janela
SEQUENCE_LEN = 30
IMPRIMIR_A_CADA = 5     # frames entre cada print do top3

# ---------------- caminhos ----------------
SCRIPT_DIR = Path(__file__).resolve().parent   # ...\signa\ml\scripts
MODELS_DIR = SCRIPT_DIR.parent / "models"      # ...\signa\ml\models

MODEL_PATH = MODELS_DIR / "signa_model.keras"
LABEL_PATH = MODELS_DIR / "label_map.npy"
TASK_PATH = SCRIPT_DIR / "hand_landmarker.task"
VIDEO_PATH = SCRIPT_DIR.parent.parent / "ml" / "data" / "raw" / "AMIGO" / "Amigo_Articulador1.mp4"

caminhos = [MODEL_PATH, LABEL_PATH, TASK_PATH]
if MODO == "video":
    caminhos.append(VIDEO_PATH)
for p in caminhos:
    print(p, "OK" if p.exists() else "NÃO ENCONTRADO")

# ---------------- modelo e labels ----------------
modelo = tf.keras.models.load_model(MODEL_PATH)
label_map = np.load(LABEL_PATH, allow_pickle=True).item()
index_to_label = {v: k for k, v in label_map.items()}
print("Sinais reconhecidos:", label_map)

# ---------------- detector de mãos ----------------
base_options = python.BaseOptions(model_asset_path=str(TASK_PATH))
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)


def extrair(resultado):
    mao_direita = np.zeros(21 * 3)
    mao_esquerda = np.zeros(21 * 3)

    for i, mao in enumerate(resultado.hand_landmarks):
        coords = np.array([[lm.x, lm.y, lm.z] for lm in mao]).flatten()

        # use o mesmo campo do extract_landmarks.py
        categoria = resultado.handedness[i][0]
        label = categoria.category_name or categoria.display_name
        if label == "Left":
            mao_esquerda = coords
        else:
            mao_direita = coords

    return np.concatenate([mao_esquerda, mao_direita])


# ---------------- fonte de vídeo ----------------
if MODO == "video":
    captura = cv2.VideoCapture(str(VIDEO_PATH))
else:
    captura = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)

if not captura.isOpened():
    raise SystemExit("Não consegui abrir a fonte de vídeo.")

print("FPS informado:", captura.get(cv2.CAP_PROP_FPS))

buffer_frames = []
texto = "..."
contador = 0
inicio = time.time()

print("\nPressione 'q' para sair.")

while True:
    ret, frame = captura.read()
    if not ret:
        print("Fim do vídeo / não consegui ler o frame.")
        break

    if ESPELHAR:
        frame = cv2.flip(frame, 1)

    imagem = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
    )
    resultado = detector.detect(imagem)
    buffer_frames.append(extrair(resultado))

    # mantém os últimos 30 frames
    if len(buffer_frames) > SEQUENCE_LEN:
        buffer_frames.pop(0)

    contador += 1
    maos_na_janela = sum(1 for f in buffer_frames if f.any())

    if len(buffer_frames) == SEQUENCE_LEN and maos_na_janela >= MIN_FRAMES_COM_MAO:
        sequencia = np.expand_dims(np.array(buffer_frames), axis=0)
        predicao = modelo(sequencia, training=False).numpy()[0]
        indice = int(np.argmax(predicao))
        confianca = float(predicao[indice])

        if contador % IMPRIMIR_A_CADA == 0:
            top3 = np.argsort(predicao)[-3:][::-1]
            print([(index_to_label[i], f"{predicao[i]:.0%}") for i in top3],
                  "| frames com mão:", maos_na_janela)

        if confianca > LIMIAR:
            texto = f"{index_to_label[indice]} ({confianca * 100:.1f}%)"
        else:
            texto = "..."
    else:
        texto = "..."

    fps_real = contador / (time.time() - inicio)
    cv2.putText(frame, texto, (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)
    cv2.putText(frame, f"FPS: {fps_real:.1f}", (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    cv2.imshow("Signa - Teste", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

captura.release()
cv2.destroyAllWindows()