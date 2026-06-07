# IDOR Response Platform

Plataforma de investigação e resposta automática a incidentes **IDOR** (Insecure Direct Object Reference).

Desafio técnico — Líder Técnico de Digital Forensics and Incident Response.

---

## Sprint 1.1 — Processamento de Logs

Pipeline inicial: ingestão forense, integridade da evidência, parsing de URIs e persistência em Parquet.

### Pré-requisitos

- Python **3.12+**
- Arquivo de entrada: `data/raw/three_months.csv` (~4,5M registros)

### Instalação

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### Execução

Na raiz do projeto:

```bash
python src/app.py
```

**Saídas geradas:**

```
data/
├── evidence/
│   └── chain_of_custody.json    # SHA-256 + metadados de integridade
└── processed/
    └── parsed_events.parquet    # logs normalizados + campos extraídos da URI
```

### Testes

```bash
pytest
```

### Estrutura (Sprint 1.1)

```
src/
├── config/settings.py       # caminhos e constantes
├── utils/filesystem.py      # criação de diretórios
├── models/
│   ├── events.py            # ParsedEvent (Pydantic v2)
│   └── features.py          # IpFeatures (Sprint 1.2+)
├── ingestion/
│   ├── loader.py            # scan CSV com Polars (LazyFrame)
│   └── integrity.py         # SHA-256 + chain of custody
├── parsing/
│   └── uri_parser.py        # extração invoice_id, site_id, authtoken
└── app.py                   # orquestrador do pipeline

tests/
├── test_integrity.py
└── test_uri_parser.py
```

### Decisões técnicas

| Decisão | Justificativa |
|---------|---------------|
| **Polars** (LazyFrame + streaming) | ~4,5M linhas; `scan_csv` evita carregar tudo em memória; execução lazy e `collect(streaming=True)` na escrita Parquet |
| **Parquet** | formato columnar compacto, leitura rápida nas etapas de detecção e features |
| **Pydantic v2** | contratos tipados para eventos e features; base para validação e serialização JSON nas fases seguintes |
| **SHA-256 + chain of custody** | requisito forense: prova de integridade do artefato original antes de qualquer transformação |
| **Rename de colunas no loader** | CSV usa `http_staus` (typo); normalização centralizada evita propagação do erro |

### Schema de entrada (CSV)

| Coluna original | Renomeada |
|-----------------|-----------|
| `timestamp` | `timestamp` |
| `http_staus` | `status_code` |
| `http_host` | `host` |
| `http_uri` | `uri` |
| `http_method` | `method` |
| `http_referer` | `referer` |
| `http_user_agent` | `user_agent` |
| `source_ip` | `source_ip` |

Campos extraídos da URI: `invoice_id`, `site_id`, `auth_token`.

---

## Roadmap (próximos sprints)

| Sprint | Escopo |
|--------|--------|
| **1.1** | Ingestão, integridade, parsing URI, Parquet |
| **1.2** | Métricas por IP, detecção de padrões IDOR, anomalias |
| **1.3** | Evidência forense: top IPs, timeline, IOCs (JSON) |
| **2.x** | Agentes GenAI (Triage, Forensic Analyst, Response Advisor) via LangGraph |
| **3.x** | Resposta NIST: contenção, TTD/TTR/TTC, playbook |
| **Final** | Docker Compose, observabilidade, relatório técnico, resumo executivo |
