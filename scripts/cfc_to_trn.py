import json, re
from pathlib import Path

src = Path("datasets/processed/s6_pairs.jsonl")
dst = Path("datasets/processed/s6_pairs_TRN.jsonl")
dst_final = Path("datasets/dataset-final-TRN.jsonl")
map_file = Path("datasets/processed/mapa_CFC_TRN.json")

# 1. Cria mapa CFC000->TRN000
mapping = {}
# pega todos ids do s6_pairs
all_ids = []
for line in src.read_text(encoding="utf-8").splitlines():
    orig = json.loads(line)["id"].split("_")[0] # CFC000_V0 -> CFC000
    all_ids.append(orig)
all_ids = sorted(list(dict.fromkeys(all_ids)))

for orig in all_ids:
    m = re.match(r'([A-Z]+)(\d+)', orig)
    if m:
        prefix, num = m.groups()
        if prefix == "CFC": # sua regra
            mapping[orig] = f"TRN{int(num):03d}" # CFC000->TRN000
        else:
            mapping[orig] = f"{prefix}{int(num):03d}" # mantém outros se quiser, ou troca pra TRN tbm
    else:
        # sem número tipo CADTRANS -> TRN sequencial
        mapping[orig] = f"TRN{len(mapping):03d}"

map_file.write_text(json.dumps(mapping, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Mapa {len(mapping)}:")
for k,v in list(mapping.items())[:10]:
    print(f" {k} -> {v}")

# 2. Aplica dentro do código - CALLP CFC000 vira CALLP TRN000
def anon_code(code, mapping):
    c = code
    # ordena por tamanho pra não trocar CFC00 dentro de CFC000
    for orig in sorted(mapping.keys(), key=len, reverse=True):
        anon = mapping[orig]
        c = re.sub(rf'\b{re.escape(orig)}\b', anon, c, flags=re.IGNORECASE)
    return c

out = []
for line in src.read_text(encoding="utf-8").splitlines():
    obj = json.loads(line)
    orig_id = obj["id"].split("_")[0]
    anon_id = mapping.get(orig_id, orig_id)
    out.append({
        "id": anon_id, # TRN000
        "type": obj["type"],
        "input": anon_code(obj["input"], mapping)[:6000]
    })

dst.write_text("\n".join([json.dumps(x, ensure_ascii=False) for x in out]), encoding="utf-8")

# 3. Gera dataset-final-TRN = 111 + 6 + 697 anonimizados
base = []
for f in [Path("datasets/rpg_ile_training_data.jsonl"), Path("datasets/novos-pares.jsonl")]:
    if f.exists():
        base += [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]

final = base + out
dst_final.write_text("\n".join([json.dumps(x, ensure_ascii=False) for x in final]), encoding="utf-8")
print(f"\n✅ s6_pairs_TRN.jsonl: {len(out)}")
print(f"✅ dataset-final-TRN.jsonl: {len(final)} pronto pro Colab - CFC000->TRN000 dentro e fora")
