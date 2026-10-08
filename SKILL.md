# SKILL.md - RPG ILE to Java 21 Skills

## Skills Mapeadas para IBM Bob

### 1. CHAIN/READE/READ -> Spring Data JPA
- **RPG:** `CHAIN (custId) Customer`
- **Java:** `customerRepository.findById(custId).orElseThrow()`
- **RPG:** `READE (status) Orders`
- **Java:** `orderRepository.findByStatus(status, Pageable)`

### 2. D-Specs -> Java Entity / Record
- **RPG:** `D Customer DS Qualified` + campos zoned/packed
- **Java:** `@Entity class Customer { @Id Long id; BigDecimal balance; }`
- **Conversão tipos:** Zoned(7,2) -> BigDecimal, Char(10) -> String, Date *ISO -> LocalDate

### 3. Indicators (*INLR, *IN90, *INxx) -> Exceptions / Booleans
- **RPG:** `*INLR = *ON; RETURN`
- **Java:** `return; // end of use case`
- **RPG:** `*IN90 = *ON` (erro)
- **Java:** `throw new BusinessException("...")` + try/catch

### 4. RAG Retrieval - Few-Shot
- Ao receber C-Spec, buscar 3 exemplos similares em `datasets/rpg_ile_training_data.jsonl`
- Formato: `{"messages": [{"role":"user","content":"RPG: ..."}, {"role":"assistant","content":"Java: ..."}]}`
- Usar `novos-pares.jsonl` como prioridade (casos reais do Hackathon RPG Java)

### 5. Como lidar com MCP Payload Limit (pergunta feita na comunidade IBM)
**Problema:** Arquivo RPG de 5000 linhas estoura limite do MCP (Model Context Protocol) do IBM Bob / watsonx Code Assistant.

**Solução implementada neste projeto:**
1. Não enviar arquivo RPG inteiro pro Bob.
2. Usar `scripts/dataset.py` para criar summary de 50 linhas (o que o programa faz).
3. Usar `scripts/train_pipeline.py` (if/else simples - mesmo do python-dio) para filtrar e consolidar `dataset-final.jsonl`
4. Mandar pro Bob: summary + 3 exemplos do RAG (total < 8k tokens) + instrução de Clean Architecture Java 21

**Comando para validar payload:**
`python -m codegraph analyze . --force` gera `.agents/codegraph/` que o @workspace usa sem estourar contexto.

## Stack
- Python 3.10+ (if, for, json, pathlib - aprendido em python-dio)
- Qwen2.5-1.5B-Instruct + LoRA (Unsloth)
- Java 21, Spring Boot, Clean Architecture
- IBM Bob / watsonx Code Assistant
- RAG com JSONL
