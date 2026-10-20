import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout

# caminhos a partir da pasta deste arquivo (funciona rodando de qualquer lugar)
BASE = os.path.dirname(os.path.abspath(__file__))
LANDMARKS_DIR = os.path.join(BASE, "..", "data", "landmarks")
MODELS_DIR = os.path.join(BASE, "..", "models")

SEQUENCE_LEN = 30
FEATURE_SIZE = 126
COPIAS_POR_VIDEO = 30   # quantas versões alteradas de cada vídeo criar
EPOCHS = 60

rng = np.random.default_rng(42)
tf.keras.utils.set_random_seed(42)


def reamostrar(seq, n=SEQUENCE_LEN):
    # pega n frames igualmente espaçados do início ao fim do vídeo
    idx = np.linspace(0, len(seq) - 1, n).round().astype(int)
    return seq[idx]


def normalizar(seq):
    """
    Deixa os pontos independentes de onde a pessoa está na tela e do tamanho da mão.
    Para cada mão: os 20 pontos dos dedos ficam relativos ao pulso, divididos pelo
    tamanho da mão; o lugar do pulso guarda o movimento da mão em relação ao centro
    do sinal. IGUAL ao normalizar() do src/controllers/translator_controllers.py.
    """
    seq = np.asarray(seq, dtype="float32")
    T = len(seq)
    out = np.zeros_like(seq)
    for h in (0, 1):  # 0 = esquerda, 1 = direita
        mao = seq[:, h*63:(h+1)*63].reshape(T, 21, 3)
        presente = np.abs(mao).sum(axis=(1, 2)) > 0
        if not presente.any():
            continue
        pulso = mao[:, 0, :]
        tamanho = np.linalg.norm(mao[:, 9, :2] - mao[:, 0, :2], axis=1)  # pulso -> base do dedo médio
        escala = float(np.median(tamanho[presente])) + 1e-6
        rel = (mao - pulso[:, None, :]) / escala
        centro = pulso[presente].mean(axis=0)
        rel[:, 0, :] = (pulso - centro) / escala
        rel[~presente] = 0
        out[:, h*63:(h+1)*63] = rel.reshape(T, 63)
    return out


def aumentar(seq):
    """Cria uma cópia levemente diferente do vídeo: corta um pouco do começo/fim,
    gira um pouco, estica um pouco na horizontal e adiciona um tremidinho."""
    seq = np.asarray(seq, dtype="float32").copy()
    T = len(seq)
    ini = rng.integers(0, max(1, int(T * 0.12)))
    fim = T - rng.integers(0, max(1, int(T * 0.12)))
    seq = seq[ini:fim]
    ang = np.deg2rad(rng.uniform(-12, 12))
    c, s = np.cos(ang), np.sin(ang)
    estica = rng.uniform(0.9, 1.1)
    pts = seq.reshape(len(seq), 42, 3)
    pres = np.abs(pts).sum(axis=2) > 0
    x = pts[..., 0] - 0.5
    y = pts[..., 1] - 0.5
    pts[..., 0] = np.where(pres, (c*x - s*y) * estica + 0.5, 0)
    pts[..., 1] = np.where(pres, s*x + c*y + 0.5, 0)
    pts += np.where(pres[..., None], rng.normal(0, 0.004, pts.shape), 0)
    return pts.reshape(len(seq), FEATURE_SIZE)


# ---------- carrega os vídeos ----------
X, y = [], []
label_map = {}
videos = 0

for arquivo in sorted(os.listdir(LANDMARKS_DIR)):
    if not arquivo.endswith(".npy"):
        continue
    seq = np.load(os.path.join(LANDMARKS_DIR, arquivo))
    if len(seq) == 0:
        continue

    sinal = arquivo.split("__")[0]
    if sinal not in label_map:
        label_map[sinal] = len(label_map)
    videos += 1

    X.append(normalizar(reamostrar(seq)))       # o vídeo original
    y.append(label_map[sinal])
    for _ in range(COPIAS_POR_VIDEO):            # + cópias alteradas
        X.append(normalizar(reamostrar(aumentar(seq))))
        y.append(label_map[sinal])

X = np.array(X)
y = np.array(y)

print(f"Vídeos: {videos}")
print(f"Amostras de treino (com cópias): {len(X)}")
print(f"Sinais ({len(label_map)}): {label_map}")

# ---------- modelo ----------
model = Sequential([
    Input((SEQUENCE_LEN, FEATURE_SIZE)),
    LSTM(64, return_sequences=True),
    Dropout(0.2),
    LSTM(128, return_sequences=False),
    Dropout(0.2),
    Dense(64, activation='relu'),
    Dense(len(label_map), activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

# treina com TODOS os vídeos (não separa teste: o teste de verdade é na webcam)
model.fit(X, y, epochs=EPOCHS, batch_size=32, shuffle=True)

os.makedirs(MODELS_DIR, exist_ok=True)
model.save(os.path.join(MODELS_DIR, "signa_model.keras"))
np.save(os.path.join(MODELS_DIR, "label_map.npy"), label_map)

print("\nModelo treinado e salvo em", os.path.abspath(MODELS_DIR))
print("Labels:", label_map)
