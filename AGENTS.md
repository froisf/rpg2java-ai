# AGENTS.md - RPG2JAVA - IBM Bob Architecture

## Overview
Projeto RPG2JAVA - Modernização de RPG ILE para Java 21 + Clean Architecture usando IBM Bob, RAG e fine-tuning LoRA.

Autor: FLAVIO FROIS - IBM i Professional (AS/400, RPG ILE) com 15+ anos, transição para Java 21 e Generative AI.
Iniciativas: Hackathon RPG Java, IBM Bob platform, projeto pessoal RPG2JAVA (LoRA + RAG).

## Agents

### 1. rpg-analyzer
- **Role:** Lê código legado RPG ILE da pasta `rpgle/`
- **Input:** .rpgle, .sqlrpgle (D-Specs, C-Specs, F-Specs)
- **Output:** JSON com estrutura mapeada: arquivos, campos, CHAIN, READ, SETLL, indicators
- **Limitação MCP Payload:** Não envia arquivo inteiro. Envia chunk de 500 linhas + summary gerado por `scripts/dataset.py`
- **Local:** `scripts/dataset.py`

### 2. java-generator
- **Role:** Converte JSON do analyzer em Java 21 + Clean Architecture
- **Modelo Base:** `unsloth/Qwen2.5-1.5B-Instruct-bnb-4bit`
- **Adapter:** `content/lora_model_v2/` (LoRA fine-tuned)
- **RAG:** Busca em `datasets/rpg_ile_training_data.jsonl` e `datasets/novos-pares.jsonl` e `datasets/dataset-final.jsonl`
- **Output:** Entity, Repository (Spring Data JPA), UseCase, Controller, DTO
- **Local:** `scripts/inference.py` + `scripts/train_pipeline.py`

### 3. doc-generator
- **Role:** Gera documentação para Copilot / Cursor entender o fluxo ponta a ponta
- **Tool:** CodeGraph (`D:\Workspace\02-Labs\codegraph-tool`)
- **Output:** `.agents/codegraph/architecture.md`, `modules.md`, `hotspots.md`
- **Comando:** `python -m codegraph analyze . --force`

## Fluxo Ponta a Ponta
rpgle/ -> rpg-analyzer (dataset.py) -> datasets/*.jsonl -> train_pipeline.py -> dataset-final.jsonl -> Colab (Qwen2.5 LoRA) -> lora_model_v2/ -> java-generator -> Java 21
