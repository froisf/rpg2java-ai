from pathlib import Path
import json

base = Path(__file__).parent.parent
datasets = base / "datasets"
processed = datasets / "processed"

all_data = []
for f in [datasets/"rpg_ile_training_data.jsonl", datasets/"novos-pares.jsonl", processed/"s6_pairs.jsonl"]:
    if f.exists():
        lines = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
        print(f"Lendo {f.name}: {len(lines)}")
        all_data.extend(lines)

out = datasets / "dataset-final.jsonl"
out.write_text("\n".join([json.dumps(x, ensure_ascii=False) for x in all_data]), encoding="utf-8")

print(f"SUCESSO! dataset-final.jsonl com {len(all_data)} exemplos")
print(f"117 antigos + 697 S6 reais")
