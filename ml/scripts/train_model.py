import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical

LANDMARKS_DIR = "../data/landmarks"
SEQUENCE_LEN = 30 # padroniza os vídeos para apenas 30 frames
FEATURE_SIZE = 126 # 2 mão x 21 pontos x 3 coordenadas

X, y = [], []
label_map = {}

for arquivo in sorted(os.listdir(LANDMARKS_DIR)):
    if not arquivo.endswith(".npy"):
        continue

    sinal = arquivo.split("__")[0]
    if sinal not in label_map:
        label_map[sinal] = len(label_map)

    seq = np.load(os.path.join(LANDMARKS_DIR, arquivo))

    # padroniza para SEQUENCE_LEN frames (corta ou preenche com 0)
    if len(seq) >= SEQUENCE_LEN:
        seq = seq[:SEQUENCE_LEN]
    else:
        pad = np.zeros((SEQUENCE_LEN - len(seq), FEATURE_SIZE))
        seq = np.vstack([seq, pad])

    X.append(seq)
    y.append(label_map[sinal])

X = np.array(X)
y = to_categorical(y, num_classes = len(label_map))

print(F"Total de amostras: {len(X)}")
print(f"Sinais: {label_map}")

# com poucos dados, não da pra separar teste de forma significativa
# então treinamos com tudo só para validar que o pipeline funciona
model = Sequential([
    LSTM(64, return_sequences = True, input_shape = (SEQUENCE_LEN, FEATURE_SIZE)),
    Dropout(0.2),
    LSTM(128, return_sequences = False),
    Dropout(0.2),
    Dense(64, activation = 'relu'),
    Dense(len(label_map), activation = 'softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

model.fit(X, y, epochs = 30, batch_size = 4)

os.makedirs("../models", exist_ok = True)
model.save("../models/signa_model.keras")
np.save("../models/label_map.npy", label_map)

print("n\Modelo treinado e salvo.")
print("Labels: ", label_map)