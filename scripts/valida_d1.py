import json, re
from pathlib import Path
f = Path('datasets/processed/s6_pairs_TRN.jsonl')
if not f.exists():
    print("Arquivo nao existe, roda cfc_to_trn_v2.py primeiro")
    exit()
txt = f.read_text(encoding='utf-8')
c_trn = len(re.findall(r'\bTRN\d{3}\b', txt))
c_trn_d1 = len(re.findall(r'\bTRN\d{3}D1\b', txt))
c_cfc_d1 = len(re.findall(r'\bCFC\d{3}D1\b', txt, re.I))
c_adb = len(re.findall(r'ADB017C', txt))
print(f'TRN000: {c_trn} ocorrencias')
if c_trn_d1>0:
    print(f'TRN001D1: {c_trn_d1} ocorrencias OK')
else:
    print(f'TRN001D1: {c_trn_d1} NAO ACHOU')
if c_cfc_d1>0:
    print(f'CFC001D1 leak: {c_cfc_d1} VAZOU!')
else:
    print(f'CFC001D1 leak: {c_cfc_d1} LIMPO')
print(f'ADB017C mantido: {c_adb}')
