import json
from pathlib import Path

# Mesmo if da sua aula de idade, mas pra IBM
TAMANHO_MINIMO = 20
datasets = Path("datasets").glob("*.jsonl")
saida = []

for arq in datasets:
    if arq.stat().st_size < 100: # if idade < IDADE_MINIMA
        print(f"Pula {arq.name} - vazio")
    else:
        for linha in open(arq, encoding="utf-8"):
            saida.append(json.loads(linha))

Path("datasets/dataset-final.jsonl").write_text(
    "\n".join([json.dumps(x, ensure_ascii=False) for x in saida]), 
    encoding="utf-8"
)
print(f"Gerado dataset-final.jsonl com {len(saida)} exemplos - pronto pro Colab")