import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

LANDMARKS_DIR = "../data/landmarks"
SEQUENCE_LEN = 30
FEATURE_SIZE = 126

def reamostrar(seq, n=SEQUENCE_LEN):
    idx = np.linspace(0, len(seq) - 1, n).round().astype(int)
    return seq[idx]

X, y = [], []
label_map = {}

for arquivo in sorted(os.listdir(LANDMARKS_DIR)):
    if not arquivo.endswith(".npy"):
        continue

    sinal = arquivo.split("__")[0]
    if sinal not in label_map:
        label_map[sinal] = len(label_map)

    seq = np.load(os.path.join(LANDMARKS_DIR, arquivo))

    if len(seq) == 0:
        continue
    seq = reamostrar(seq)    

    X.append(seq)
    y.append(label_map[sinal])

X = np.array(X)
y = to_categorical(y, num_classes=len(label_map))

print(f"Total de amostras: {len(X)}")
print(f"Sinais: {label_map}")

# separa 80% treino e 20% teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=14, random_state=42, stratify=y
)

print(f"Treino: {len(X_train)} amostras")
print(f"Teste: {len(X_test)} amostras")

model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(SEQUENCE_LEN, FEATURE_SIZE)),
    Dropout(0.2),
    LSTM(128, return_sequences=False),
    Dropout(0.2),
    Dense(64, activation='relu'),
    Dense(len(label_map), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

os.makedirs("../models", exist_ok=True)

# salva automaticamente o melhor modelo
checkpoint = ModelCheckpoint(
    "../models/signa_model.keras",
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1
)

# para o treino se não melhorar por 15 epochs seguidas
early_stopping = EarlyStopping(
    monitor='val_accuracy',
    patience=15,
    restore_best_weights=True,
    verbose=1
)

model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=8,
    validation_data=(X_test, y_test),
    callbacks=[checkpoint, early_stopping]
)

# avalia no conjunto de teste
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\nAcurácia real no teste: {accuracy*100:.1f}%")

np.save("../models/label_map.npy", label_map)
print("\nModelo treinado e salvo!")
print("Labels:", label_map)