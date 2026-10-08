import json, re
from pathlib import Path
print("=== VALIDACAO ANON CFC->TRN ===\n")
map_file = Path("datasets/processed/mapa_CFC_TRN.json")
s6_trn = Path("datasets/processed/s6_pairs_TRN.jsonl")
final_trn = Path("datasets/dataset-final-TRN.jsonl")
if not map_file.exists():
    print("❌ mapa_CFC_TRN.json nao existe - roda cfc_to_trn.py primeiro")
    exit()
mapping = json.loads(map_file.read_text(encoding="utf-8"))
print(f"1. Mapa: {len(mapping)} entradas")
print(f" CFC000 -> {mapping.get('CFC000','?')}")
print(f" CFC001 -> {mapping.get('CFC001','?')}")
adb = mapping.get('ADB017C','?')
print(f" ADB017C -> {adb} {'✅ MANTIDO' if adb=='ADB017C' else '❌ ALTERADO!'}")

leak_cfc = 0
has_trn = 0
has_adb = 0
if s6_trn.exists():
    for line in s6_trn.read_text(encoding="utf-8").splitlines()[:200]:
        obj = json.loads(line)
        txt = obj["input"] + " " + obj["id"]
        if re.search(r'\bCFC\d{3}\b', txt, re.I):
            leak_cfc += 1
        if re.search(r'\bTRN\d{3}\b', txt):
            has_trn += 1
        if "ADB017C" in txt:
            has_adb += 1
    print(f"\n2. s6_pairs_TRN.jsonl (amostra 200):")
    print(f" Com TRN000: {has_trn} {'✅' if has_trn>0 else '❌'}")
    print(f" Com leak CFC000: {leak_cfc} {'❌ VAZOU!' if leak_cfc>0 else '✅ LIMPO'}")
    print(f" Com ADB017C: {has_adb} {'✅ mantido' if has_adb>0 else 'ℹ️ nao na amostra'}")
    sample = json.loads(s6_trn.read_text(encoding="utf-8").splitlines()[0])
    print(f"\n3. Consistencia: ID: {sample['id']}")
    print(f" {sample['input'][:300]}")
else:
    print("❌ s6_pairs_TRN.jsonl nao existe")

final_count = len(final_trn.read_text(encoding="utf-8").splitlines()) if final_trn.exists() else 0
print(f"\n4. dataset-final-TRN.jsonl: {final_count} {'✅ 814 OK' if final_count==814 else '❌ esperado 814'}")
print(f"\n5. Gitignore:")
gitignore = Path(".gitignore").read_text(encoding="utf-8") if Path(".gitignore").exists() else ""
for c in ["dataset-final-TRN.jsonl", "mapa_CFC_TRN.json", "raw-qrpglesrc"]:
    print(f" {c}: {'✅ ignorado' if c in gitignore else '❌ NAO IGNORADO!'}")
print("\n=== FIM ===")
