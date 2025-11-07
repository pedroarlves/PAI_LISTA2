
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import skeletonize
import os
from glob import glob

# ==========================
# Funções auxiliares
# ==========================

def extrair_contorno(img_segmentada):
    _, binaria = cv2.threshold(img_segmentada, 127, 255, cv2.THRESH_BINARY)
    contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contornos, binaria

def gerar_codigo_cadeia(contorno):
    direcoes = [(0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1), (1,0), (1,1)]
    codigo = []
    for i in range(1, len(contorno)):
        dx = contorno[i][0][0] - contorno[i-1][0][0]
        dy = contorno[i][0][1] - contorno[i-1][0][1]
        if (dy, dx) in direcoes:
            codigo.append(direcoes.index((dy, dx)))
    return codigo

def exibir_resultados(img_segmentada, contorno, skeleton, nome_saida):
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(img_segmentada, cmap='gray')
    plt.title('Imagem Segmentada')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    img_cont = cv2.cvtColor(img_segmentada, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(img_cont, contorno, -1, (0,255,0), 1)
    plt.imshow(img_cont)
    plt.title('Contorno + Código de Cadeia')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(skeleton, cmap='gray')
    plt.title('Esqueleto do Objeto')
    plt.axis('off')

    os.makedirs(os.path.dirname(nome_saida), exist_ok=True)
    plt.savefig(nome_saida, bbox_inches='tight')
    plt.close()


# ==========================
# Execução principal
# ==========================

# Caminhos
input_dir = "./data/outputs/"
output_dir = "./data/representa/"
os.makedirs(output_dir, exist_ok=True)

# Busca imagens que correspondem ao padrão
imagens = glob(os.path.join(input_dir, "*_otsu.png")) + glob(os.path.join(input_dir, "*_kmeans*.png"))

if not imagens:
    print("⚠️ Nenhuma imagem encontrada em ./data/outputs/")
else:
    for caminho in imagens:
        nome_base = os.path.basename(caminho).replace(".png", "")
        print(f"🔹 Processando: {nome_base}")

        img_segmentada = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)
        if img_segmentada is None:
            print(f"❌ Erro ao carregar {caminho}")
            continue

        # Binariza a imagem
        _, img_segmentada = cv2.threshold(img_segmentada, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Extrair contornos
        contornos, binaria = extrair_contorno(img_segmentada)
        if len(contornos) == 0:
            print(f"⚠️ Nenhum contorno encontrado em {nome_base}")
            continue

        contorno = max(contornos, key=cv2.contourArea)
        codigo_cadeia = gerar_codigo_cadeia(contorno)
        print(f"   Código da cadeia (parcial): {codigo_cadeia[:20]} ...")

        # Calcular esqueleto
        skeleton = skeletonize(binaria > 0)

        # Gerar visualização e salvar
        saida_fig = os.path.join(output_dir, f"{nome_base}_representacao.png")
        exibir_resultados(binaria, [contorno], skeleton, saida_fig)

        print(f"   ✅ Resultado salvo em {saida_fig}")

print("🟢 Processamento concluído com sucesso!")
