# 🧠 Lista 2 — Processamento e Análise de Imagens

**Disciplina:** Processamento e Análise de Imagens

Este repositório contém os scripts e dados usados na Lista 2 da disciplina. A implementação está em Python e usa bibliotecas comuns para processamento de imagens.

## 🎯 Objetivo

1. Implementar e comparar métodos de segmentação de imagens (Questão de segmentação).
2. Extrair representações geométricas de objetos segmentados (contorno, código de cadeia e esqueleto) e gerar visualizações (Questão de representação).

## 📁 Estrutura do repositório

- `lista2_pai_segmentacao.py`  — script responsável pela etapa de segmentação (gera imagens em `data/outputs/`).
- `lista2_pai_representacao.py` — script que carrega segmentações, extrai contorno, código de cadeia e esqueleto e salva figuras em `data/representa/`.
- `data/` — pasta com imagens e saídas organizadas em subpastas:
    - `data/imgs/` — imagens de entrada (originais)
    - `data/outputs/` — imagens segmentadas (outputs dos algoritmos). O script de representação procura por arquivos com padrão `*_otsu.png` e `*_kmeans*.png` aqui.
    - `data/representa/` — imagens geradas pela representação (contorno + esqueleto)
    - `data/comparacao/` — (opcional) comparações ou resultados auxiliares

## Dependências

Instale as dependências (recomendado criar um ambiente virtual):

PowerShell (Windows):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install opencv-python numpy matplotlib scikit-image
```

Ou, sem virtualenv:

```powershell
pip install opencv-python numpy matplotlib scikit-image
```

Se preferir um `requirements.txt`, crie um com estas linhas:

```
opencv-python
numpy
matplotlib
scikit-image
```

## Como executar

1. (Opcional) Gere as segmentações executando o script de segmentação:

```powershell
python lista2_pai_segmentacao.py
```

Esse script deve salvar imagens segmentadas em `data/outputs/`.

2. Execute o script de representação para extrair contornos, código de cadeia (parcial) e esqueleto e salvar figuras em `data/representa/`:

```powershell
python lista2_pai_representacao.py
```

Observações sobre `lista2_pai_representacao.py`:
- Ele procura por arquivos em `data/outputs/` com padrão `*_otsu.png` e `*_kmeans*.png`.
- Para cada imagem encontrada ele:
    - Carrega em escala de cinza e binariza (OTSU).
    - Extrai o maior contorno e gera um código de cadeia (lista de direções entre pontos consecutivos do contorno).
    - Calcula o esqueleto com `skimage.morphology.skeletonize`.
    - Salva uma figura com três painéis: imagem segmentada, contorno sobreposto e esqueleto em `data/representa/{nome}_representacao.png`.

## Formato de entrada/saída (contrato rápido)

- Entrada: imagens segmentadas binárias em `data/outputs/` (padrão: `*_otsu.png`, `*_kmeans*.png`).
- Saída: imagens de visualização em `data/representa/` com sufixo `_representacao.png`.
- Erros/validações: o script reporta quando não encontra imagens ou quando não há contornos detectados.

## Casos de borda e recomendações

- Se `data/outputs/` estiver vazio, nada será processado — verifique se `lista2_pai_segmentacao.py` gerou arquivos.
- Objetos muito pequenos podem não gerar contornos significativos; filtre pequenos componentes caso necessário.
- Em imagens coloridas, converta para escala de cinza antes de segmentar.

## Exemplos de saída

- `data/representa/{nome}_representacao.png`: imagem com três paineis — segmentação binária, contorno sobreposto (verde) e esqueleto (mapa de pixels esqueleto).

