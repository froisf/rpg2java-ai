# SKILL.md - RPG ILE to Java 21 Skills

## Skills Mapeadas
- **CHAIN/READE -> Spring Data JPA:** Converte CHAIN para findById, READE para findAll com paginação
- **D-Specs -> Java Record/Entity:** DS para @Entity, campos zoned/packed para BigDecimal
- **Indicators (*INLR, *IN90) -> Exceptions/Booleans:** *INLR true vira return, *IN90 error vira try/catch
- **RAG Retrieval:** Ao receber C-Spec, busca 3 exemplos similares no JSONL para few-shot

## Como lidar com MCP Payload Limit (sua pergunta no post)
- Não enviar arquivo RPG inteiro pro Bob. 
- Usar `scripts/dataset.py` para criar summary de 50 linhas.
- Mandar summary + 3 exemplos do RAG (total < 8k tokens).