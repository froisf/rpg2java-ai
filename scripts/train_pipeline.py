"""
train_pipeline.py - O FIO QUE FALTAVA
Mesmo if/else que você aprendeu em python-dio/teste/estrutura_condicionais.py
Mas agora para juntar seus datasets de RPG para treinar o LoRA

Autor: Flavio Frois - Projeto RPG2JAVA para comunidade IBM
Modelo base: unsloth/Qwen2.5-1.5B-Instruct-bnb-4bit
"""
import json
from pathlib import Path

# Constantes - igual IDADE_MINIMA = 18 da sua aula
TAMANHO_MINIMO_CONTEUDO = 20
PASTA_DATASETS = Path("datasets")
ARQUIVO_SAIDA = PASTA_DATASETS / "dataset-final.jsonl"

# Lista de JSONLs que você tem (os mesmos que o CodeGraph achou soltos)
arquivos_entrada = [
    PASTA_DATASETS / "rpg_ile_training_data.jsonl",
    PASTA_DATASETS / "novos-pares.jsonl",
]

# Pode adicionar mais se tiver
for extra in PASTA_DATASETS.glob("*.jsonl"):
    if extra.name not in ["dataset-final.jsonl"] and extra not in arquivos_entrada:
        arquivos_entrada.append(extra)

print("🚀 train_pipeline - RPG2JAVA")
print(f"Procurando em: {PASTA_DATASETS.resolve()}")

dataset_final = []
total_lidos = 0

for arquivo in arquivos_entrada:
    # MESMO if/else da sua aula de estrutura_condicionais.py!
    if not arquivo.exists():
        print(f"⏭️  Pula - não existe: {arquivo.name}")
        continue

    if arquivo.stat().st_size < 100:
        print(f"⏭️  Pula {arquivo.name} - muito pequeno / vazio")
        continue
    else:
        print(f"📖 Lendo: {arquivo.name}")

    try:
        with open(arquivo, encoding="utf-8") as f:
            for num_linha, linha in enumerate(f, 1):
                linha = linha.strip()
                if len(linha) < TAMANHO_MINIMO_CONTEUDO:
                    continue  # igual if idade < IDADE_MINIMA

                try:
                    exemplo = json.loads(linha)
                    # Valida formato esperado pro LoRA
                    if isinstance(exemplo, dict):
                        dataset_final.append(exemplo)
                        total_lidos += 1
                except json.JSONDecodeError:
                    print(f"⚠️  Linha {num_linha} inválida em {arquivo.name}")
    except Exception as e:
        print(f"❌ Erro em {arquivo.name}: {e}")

# Salva o dataset consolidado - pronto pro Colab
if dataset_final:
    # Cria pasta se não existir
    PASTA_DATASETS.mkdir(exist_ok=True)
    
    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as out:
        for ex in dataset_final:
            out.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print("\n" + "="*60)
    print(f"✅ SUCESSO! Gerado {ARQUIVO_SAIDA.name}")
    print(f"📊 Total de exemplos: {len(dataset_final)} (lidos {total_lidos})")
    print(f"📁 Local: {ARQUIVO_SAIDA.resolve()}")
    print(f"🎯 Próximo passo: Levar pro Colab e treinar lora_model_v2/")
    print(f"   Modelo base: unsloth/Qwen2.5-1.5B-Instruct-bnb-4bit")
    print("="*60)
    
    # Dica para IBM Bob - resolve MCP Payload
    print("\n💡 Dica IBM Bob - MCP Payload:")
    print("   Não mande rpgle/ inteiro. Mande:")
    print(f"   - Summary + 3 exemplos de {ARQUIVO_SAIDA.name} (< 8k tokens)")
else:
    print("\n❌ Nenhum exemplo válido encontrado. Verifique seus .jsonl em datasets/")
