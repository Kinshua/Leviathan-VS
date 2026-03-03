# ☠️ Contributing to Leviathan-VS v66.6.0

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ☠️  LEVIATHAN VS — OPERATOR INDUCTION PROTOCOL  ☠️                        ║
║                                                                              ║
║   Classification: OMEGA-BLACK                                                ║
║   Clearance Required: Level 3+ (Contributor)                                ║
║                                                                              ║
║   "Cada contribuicao e um tentaculo a mais no monstro.                       ║
║    Cada PR e uma arma nova no arsenal.                                       ║
║    Cada bug fix, uma camada de armadura."                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## ⚡ Quick Start — Ambiente de Desenvolvimento

```bash
# 1. Fork + Clone o monstro
git clone https://github.com/SEU-USER/Leviathan-VS.git
cd Leviathan-VS

# 2. Crie uma branch de guerra
git checkout -b feature/nova-arma

# 3. Instale dependencias de dev (arsenal completo)
pip install -e ".[dev]"

# 4. Rode os testes (79+ testes devem passar — TODOS)
pytest tests/ -v

# 5. Diagnostico de profundidade
python core/doctor.py

# 6. Validar configs de guerra
python core/config_schema.py

# 7. Lint (qualidade militar)
ruff check core/

# 8. Type check (sem erros escapam)
pyright core/
```

---

## 🎖️ Sistema de Ranks — Hierarquia de Contribuicao

```
  ╔═══════════════════════════════════════════════════════════════════╗
  ║                    CONTRIBUTOR RANK SYSTEM                        ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  RANK 1 ★         RECRUIT          1-2 PRs merged               ║
  ║  RANK 2 ★★        OPERATOR         3-5 PRs merged               ║
  ║  RANK 3 ★★★       SPECIALIST       6-10 PRs + MCP contribution  ║
  ║  RANK 4 ★★★★      COMMANDER        11+ PRs + major feature      ║
  ║  RANK 5 ★★★★★     ARCHITECT        Core maintainer access       ║
  ║                                                                   ║
  ║  Each rank unlocks deeper access to the abyss.                   ║
  ║                                                                   ║
  ╚═══════════════════════════════════════════════════════════════════╝
```

---

## 📋 Estrutura de PRs — Padrao Operacional

### Formato de Titulo

```
[AREA] tipo: descricao concisa
```

### Tipos Aceitos

| Tipo       | Descricao                | Exemplo                                               |
| ---------- | ------------------------ | ----------------------------------------------------- |
| `feat`     | Nova funcionalidade/arma | `[KRAKEN] feat: add 50 evasion rules for cloud terms` |
| `fix`      | Correcao de bug/vuln     | `[MCP] fix: sanitize path traversal in tool call`     |
| `perf`     | Otimizacao               | `[TRANSLATOR] perf: 3x faster regex compilation`      |
| `docs`     | Documentacao             | `[DOCS] docs: add AD attack walkthrough`              |
| `test`     | Testes                   | `[TESTS] test: add MCP server integration tests`      |
| `refactor` | Refatoracao              | `[CORE] refactor: split translator into modules`      |
| `style`    | Estilo (lint/format)     | `[CORE] style: apply ruff formatting`                 |
| `ci`       | CI/CD                    | `[CI] ci: add GitHub Actions pipeline`                |
| `mcp`      | Novo servidor MCP        | `[MCP] mcp: add Maltego MCP server (21 tools)`        |
| `weapon`   | Nova ferramenta ofensiva | `[MOBILE] weapon: add runtime SSL unpin via Frida`    |

### Template de PR Body

```markdown
## Descricao
[O que essa PR faz e por que]

## Tipo de Mudanca
- [ ] feat: Nova funcionalidade
- [ ] fix: Correcao
- [ ] mcp: Novo MCP server
- [ ] weapon: Nova ferramenta/arma
- [ ] docs: Documentacao
- [ ] test: Testes

## MITRE ATT&CK (se aplicavel)
- Tactic: TA00XX
- Technique: T1XXX

## Checklist
- [ ] 🧪 Testes passam (`pytest tests/ -v`)
- [ ] ⚙️ Configs validos (`python core/config_schema.py`)
- [ ] 🏥 Doctor OK (`python core/doctor.py`)
- [ ] 🔒 Sem credenciais/secrets no codigo
- [ ] 📖 Documentacao atualizada
- [ ] 📋 CHANGELOG.md atualizado
- [ ] 🔢 Contadores atualizados (servers, tools, tasks)
```

---

## 🎨 Padrao de Codigo — Military Code Standard

### Python

```python
# ✅ CORRETO — Padrao Leviathan
def translate_term(text: str, mode: str = "encode") -> tuple[str, list[dict]]:
    """Traduz termo usando KRAKEN ENGINE.

    Args:
        text: Texto para traduzir.
        mode: 'encode' (submergir) ou 'decode' (emergir).

    Returns:
        Tupla (texto_traduzido, lista_de_mudancas).
    """
    ...

# ❌ ERRADO
def translate(t, m="e"):
    ...
```

### Regras

| Regra             | Padrao                                            |
| ----------------- | ------------------------------------------------- |
| 🐍 **Python**      | 3.9+ (compativel 3.9 → 3.14)                      |
| 📝 **Encoding**    | UTF-8 sem BOM                                     |
| 📏 **Line length** | 100 chars (ruff enforced)                         |
| 📖 **Docstrings**  | Google style para classes e funcoes publicas      |
| 🔍 **Type hints**  | Obrigatorio para funcoes publicas                 |
| 🎯 **Linter**      | ruff (config em pyproject.toml)                   |
| 📕 **Nomes**       | Variaveis em ingles, mensagens podem ser em PT-BR |
| 🎨 **Output**      | Sem cores quando `--json` flag presente           |
| ⚡ **Imports**     | Agrupados: stdlib → 3rd party → local             |

---

## 🧠 Como Criar um Novo MCP Server

Novos servidores MCP multiplicam o poder do Leviathan. Siga o protocolo:

### Estrutura Obrigatoria

```
core/<nome>/
├── __init__.py              # Exports do pacote
├── mcp_mcp_<nome>.py        # O servidor MCP (JSON-RPC 2.0)
└── README.md                # Documentacao do server (opcional)
```

### Protocolo de Registro (5 Passos Obrigatorios)

```
  ╔═══════════════════════════════════════════════════════════════════════╗
  ║                    MCP SERVER CREATION PROTOCOL                       ║
  ╠═══════════════════════════════════════════════════════════════════════╣
  ║                                                                       ║
  ║  PASSO 1: Criar core/<nome>/mcp_mcp_<nome>.py                       ║
  ║           - Implementar JSON-RPC 2.0 sobre stdio                     ║
  ║           - initialize/tools-list/tools-call/shutdown                 ║
  ║           - Cada tool com name, description, inputSchema             ║
  ║                                                                       ║
  ║  PASSO 2: Registrar em .vscode/mcp.json                             ║
  ║           - type: "stdio"                                             ║
  ║           - command: "python"                                        ║
  ║           - args: ["core/<nome>/mcp_mcp_<nome>.py"]                  ║
  ║                                                                       ║
  ║  PASSO 3: Documentar em .github/copilot-instructions.md             ║
  ║           - Descrever cada tool                                      ║
  ║           - Exemplos de uso                                          ║
  ║           - Mapeamento MITRE ATT&CK                                  ║
  ║                                                                       ║
  ║  PASSO 4: Adicionar tasks em .vscode/tasks.json                     ║
  ║           - Minimo 2 tasks por server                                ║
  ║           - Prefixo: [NOME] - Descricao                             ║
  ║                                                                       ║
  ║  PASSO 5: Atualizar contadores                                      ║
  ║           - README.md (servers, tools)                               ║
  ║           - __version__.py (__mcp_servers__, __total_tools__)        ║
  ║           - CHANGELOG.md (registrar adicao)                          ║
  ║                                                                       ║
  ╚═══════════════════════════════════════════════════════════════════════╝
```

### Exemplo de Tool Definition

```python
{
    "name": "meu_tool_scan",
    "description": "Scans target for vulnerabilities using custom engine",
    "inputSchema": {
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "Target URL or IP address"
            },
            "depth": {
                "type": "integer",
                "description": "Scan depth (1-5)",
                "default": 3
            }
        },
        "required": ["target"]
    }
}
```

---

## 🧪 Testes — Cobertura de Guerra

```bash
# Rodar tudo (79+ testes)
pytest tests/ -v

# Com coverage (intel completo)
pytest tests/ --cov=core --cov-report=term-missing

# Arquivo especifico (cirurgia)
pytest tests/test_translator.py -v

# Somente MCP tests
pytest tests/ -v -k "mcp"

# Parallel (mais rapido)
pytest tests/ -v -n auto
```

### Requisitos de Teste para PRs

| Tipo de PR        | Testes Requeridos                                   |
| ----------------- | --------------------------------------------------- |
| `feat` / `weapon` | Testes unitarios para CADA funcionalidade nova      |
| `fix`             | Teste de regressao provando que o bug nao volta     |
| `mcp`             | Integration test para tools/list e tools/call       |
| `refactor`        | Todos os testes existentes devem continuar passando |
| `docs`            | Nenhum (mas apreciado)                              |

---

## ✅ Checklist Final — Antes de Abrir o PR

```
  ╔═══════════════════════════════════════════════════════════════════╗
  ║                    PR SUBMISSION CHECKLIST                        ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  [ ] 🧪 pytest tests/ -v                    → ALL PASS           ║
  ║  [ ] ⚙️ python core/config_schema.py         → VALID             ║
  ║  [ ] 🏥 python core/doctor.py                → NO FAILURES       ║
  ║  [ ] 🔍 ruff check core/                    → NO ERRORS          ║
  ║  [ ] 🔒 Sem secrets/credenciais no codigo                       ║
  ║  [ ] 📖 Documentacao atualizada (se aplicavel)                   ║
  ║  [ ] 📋 CHANGELOG.md atualizado                                 ║
  ║  [ ] 🔢 Contadores atualizados (servers/tools/tasks)            ║
  ║  [ ] 🎯 MITRE mapping incluido (se aplicavel)                   ║
  ║  [ ] 💬 Commits com mensagens descritivas                       ║
  ║                                                                   ║
  ╚═══════════════════════════════════════════════════════════════════╝
```

---

## 🔒 Seguranca

Se encontrar uma vulnerabilidade, **NAO abra uma issue publica**.
Consulte [SECURITY.md](SECURITY.md) para reportar responsavelmente.

---

> *"Cada PR que chega, o Leviathan fica mais forte. Cada bug fix, mais resiliente. Cada MCP server, mais perigoso. Cada arma nova, mais profundo no abismo. A evolucao e inevitavel."*
