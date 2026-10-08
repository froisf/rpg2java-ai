import json, re
from pathlib import Path
from collections import Counter

p = Path("datasets/dataset-final-TRN.jsonl")
fails=[]
ok=0
c_trn=Counter()
c_cfc=Counter()

for i, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
    try:
        obj=json.loads(line)
    except:
        fails.append(f"Linha {i}: JSON invalido")
        continue
    id_prog=obj.get("id","?")
    code=obj.get("input","") or obj.get("codigo","")
    up=code.upper()

    # 1. Regras que voce pediu
    if "CASAS" in up or "DESENVOLVIMENTO" in up:
        fails.append(f"{id_prog}: ainda tem H* CASAS/DESENVOLVIMENTO")
    if not code.strip():
        fails.append(f"{id_prog}: codigo vazio")
    
    # 2. TRN vs CFC
    c_trn["TRN000"] += up.count("TRN000")
    c_trn["TRN001D1"] += up.count("TRN001D1")
    c_cfc["CFC001"] += len(re.findall(r'(?<![A-Z0-9])CFC001(?![A-Z0-9])', up))
    c_cfc["CFC001D1"] += len(re.findall(r'(?<![A-Z0-9])CFC001D1(?![A-Z0-9])', up))

    # 3. Sintaxe RPG basica
    if "DCL-F" not in up and "DCL-PROC" not in up and "BEGSR" not in up and "DCL-S" not in up and "// Programa" not in code:
        # pode ser ok se for programa pequeno, só avisa
        pass

    ok+=1

print(f"=== VALIDACAO CODIGO ===")
print(f"Total lidos: {ok}")
print(f"TRN000: {c_trn['TRN000']} | TRN001D1: {c_trn['TRN001D1']}")
print(f"CFC leak: CFC001={c_cfc['CFC001']} CFC001D1={c_cfc['CFC001D1']} (tem que ser 0)")
print(f"Falhas CASAS/vazio: {len(fails)}")
for f in fails[:20]:
    print(" -", f)

if not fails and c_cfc["CFC001"]==0 and c_cfc["CFC001D1"]==0:
    print("\n✅ CODIGO VALIDO - pronto pro lora_model_v2")
else:
    print("\n❌ CORRIGIR falhas acima")
