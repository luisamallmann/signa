import cv2 # le e processa os videos
import mediapipe as mp # detecta os landmarks
import numpy as np # arrays numericos
import os # navega por pastas e arquivos

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# define diretorios
RAW_DIR = "../data/raw" # local dos vídeos
OUT_DIR = "../data/landmarks" # local das saídas
os.makedirs(OUT_DIR, exist_ok=True)

# detector api

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task') # carrega o modelo

options = vision.HandLandmarkerOptions( # configura para detectar 2 mãos pot frame
    base_options = base_options,
    num_hands = 2
)

detector = vision.HandLandmarker.create_from_options(options) # detector a partir das opções

# função extração

def extrair(resultado):
    """
    Receba o resultado do detector e retorna um vetor de 126 numeros.
    2 mãos x 21 pontos das mãos x 3 coordenadas (x, y, z) = 126
    """
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

for sinal in os.listdir(RAW_DIR): # percorre pelas pastas dos videos
    sinal_path = os.path.join(RAW_DIR, sinal)
    if not os.path.isdir(sinal_path): # ignora se não for pasta
        continue

    for arq_video in os.listdir(sinal_path): # percorre pelos vídeos
        if not arq_video.endswith(".mp4"):
            continue

        video_path = os.path.join(sinal_path, arq_video)
        captura = cv2.VideoCapture(video_path) # abre o vídeo
        frames_data = [] # guarda os keypoints de cada frame

        while captura.isOpened():
            ret, frame = captura.read() # lê um frame
            if not ret: # acabou o vídeo
                break

            # conversao do frame p/ o mediapipe ler
            imagem = mp.Image(
                image_format = mp.ImageFormat.SRGB,
                data = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            )

            resultado = detector.detect(imagem)
            keypoints = extrair(resultado)
            frames_data.append(keypoints)

        captura.release()

        saida = f"{sinal}__{arq_video.replace('.mp4', '')}.npy"
        np.save(os.path.join(OUT_DIR, saida), np.array(frames_data))
        print(f"{saida} - {len(frames_data)} frames")

print("\nExtração concluida.")