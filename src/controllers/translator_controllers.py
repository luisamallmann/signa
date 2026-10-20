import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from pathlib import Path
import numpy as np
import tensorflow as tf
from flask import request, jsonify

# controllers -> src -> raiz do projeto -> ml/models
MODELS_DIR = Path(__file__).resolve().parents[2] / "ml" / "models"

SEQUENCE_LEN = 30
FEATURE_SIZE = 126
MIN_FRAMES_COM_MAO = 20

# carrega uma única vez, quando o servidor sobe
modelo = tf.keras.models.load_model(MODELS_DIR / "signa_model.keras")
label_map = np.load(MODELS_DIR / "label_map.npy", allow_pickle=True).item()
index_to_label = {v: k for k, v in label_map.items()}


def normalizar(seq):
    """
    IGUAL ao normalizar() do ml/scripts/train_model.py — se mudar um, mude o outro.
    Deixa os pontos independentes de onde a pessoa está na tela e do tamanho da mão.
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
        tamanho = np.linalg.norm(mao[:, 9, :2] - mao[:, 0, :2], axis=1)
        escala = float(np.median(tamanho[presente])) + 1e-6
        rel = (mao - pulso[:, None, :]) / escala
        centro = pulso[presente].mean(axis=0)
        rel[:, 0, :] = (pulso - centro) / escala
        rel[~presente] = 0
        out[:, h*63:(h+1)*63] = rel.reshape(T, 63)
    return out



def predict():
    dados = request.get_json(silent=True) or {}
    frames = np.array(dados.get("frames", []), dtype="float32")

    if frames.shape != (SEQUENCE_LEN, FEATURE_SIZE):
        return jsonify(error=f"formato inválido: {frames.shape}"), 400

    # poucos frames com mão = ninguém sinalizando
    if int((frames != 0).any(axis=1).sum()) < MIN_FRAMES_COM_MAO:
        return jsonify(label=None, confidence=0.0)

    frames = normalizar(frames)
    probs = modelo(frames[None, ...], training=False).numpy()[0]
    i = int(np.argmax(probs))
    return jsonify(label=index_to_label[i], confidence=float(probs[i]))