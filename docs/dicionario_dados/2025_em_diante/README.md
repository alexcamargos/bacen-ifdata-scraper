# Dicionários de colunas do IF.Data a partir de 2025

Os documentos seguem a organização
`AAAA-MM/<escopo>/<relatório>.pdf`. O [manifesto](manifesto.json)
registra os identificadores do catálogo, a URL e o SHA-256 de cada
arquivo.

```bash
uv run python ifdata.py --download-dictionaries
```

Use `--data-base`, `--institution` ou `--report` para baixar uma seleção.
Para a Segmentação de março de 2025, o endpoint de PDF retornou erro
interno. O [JSON de Segmentação](2025-03/prudential_conglomerates/segmentation.json)
reúne a definição do relatório e os metadados de suas colunas obtidos
no próprio portal. As duas URLs estão no arquivo.
[IF.Data do Banco Central](https://www3.bcb.gov.br/ifdata/).
