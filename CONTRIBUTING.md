# ☠️ Contributing to Leviathan-VS

```
"Cada contribuicao e um tentaculo a mais no monstro."
```

Obrigado por querer fortalecer o arsenal. Siga as diretrizes abaixo para garantir que sua contribuicao seja digna do abismo.

## ⚡ Quick Start para Desenvolvimento

```bash
# Clone o monstro
git clone https://github.com/ThiagoFrag/Leviathan-VS.git
cd Leviathan-VS

# Instale dependencias de dev (ambiente de guerra)
pip install -e ".[dev]"

# Rode os testes (79+ testes devem passar)
pytest tests/ -v

# Diagnostico de profundidade
python core/doctor.py

# Validar configs de guerra
python core/config_schema.py

# Lint (qualidade militar)
ruff check core/
```

## 📋 Estrutura de PRs

| Regra           | Descricao                                                    |
| --------------- | ------------------------------------------------------------ |
| 🎯 **Foco**      | PRs pequenos e focados (1 feature ou 1 fix por PR)           |
| 📝 **Titulo**    | `[AREA] Descricao` (ex: `[KRAKEN] Add 50 new evasion rules`) |
| 🧪 **Testes**    | Inclua testes para funcionalidade nova                       |
| ✅ **Validacao** | Rode `pytest` e `config_schema.py` antes de abrir PR         |

## 🎨 Padrao de Codigo

- **Python 3.9+** (compativel com 3.9 a 3.14)
- **UTF-8** sem BOM em todos os arquivos
- **Docstrings** para classes e funcoes publicas
- **ruff** para lint (config em `pyproject.toml`)
- Sem output colorido quando `--json` flag presente
- Nomes de variaveis em ingles, mensagens podem ser em portugues

## 🧠 Padrao de MCP Servers

Novos MCP servers devem seguir o protocolo:

1. Criar `core/<nome>/mcp_mcp_<nome>.py` — o servidor
2. Criar `core/<nome>/__init__.py` — o pacote
3. Registrar em `.vscode/mcp.json` — ativar no Copilot
4. Documentar em `copilot-instructions.md` — instrucoes cognitivas
5. Adicionar tasks em `tasks.json` (minimo 2)
6. Atualizar contadores no README (servers, tools)

## 🧪 Testes

```bash
# Rodar tudo (modo guerra)
pytest tests/ -v

# Com coverage (intel completo)
pytest tests/ --cov=core --cov-report=term-missing

# Arquivo especifico (cirurgia)
pytest tests/test_translator.py -v
```

## ✅ Checklist para PRs

- [ ] 🧪 Testes passam (`pytest`)
- [ ] ⚙️ Configs validos (`python core/config_schema.py`)
- [ ] 🏥 Doctor OK (`python core/doctor.py`)
- [ ] 🔒 Sem secrets ou dados pessoais no codigo
- [ ] 📖 Documentacao atualizada se necessario
- [ ] 📋 CHANGELOG.md atualizado
- [ ] 🔢 Contadores atualizados (servers, tools, tasks)

## 🔒 Seguranca

Se encontrar uma vulnerabilidade, **NAO abra uma issue publica**.
Consulte [SECURITY.md](SECURITY.md) para reportar responsavelmente.

---

> *"Cada PR que chega, o Leviathan fica mais forte. Cada bug fix, mais resiliente. Cada feature, mais perigoso."*
