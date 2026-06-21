import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# carrega o modelo treinado e o mapa de labels
modelo = tf.keras.models.load_model("../models/signa_model.keras")
label_map = np.load("../models/label_map.npy", allow_pickle = True).item()
index_to_label = {v: k for k, v in label_map.items()}

print("Sinais reconhecidos: ", label_map)

# configura o detector de mãos (mesma config. do extract_landmarks.py)
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task') # carrega o modelo

options = vision.HandLandmarkerOptions( # configura para detectar 2 mãos pot frame
    base_options = base_options,
    num_hands = 2
)

detector = vision.HandLandmarker.create_from_options(options) # detector a partir das opções

SEQUENCE_LEN = 30
FEATURE_SIZE = 126

def extrair(resultado):
    mao_direita = np.zeros(21*3)
    mao_esquerda = np.zeros(21*3)

    # resultado.hand_landmarks -> lista com os landmarks de cada mão detectada
    # resultado.handness -> lista que diz se cada mão é esquerda ou direita

    for i, mao in enumerate(resultado.hand_landmarks):
        # converte os 21 pontos da mão em array
        coords = np.array([[lm.x, lm.y, lm.z] for lm in mao]).flatten()

        # descobrir mão esquerda ou direita pelo handedness
        label = resultado.handedness[i][0].display_name
        if label == 'Left':
            mao_esquerda = coords
        else:
            mao_direita = coords

    # juntar tudo em um vetor de 126 numeros
    return np.concatenate([mao_esquerda, mao_direita])

# abre a webcam
captura = cv2.VideoCapture(0)
buffer_frames = []

print("n\Pressione 'q para sair. Faça o sinal na frente da camera")

while captura.isOpened():
    ret, frame = captura.read()
    if not ret:
        break

    frame = cv2.flip(frame,1) # espelha pra ficar mais natural
    imagem = mp.Image(
        image_format = mp.ImageFormat.SRGB,
        data = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    )
    resultado = detector.detect(imagem)
    keypoints = extrair(resultado)
    buffer_frames.append(keypoints)

    # mantém os ultimos 30 frames
    if len(buffer_frames) > SEQUENCE_LEN:
        buffer_frames.pop(0)

    # quando tiver 30 frames, faz a predição
    if len(buffer_frames) == SEQUENCE_LEN:
        sequencia = np.expand_dims(np.array(buffer_frames), axis = 0)
        predicao = modelo.predict(sequencia, verbose = 0)[0]
        indice = np.argmax(predicao)
        confianca = predicao[indice]
        sinal_previsto = index_to_label[indice]

        texto = f"{sinal_previsto} ({confianca*100:.1f}%)"
        cv2.putText(frame, texto, (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow("Signa - Teste", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

captura.release()
cv2.destroyAllWindows()