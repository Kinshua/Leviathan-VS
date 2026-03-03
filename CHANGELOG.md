# ☠️ Changelog — Leviathan VS

> Cada versao e uma profundidade a mais no abismo.
> Format based on [Keep a Changelog](https://keepachangelog.com/).

---

## [66.6.0] ABYSSAL SOVEREIGN — 2026-03-02

### ☠️ THE GREAT TRANSFORMATION — O Monstro Renasceu

Esta versao reescreve **o projeto inteiro** com uma identidade surreal de pentester nivel militar.

### Added
- **ABYSS COLOR ENGINE** (`core/colors.py`) — Paleta abissal completa com:
  - 40+ cores ANSI (256 + true color 24-bit)
  - Motor de gradientes com 8 paletas (fire, ocean, toxic, blood, phantom, matrix, skull, abyss)
  - Efeito typewriter para dramaturgia terminal
  - Banners ASCII art gigantes com skull art
  - Threat gauge animado com blink OMEGA
  - Separadores e headers de secao estilizados
- **Boot Sequence** no CLI — animacao dramatica de inicializacao
- **Version manifest completo** — codename, threat level, depth
- **Threat Level OMEGA** — indicador visual de periculosidade
- Skull ASCII art no modulo de cores
- Comprehensive `__init__.py` com docstring abissal

### Changed
- **Version**: 16.0.0 → **66.6.0 ABYSSAL SOVEREIGN**
- **README.md** — Reescrito COMPLETAMENTE:
  - Banner ASCII art gigante com moldura
  - Diagrama de arquitetura neural em ASCII
  - 15 dominios de ataque tabelados com codinomes e icones
  - Estrutura hierarquica com emojis por dominio
  - 10 badges customizados com cores vibrantes
  - Aviso de profundidade extrema
  - Tabelas de MCP servers com codinomes de guerra
  - Secao de tarefas expandida com categorias
  - Secao de Quick Start dramatica
  - Footer com citacao abissal
- **LEVIATHAN.bat** — Redesenhado:
  - Banner com cores ANSI 256 (vermelho sangue)
  - Threat gauge OMEGA com blink
  - Menu com emojis e descricoes dramaticas
  - 10 opcoes (adicionado Doctor)
  - Mensagem de saida filosofica
- **INSTALL.bat** — Redesenhado:
  - Banner Leviathan em vez de "Hand of God"
  - Cores vermelho sangue
  - Estatisticas do arsenal (49 MCPs, 704+ tools, etc.)
  - Final section com instrucoes estilizadas
- **install.ps1** — Redesenhado:
  - Banner Leviathan com cores ANSI
  - Synopsis e description atualizados
  - Final colorido com instrucoes de guerra
- **pyproject.toml**:
  - Version 66.6.0
  - Description abissal com emoji skull
  - 20 keywords de seguranca ofensiva
  - Status mudou para "Production/Stable"
  - Adicionado Python 3.14 nos classifiers
  - Email de autor abissal
- **SECURITY.md** — Reescrito com:
  - Citacao dramatica
  - Tabelas de SAFE_MODE
  - Tabelas de escopo com emojis
  - Versoes suportadas expandidas com niveis de suporte
- **CONTRIBUTING.md** — Reescrito com:
  - Citacoes tematicas
  - Tabelas de regras
  - Checklist expandido
  - Citacao final motivacional
- **core/cli.py**:
  - Docstring dramatica com citacao
  - Import de banners, gradientes e efeitos
  - Comando `version` mostra banner + threat gauge + stats completos + JSON mode
  - Boot sequence com 5 estagios animados
  - Mini banner em todos os comandos
  - Description e epilog tematicos no argparse
- **core/__version__.py** — Adicionado codename, threat_level, depth
- **core/__init__.py** — Docstring expandida com stats e citacao
- **core/colors.py** — Reescrito de 50 para 200+ linhas
- **CHANGELOG.md** — Este mega changelog
- **core/doctor.py** — Headers e banners dramaticos
- **core/mcp_server.py** — Docstring e identidade atualizados
- **core/mcp_launcher.py** — Identidade visual atualizada
- **docs/** — Documentacao atualizada
- **.github/copilot-instructions.md** — Identidade OMEGA

## [16.0.0] - 2026-02-27

### Added
- **10 new MCP servers** — 160 new tools across 10 security categories:
  - `core/wireless/mcp_wireless.py` — 16 Wireless/RF/Bluetooth tools (aircrack-ng suite, wifite, reaver, wash, bully, bettercap wifi/ble, kismet, cowpatty, wifipumpkin3, airgeddon)
  - `core/active_directory/mcp_ad.py` — 18 Active Directory/Kerberos tools (bloodhound, impacket suite x8, netexec smb/ldap/winrm, evil-winrm, mimikatz, rubeus, bloodyAD, certipy)
  - `core/stego/mcp_stego.py` — 14 Steganography tools (steghide, zsteg, openstego, outguess, snow, stegseek, stegcracker, exiftool)
  - `core/social_eng/mcp_social_eng.py` — 14 Social Engineering tools (setoolkit, gophish, evilginx2, beef-xss, modlishka, wifiphisher, blackeye, zphisher)
  - `core/netattack/mcp_netattack.py` — 16 Network Attack/MITM tools (bettercap, ettercap, hping3, arp-scan, netdiscover, mitm6, sslscan, tcpdump, socat, snort, dnschef, sslstrip)
  - `core/adv_recon/mcp_adv_recon.py` — 16 Advanced Recon tools (rustscan, autorecon, feroxbuster, dirsearch, katana, wpscan, eyewitness, sublist3r, wapiti, httprobe, hakrawler, gau, waybackurls, unfurl, meg)
  - `core/exploit_dev/mcp_exploit_dev.py` — 16 Exploit Development tools (gdb, pwntools, angr, checksec, ROPgadget, one_gadget, msf-pattern, spike, boofuzz, afl, radamsa, ropper, patchelf, msfvenom, shellcraft)
  - `core/redteam/mcp_redteam.py` — 16 Red Team/C2 tools (sliver, mythic, empire, havoc, covenant, armitage, macro_pack, donut, scarecrow, shellter, veil, nim payloads)
  - `core/wordlist/mcp_wordlist.py` — 16 Wordlist/Password tools (cewl, crunch, cupp, hash-identifier, hashid, ophcrack, patator, mentalist, kwprocessor, princeprocessor, john, wordlistctl, username-anarchy, rsmangler)
  - `core/reveng/mcp_reveng.py` — 16 Reverse Engineering tools (objdump, readelf, ltrace, strace, dex2jar, pefile, oletools, upx, detect-it-easy, binwalk, yara, capa, strings, file, xxd, nm)
- 25+ new VS Code tasks for all 10 new MCP categories
- All 10 servers registered in `.vscode/mcp.json` with proper `cwd` and `-m` module paths
- `__init__.py` for all 10 new packages
- Deep research integration from hexstrike-ai (150+ tools reference), Kali Linux tools database, and GitHub security MCP ecosystem

### Changed
- Version bump 15.5.0 → 16.0.0
- MCP server count 39 → 49, tool count 544+ → 704+
- Project now integrates tools from: aircrack-ng, impacket, BloodHound, Metasploit, Sliver C2, Mythic, Empire, Havoc, angr, pwntools, AFL, YARA, capa, and 100+ more
- `.vscode/tasks.json` expanded with tasks for wireless, AD, stego, social eng, netattack, adv recon, exploit dev, redteam, wordlist, and reverse engineering

## [15.5.0] - 2026-02-26

### Added
- **6 new MCP servers** — 84 new tools across 6 security categories:
  - `core/recon/mcp_recon.py` — 14 reconnaissance tools (amass, gobuster, masscan, whatweb, dnsrecon, wafw00f, fierce, theHarvester, assetfinder)
  - `core/exploit/mcp_exploit.py` — 14 exploitation tools (searchsploit, msfvenom, msfconsole, hydra, john, medusa, responder, enum4linux)
  - `core/osint/mcp_osint.py` — 14 OSINT tools (shodan, maigret, sherlock, holehe, dnstwist, recon-ng, spiderfoot, phoneinfoga, ghunt)
  - `core/forensics/mcp_forensics.py` — 14 forensics tools (volatility3, yara, binwalk, capa, foremost, bulk_extractor, exiftool, strings)
  - `core/webapp/mcp_webapp.py` — 14 web app security tools (xsstrike, wfuzz, arjun, gospider, commix, dalfox, jwt_tool, nosqlmap, ssrfmap, crlfuzz)
  - `core/cloud/mcp_cloud.py` — 14 cloud security tools (trivy, gitleaks, trufflehog, semgrep, checkov, prowler, kube-hunter, grype, syft)
- 17 new VS Code tasks for new MCP categories (recon, exploit, osint, forensics, webapp, cloud)
- All 6 servers registered in `.vscode/mcp.json` with proper `cwd` and `-m` module paths
- `__init__.py` for all 6 new packages

### Changed
- Version bump 14.2.0 → 15.5.0
- MCP server count 33 → 39, tool count 460+ → 544+
- README.md badges and module table updated
- `.vscode/mcp.json` header updated
- `.github/copilot-instructions.md` identity and tool chains updated

## [14.2.0] - 2026-02-25

### Added
- `core/cache.py` — SQLite-backed result cache (put/get/list/purge/stats/TTL)
- `core/generate_tasks_md.py` — auto-generates `docs/TASKS.md` from `.vscode/tasks.json`
- `docs/TASKS.md` — 138 tasks across 20+ categories, auto-generated
- `.pre-commit-config.yaml` — ruff lint/format + pre-commit hooks (trailing whitespace, YAML, merge conflicts)
- `tests/test_http_and_cache.py` — 30 unit tests for ResultCache, HTTPToolkit classes, and TASKS.md generator
- `http_toolkit.py`: `SessionManager` class — persists cookies/tokens across requests
- `http_toolkit.py`: `dispatch_json()` — returns JSON-serializable `dict` for automation
- `http_toolkit.py`: `profile_endpoint()` — timing/status distribution analysis over N rounds
- `http_toolkit.py`: `--json` flag on both `dispatch` and `scan` subcommands
- CI: `secrets-scan` job using gitleaks
- CI: dedicated `json-validate` job via `config_schema.py`
- CI: `fail-fast: false` in test matrix for better feedback

### Changed
- `http_toolkit.py`: dispatch retry now uses exponential backoff (`0.5 * 2^attempt`, capped at 30s)
- `http_toolkit.py`: session cookies injected automatically (opt-out via `session=False`)
- `http_toolkit.py`: response cookies persisted to `.http_session.json`
- CI: removed flaky inline JSON validation in favor of `config_schema.py`
- Version bump 14.1.0 → 14.2.0

## [14.1.0] - 2026-02-25

### Added
- `core/doctor.py` — healthcheck & diagnostics (`python core/doctor.py`, `--json`, `--fix`)
- `core/config_schema.py` — config validation for config.json, mcp.json, tasks.json
- `core/cli.py` — unified CLI entrypoint (`leviathan translate|http|doctor|validate|report|version`)
- `pyproject.toml` — package manifest with `[project.scripts]`, ruff/pytest config
- `tests/test_translator.py` — 25+ unit tests for Kraken Engine (roundtrip, case, format, edge cases)
- `.github/workflows/ci.yml` — GitHub Actions: lint, test (Windows+Ubuntu matrix), JSON validation
- `CONTRIBUTING.md` — contributor guide
- `SECURITY.md` — security policy + responsible use + SAFE_MODE docs
- `CHANGELOG.md` — this file
- VS Code tasks: `[LEVIATHAN] Doctor`, `[LEVIATHAN] Validate Configs`, `[LEVIATHAN] Run Tests`, `[LEVIATHAN] Lint`, `[LEVIATHAN] Export Report`
- `SAFE_MODE` environment variable (default=1): excludes DELETE from scans, defensive defaults

### Fixed
- **http_toolkit.py**: 6 bare `except:` clauses → specific exception types (prevents swallowing KeyboardInterrupt/SystemExit)
- **http_toolkit.py**: `os.system('')` called on every `colorize()` → called once at import
- **http_toolkit.py**: `scan()` sends DELETE by default → excluded in SAFE_MODE
- **http_toolkit.py**: `scan()` delay now configurable (`delay` parameter)
- **install.ps1**: validation checks wrong paths (`$scriptPath\translator.py` → `$scriptPath\core\translator.py`)
- **install.ps1**: MCP server path missing `core/` prefix
- **install.ps1**: `$ErrorActionPreference = "SilentlyContinue"` → `"Continue"` (don't suppress errors)

### Changed
- `scan()` method signature: added `delay` and `methods` parameters (backward-compatible defaults)

## [14.0.0] - 2026-02-24

### Added
- 6 new MCP servers: Scapy (15 tools), Radare2 (16 tools), Hashcat (12 tools), APKTool (12 tools), Androguard (15 tools), MITMProxy (14 tools)
- 3 missing MCP servers registered in mcp.json (mitmproxy, apktool, androguard)
- Tasks for new MCPs in tasks.json

### Fixed
- **mcp_frida.py**: 8 calls to undefined `_run_frida_cli` → `_run_frida_cmd`
- **mcp_frida.py**: broken tuple unpacking from `_build_inject_cmd`
- **mcp_frida.py**: missing tmpfile cleanup in 6 handlers
