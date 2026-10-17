import os
import shutil

ORIGEM = r"C:\Users\luisa\.cache\kagglehub\datasets\davimedio01\v-librasil\versions\1\videos UFPE (V-LIBRASIL)\data"
DESTINO = r"C:\Users\luisa\projetos\signa\ml\data\raw"

for arquivo in os.listdir(ORIGEM):
    if '_Articulador' not in arquivo:
        continue

    sinal = arquivo.split('_Articulador')[0]
    pasta_destino = os.path.join(DESTINO, sinal.upper())
    os.makedirs(pasta_destino, exist_ok=True)

    origem_arquivo = os.path.join(ORIGEM, arquivo)
    destino_arquivo = os.path.join(pasta_destino, arquivo)

    shutil.copy2(origem_arquivo, destino_arquivo)
    print(f"✓ {arquivo} → {sinal.upper()}/")

print("\nConcluído!")