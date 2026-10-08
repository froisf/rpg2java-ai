import json
from pathlib import Path
p=Path("datasets/dataset-final-TRN.jsonl")
data=[]
for l in p.read_text(encoding="utf-8", errors="ignore").splitlines():
    if not l.strip(): continue
    o=json.loads(l)
    _id=o.get("id","?")
    # pega código de onde estiver
    code = o.get("input") or o.get("codigo") or o.get("code") or ""
    # limpa 100% agressivo como você pediu
    if "ADJQEB01" in _id or "CASAS" in code.upper() or "DESENVOLVIMENTO" in code.upper():
        # deixa em branco só com nome do programa
        clean = f"** Programa: {_id} **"
    else:
        clean = code
    # grava em TODOS os campos pra valida_trn não achar em outro
    o["input"]=clean
    o["codigo"]=clean
    o["code"]=clean
    data.append(o)

p.write_text("\n".join([json.dumps(x, ensure_ascii=False) for x in data]), encoding="utf-8")
Path("datasets/dataset-final-TRN-CLEAN.jsonl").write_text("\n".join([json.dumps(x, ensure_ascii=False) for x in data]), encoding="utf-8")
print(f"ADJQEB01 agora: {[x['input'] for x in data if x['id']=='ADJQEB01'][0]}")
print(f"Total: {len(data)}")
