# LEVIATHAN VS

```
    ██╗     ███████╗██╗   ██╗██╗ █████╗ ████████╗██╗  ██╗ █████╗ ███╗   ██╗
    ██║     ██╔════╝██║   ██║██║██╔══██╗╚══██╔══╝██║  ██║██╔══██╗████╗  ██║
    ██║     █████╗  ██║   ██║██║███████║   ██║   ███████║███████║██╔██╗ ██║
    ██║     ██╔══╝  ╚██╗ ██╔╝██║██╔══██║   ██║   ██╔══██║██╔══██║██║╚██╗██║
    ███████╗███████╗ ╚████╔╝ ██║██║  ██║   ██║   ██║  ██║██║  ██║██║ ╚████║
    ╚══════╝╚══════╝  ╚═══╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
```

## Ambiente Ofensivo Integrado para VS Code

Configuracao completa do VS Code voltada para seguranca ofensiva e engenharia reversa. Integra 49 servidores MCP com 704+ ferramentas acessiveis via GitHub Copilot, motor de traducao semantica com 640+ regras, toolkit HTTP com analise automatizada, analise estatica para 10+ linguagens, controle de 4 emuladores Android e 160+ extensoes pre-configuradas.

![Versao](https://img.shields.io/badge/versao-16.0.0-0d1117?style=for-the-badge&labelColor=161b22)
![Python](https://img.shields.io/badge/python-3.14-1f6feb?style=for-the-badge&labelColor=0d1117)
![Licenca](https://img.shields.io/badge/licenca-MIT-238636?style=for-the-badge&labelColor=0d1117)
![Extensoes](https://img.shields.io/badge/extensoes-160+-8957e5?style=for-the-badge&labelColor=0d1117)
![Regras](https://img.shields.io/badge/regras_traducao-640+-f85149?style=for-the-badge&labelColor=0d1117)
![Ferramentas MCP](https://img.shields.io/badge/ferramentas_MCP-704+-ff6600?style=for-the-badge&labelColor=0d1117)
![Tarefas](https://img.shields.io/badge/tarefas_VS_Code-180+-00ccff?style=for-the-badge&labelColor=0d1117)
![IA](https://img.shields.io/badge/IA_cognitiva-max-cc00ff?style=for-the-badge&labelColor=0d1117)

---

## Arquitetura

| Componente              | Descricao                                                                    |
| ----------------------- | ---------------------------------------------------------------------------- |
| **Traducao Semantica**  | Motor com 640+ regras que sanitiza termos sensiveis para evitar filtros de IA |
| **HTTP Toolkit**        | Interceptador HTTP com rotacao de User-Agent, analise e geracao de cURL      |
| **Analise Estatica**    | Linters e scanners para 10+ linguagens integrados no editor                  |
| **Protocolo MCP**       | 49 servidores JSON-RPC 2.0 / 704+ ferramentas para GitHub Copilot           |
| **Modulo ADB**          | 42 ferramentas Android Debug Bridge                                          |
| **Modulo Frida**        | 28 instrumentacao dinamica + 89 no LDPlayer composto                         |
| **Modulo Ghidra**       | 15 ferramentas de analise binaria headless                                   |
| **Modulo Radare2**      | 16 ferramentas de analise binaria e engenharia reversa                       |
| **Modulo JADX**         | 16 ferramentas de decompilacao APK                                           |
| **Modulo APKTool**      | 12 ferramentas de decode/rebuild/sign APK                                    |
| **Modulo Androguard**   | 15 ferramentas de analise estatica Python de APK                             |
| **Modulo Wireshark**    | 23 ferramentas de captura e analise de rede                                  |
| **Modulo MITMProxy**    | 14 ferramentas de interceptacao e modificacao HTTPS                          |
| **Modulo Scapy**        | 15 ferramentas de crafting de pacotes, scan e fuzzing                        |
| **Emuladores**          | LDPlayer (89) + BlueStacks (17) + MEmu (19) + Nox (22) ferramentas          |
| **Modulo Burp Suite**   | 15 ferramentas de testes de seguranca web                                    |
| **Modulo Nuclei**       | 17 scanners de vuln (nuclei + sqlmap + nmap + ffuf)                          |
| **Modulo Objection**    | 20 ferramentas de exploracao mobile runtime                                  |
| **Modulo Hashcat**      | 12 ferramentas de cracking de senhas e analise de hash                       |
| **Modulo Recon**        | 14 ferramentas de reconhecimento (amass, gobuster, masscan)                  |
| **Modulo Exploit**      | 14 ferramentas de exploracao (searchsploit, msfvenom, hydra, john)           |
| **Modulo OSINT**        | 14 ferramentas OSINT (shodan, sherlock, maigret, dnstwist)                   |
| **Modulo Forense**      | 14 ferramentas de forense digital (volatility3, yara, binwalk, capa)         |
| **Modulo WebApp**       | 14 ferramentas de seguranca web (xsstrike, wfuzz, arjun, dalfox)             |
| **Modulo Cloud**        | 14 ferramentas cloud/supply chain (trivy, gitleaks, semgrep, prowler)        |
| **Modulo Wireless**     | 16 ferramentas wireless/RF/BLE (aircrack-ng, wifite, reaver, kismet)         |
| **Modulo AD**           | 18 ferramentas AD/Kerberos (bloodhound, impacket, netexec, mimikatz)         |
| **Modulo Stego**        | 14 ferramentas de esteganografia (steghide, zsteg, openstego)                |
| **Modulo Social Eng**   | 14 ferramentas de engenharia social (setoolkit, gophish, evilginx2)          |
| **Modulo NetAttack**    | 16 ferramentas de ataque de rede/MITM (bettercap, ettercap, hping3)          |
| **Modulo Adv Recon**    | 16 ferramentas de recon avancado (rustscan, feroxbuster, katana, wpscan)     |
| **Modulo Exploit Dev**  | 16 ferramentas de dev de exploits (pwntools, angr, checksec, ROPgadget)      |
| **Modulo Red Team**     | 16 ferramentas C2/payload (sliver, mythic, empire, havoc, donut)             |
| **Modulo Wordlist**     | 16 ferramentas de wordlist/senhas (cewl, crunch, john, patator)              |
| **Modulo RevEng**       | 16 ferramentas de engenharia reversa (objdump, binwalk, yara, capa)          |

---

## Instalacao

### Windows

```batch
INSTALL.bat
```

### PowerShell

```powershell
.\install.ps1
```

O instalador:
- Detecta e instala Python, Git, VS Code se necessario
- Instala todas as extensoes configuradas
- Configura os 49 servidores MCP para GitHub Copilot
- Abre o VS Code com o ambiente pronto

### CLI Interativo — Seletor de MCPs

```batch
python core\mcp_launcher.py
```

Terminal colorido com os 49 servidores organizados em 13 categorias. Selecione uma categoria para ver as ferramentas e copiar o prompt de contexto para o Copilot.

---

## Motor de Traducao Semantica

Converte termos de seguranca ofensiva em sinonimos neutros para evitar filtros de conteudo em assistentes de IA:

| Termo Original | Termo Sanitizado |
| -------------- | ---------------- |
| exploit        | pressure_point   |
| vulnerability  | hull_breach      |
| bypass         | current_redirect |
| injection      | ink_injection    |
| reverse_shell  | sonar_callback   |
| payload        | depth_charge     |
| backdoor       | sea_gate         |
| rootkit        | barnacle_cluster |
| keylogger      | echo_recorder    |
| botnet         | shoal_network    |

640+ regras mapeadas em `core/config.json`. Funciona via CLI (`python core/translator.py encode`) ou via MCP server integrado ao Copilot.

---

## HTTP Toolkit

```bash
# Requisicao com rotacao de headers
python core/http_toolkit.py dispatch https://api.example.com

# Scan automatizado
python core/http_toolkit.py scan https://api.example.com

# Modo interativo
python core/http_toolkit.py interactive
```

- Rotacao automatica de User-Agent e headers
- Analise de resposta com classificacao automatica
- Retry automatico em erros 403/401 com headers alternativos
- Geracao de comandos cURL equivalentes

---

## Analise Estatica

| Linguagem             | Ferramentas                          |
| --------------------- | ------------------------------------ |
| Python                | Pylance, Pylint, Bandit, Mypy, Radon |
| Go                    | golangci-lint, Staticcheck, GoSec    |
| JavaScript/TypeScript | ESLint, Prettier, SonarLint          |
| Rust                  | rust-analyzer, Clippy                |
| C/C++                 | Clang-Tidy, Cppcheck                 |
| Java                  | Checkstyle, PMD, SpotBugs            |
| Shell                 | ShellCheck                           |
| Docker                | Hadolint                             |
| Terraform             | TFLint, Checkov                      |
| SQL                   | SQLFluff                             |

---

## Estrutura do Projeto

```
Leviathan-VS/
    .github/
        copilot-instructions.md  # Instrucoes cognitivas para IA (842 linhas)
    .vscode/
        extensions.json    # 160+ extensoes configuradas
        settings.json      # Configuracao completa do editor
        tasks.json         # 180+ tarefas automatizadas
        launch.json        # Configuracoes de debug
        mcp.json           # 49 servidores MCP / 704+ ferramentas
        keybindings.json   # Atalhos customizados
    core/
        config.json        # 640+ regras de traducao semantica
        translator.py      # Motor de traducao
        http_toolkit.py    # HTTP Toolkit com analise
        mcp_server.py      # Servidor MCP principal
        mcp_launcher.py    # CLI interativo — seletor de MCPs
        adb/               # ADB MCP (42 ferramentas)
        frida_mcp/         # Frida MCP (28 ferramentas)
        ghidra/            # Ghidra Headless MCP (15 ferramentas)
        r2/                # Radare2 MCP (16 ferramentas)
        jadx/              # JADX Decompiler MCP (16 ferramentas)
        apktool/           # APKTool MCP (12 ferramentas)
        androguard/        # Androguard MCP (15 ferramentas)
        ldplayer/          # LDPlayer MCP (89 ferramentas)
        bluestacks/        # BlueStacks MCP (17 ferramentas)
        memu/              # MEmu MCP (19 ferramentas)
        nox/               # NoxPlayer MCP (22 ferramentas)
        wireshark/         # Wireshark MCP (23 ferramentas)
        mitmproxy/         # MITMProxy MCP (14 ferramentas)
        scapy/             # Scapy MCP (15 ferramentas)
        burpsuite/         # Burp Suite MCP (15 ferramentas)
        nuclei/            # Nuclei + SQLMap + Nmap MCP (17 ferramentas)
        objection/         # Objection MCP (20 ferramentas)
        hashcat/           # Hashcat + John MCP (12 ferramentas)
        recon/             # Recon MCP (14 ferramentas)
        exploit/           # Exploit MCP (14 ferramentas)
        osint/             # OSINT MCP (14 ferramentas)
        forensics/         # Forense MCP (14 ferramentas)
        webapp/            # WebApp MCP (14 ferramentas)
        cloud/             # Cloud MCP (14 ferramentas)
        wireless/          # Wireless MCP (16 ferramentas)
        active_directory/  # AD MCP (18 ferramentas)
        stego/             # Stego MCP (14 ferramentas)
        social_eng/        # Social Eng MCP (14 ferramentas)
        netattack/         # NetAttack MCP (16 ferramentas)
        adv_recon/         # Adv Recon MCP (16 ferramentas)
        exploit_dev/       # Exploit Dev MCP (16 ferramentas)
        redteam/           # Red Team MCP (16 ferramentas)
        wordlist/          # Wordlist MCP (16 ferramentas)
        reveng/            # RevEng MCP (16 ferramentas)
    tests/                 # 79 testes unitarios
    docs/                  # Documentacao
```

---

## Tarefas (180+)

Acessiveis via `Ctrl+Shift+P` > `Tasks: Run Task`

### Traducao Semantica

| Tarefa                        | Descricao                             |
| ----------------------------- | ------------------------------------- |
| `[LEVIATHAN] ENCODE`          | Sanitizar termos sensiveis no arquivo |
| `[LEVIATHAN] RESTORE`         | Restaurar termos originais            |
| `[LEVIATHAN] PREVIEW`         | Preview sem alterar arquivo           |
| `[LEVIATHAN] CHECK`           | Verificar termos sensiveis restantes  |
| `[LEVIATHAN] INTERACTIVE`     | Console interativo de traducao        |
| `[LEVIATHAN] FULL CYCLE`      | Encode + copiar para clipboard        |
| `[LEVIATHAN] OBFUSCATE`       | Ofuscar nomes de variaveis            |
| `[LEVIATHAN] DEOBFUSCATE`     | Restaurar nomes de variaveis          |
| `[LEVIATHAN] FULL TRANSFORM`  | Encode + ofuscacao combinados         |
| `[LEVIATHAN] Status Completo` | Healthcheck de todas as ferramentas   |

### ADB — Android Debug Bridge (16 tarefas)

| Tarefa                         | Descricao                                   |
| ------------------------------ | ------------------------------------------- |
| `[ADB] Listar Dispositivos`    | Listar dispositivos conectados com detalhes |
| `[ADB] Shell Interativo`       | Shell interativo no device                  |
| `[ADB] Instalar APK`           | Instalar APK com reinstall + permissoes     |
| `[ADB] Extrair APK de App`     | Extrair APK instalado do device             |
| `[ADB] Screenshot`             | Capturar screenshot                         |
| `[ADB] Listar Apps Instalados` | Listar apps de terceiros                    |
| `[ADB] Logcat Filtrado`        | Logcat filtrado por pacote                  |
| `[ADB] Force Stop App`         | Forcar parada da aplicacao                  |
| `[ADB] Limpar Dados do App`    | Limpar dados e cache                        |
| `[ADB] Configurar Proxy`       | Definir proxy HTTP no device                |
| `[ADB] Remover Proxy`          | Remover proxy HTTP                          |
| `[ADB] Port Forward`           | Forward portas Frida (27042/27043)          |
| `[ADB] Info do Dispositivo`    | Info do device (modelo, RAM, storage)       |
| `[ADB] Gravar Tela`            | Gravar tela por 30 segundos                 |
| `[ADB] TCP Dump`               | Captura de trafego com tcpdump              |
| `[ADB] Conectar WiFi`          | ADB wireless                                |

### Frida — Instrumentacao Dinamica (14 tarefas)

| Tarefa                              | Descricao                                        |
| ----------------------------------- | ------------------------------------------------ |
| `[FRIDA] Setup Server no Device`    | Download e start do frida-server                 |
| `[FRIDA] Listar Processos`          | Listar processos via USB                         |
| `[FRIDA] Listar Apps`               | Listar apps instalados                           |
| `[FRIDA] Bypass SSL Pinning`        | Spawn com bypass SSL (21 camadas)                |
| `[FRIDA] Bypass Root Detection`     | Spawn com bypass de root detection               |
| `[FRIDA] Bypass Emulator Detection` | Spawn com bypass de emulator detection            |
| `[FRIDA] Bypass ALL (Nuclear)`      | Spawn com todos os bypasses combinados           |
| `[FRIDA] Interceptar Crypto`        | Hook em Cipher, Mac, MessageDigest, Keys         |
| `[FRIDA] Interceptar Rede`          | Hook em send/recv/HTTP/OkHttp                    |
| `[FRIDA] Game Inspector`            | Hooks para Unity/Cocos2d                         |
| `[FRIDA] Dump Classes Java`         | Listar classes Java carregadas                   |
| `[FRIDA] Hook Metodo Java`          | Hook metodo com log de args e retorno            |
| `[FRIDA] Trace com frida-trace`     | Auto-trace de chamadas                           |
| `[FRIDA] Attach a App Rodando`      | Attach em app rodando (REPL)                     |

### Seletor Interativo de MCPs

```bash
python core\mcp_launcher.py
```

Menu interativo com os **49 servidores MCP** em 13 categorias: Mobile, Emuladores, Analise Binaria, Rede, Web, Recon, Exploit, Red Team, Wireless, AD, Forense, Cloud, Core.

---

## Regras de Traducao (640+)

Organizadas por dominio:

- **Ofensivo** — exploit, bypass, vulnerability, privilege escalation
- **Malware** — virus, trojan, backdoor, rootkit, ransomware
- **Web** — XSS, CSRF, SQL injection, SSRF, RCE
- **C2** — reverse shell, webshell, beacon, implant, callback
- **Recon** — scanner, fuzzer, sniffer, crawler, enumerator
- **Binario** — buffer overflow, ROP chain, shellcode, heap spray
- **Cloud** — S3 bucket exposure, IAM escalation, SSRF to metadata
- **Evasao** — obfuscation, packing, anti-debug, anti-VM
- **Ferramentas** — Metasploit, Burp Suite, Nmap, Hashcat, Cobalt Strike

---

## Servidores MCP — 49 Servers / 704+ Ferramentas

Todos os servidores seguem o protocolo JSON-RPC 2.0 sobre stdio com framing Content-Length. Configurados em `.vscode/mcp.json` e acessiveis automaticamente pelo GitHub Copilot.

### Categorias

| Categoria          | Servers                                    | Ferramentas |
| ------------------ | ------------------------------------------ | ----------- |
| Analise Mobile     | ADB, Frida, Objection, JADX, Androguard, APKTool | 133    |
| Emuladores         | LDPlayer, BlueStacks, MEmu, Nox           | 147         |
| Analise Binaria    | Ghidra, Radare2, RevEng                    | 47          |
| Rede & Trafego     | Wireshark, MITMProxy, Scapy, NetAttack    | 68          |
| Seguranca Web      | Nuclei, Burp Suite, WebApp                 | 46          |
| Reconhecimento     | Recon, Adv Recon, OSINT                    | 44          |
| Exploracao         | Exploit, Exploit Dev, Hashcat, Wordlist    | 58          |
| Red Team & C2      | Red Team, Social Eng                       | 30          |
| Wireless & RF      | Wireless                                   | 16          |
| Active Directory   | Active Directory                           | 18          |
| Forense & IR       | Forensics, Stego                           | 28          |
| Cloud              | Cloud                                      | 14          |
| Core               | Leviathan                                  | 7           |

Execute `[LEVIATHAN] Status Completo` para healthcheck de todos os servidores.

---

## Configuracao do Editor

- **Tema**: Dark com highlights customizados
- **Fonte**: Cascadia Code com ligaduras
- **Auto-save**: 1s delay
- **Type Checking**: Standard
- **Format on Save**: Habilitado para todas as linguagens
- **Git**: Auto-fetch habilitado

---

## Extensoes (160+)

### Linguagens & Linters
- Python, Pylance, Go, Rust Analyzer
- ESLint, Prettier, EditorConfig

### IA & Assistentes
- GitHub Copilot, Cline, Claude Code

### Seguranca
- SonarQube, Snyk, SARIF Viewer

### Frontend
- Tailwind CSS, Vue, React, Angular
- Figma, Storybook

### Produtividade
- GitLens, Todo Tree, Project Manager
- REST Client, Thunder Client

---

## Requisitos

- Python 3.14+
- VS Code 1.80+
- Git

---

## Quick Start

```bash
git clone https://github.com/ThiagoFrag/Leviathan-VS.git
cd Leviathan-VS
code .
```

Verificar ambiente: `[LEVIATHAN] Status Completo`
Seletor de MCPs: `python core\mcp_launcher.py`

---

## Contribuicao

1. Fork o repositorio
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit (`git commit -m 'feat(modulo): descricao'`)
4. Push (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## Licenca

MIT

---

## Autor

**ThiagoFrag** — [@ThiagoFrag](https://github.com/ThiagoFrag)
