import json
from pathlib import Path
p = Path("datasets/dataset-final-TRN.jsonl")
out=[]
for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
    o=json.loads(line)
    txt=o.get("input","")
    up=txt.upper()
    # se tem qualquer vestigio do header CASAS, apaga e deixa só o nome do programa
    if "CASAS" in up or "DESENVOLVIMENTO" in up or "H*‚" in txt or "/=====" in txt:
        o["input"] = f"// Programa: {o['id']}\n"
        print(f"Limpando {o['id']} - deixado só nome")
    out.append(o)

p.write_text("\n".join([json.dumps(x, ensure_ascii=False) for x in out]), encoding="utf-8")
Path("datasets/dataset-final-TRN-CLEAN.jsonl").write_text("\n".join([json.dumps(x, ensure_ascii=False) for x in out]), encoding="utf-8")
print(f"Total final: {len(out)} - ADJQEB01 agora em branco com nome")
