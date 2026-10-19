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


def predict():
    dados = request.get_json(silent=True) or {}
    frames = np.array(dados.get("frames", []), dtype="float32")

    if frames.shape != (SEQUENCE_LEN, FEATURE_SIZE):
        return jsonify(error=f"formato inválido: {frames.shape}"), 400

    # poucos frames com mão = ninguém sinalizando
    if int((frames != 0).any(axis=1).sum()) < MIN_FRAMES_COM_MAO:
        return jsonify(label=None, confidence=0.0)

    probs = modelo(frames[None, ...], training=False).numpy()[0]
    i = int(np.argmax(probs))
    return jsonify(label=index_to_label[i], confidence=float(probs[i]))