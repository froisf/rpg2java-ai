# AGENTS.md - RPG2JAVA - IBM Bob Architecture

## Agents

### 1. rpg-analyzer
- **Role:** Lê código legado RPG ILE da pasta `rpgle/`
- **Input:** .rpgle, .sqlrpgle
- **Output:** JSON com D-Specs, C-Specs, CHAIN, READ, SETLL mapeados
- **Limitação MCP Payload:** Não envia arquivo inteiro, envia chunk de 500 linhas + summary gerado por `scripts/dataset.py`

### 2. java-generator
- **Role:** Converte JSON do analyzer em Java 21 + Clean Architecture
- **Modelo:** `unsloth/Qwen2.5-1.5B-Instruct-bnb-4bit` + LoRA `content/lora_model_v2/`
- **RAG:** Busca em `datasets/rpg_ile_training_data.jsonl` e `novos-pares.jsonl`
- **Output:** Entity, Repository, UseCase, Controller

### 3. doc-generator
- **Role:** Gera `.agents/codegraph/architecture.md` com CodeGraph para o Copilot entender o fluxo