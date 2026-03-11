<div align="center">

# Leviathan VS

### Offensive Security Platform for VS Code

<br>

![Version](https://img.shields.io/badge/version-70.0.0-blue?style=flat-square)
![Python](https://img.shields.io/badge/python-3.9+-3776ab?style=flat-square&logo=python&logoColor=white)
![MCP Servers](https://img.shields.io/badge/MCP_servers-40-orange?style=flat-square)
![Tools](https://img.shields.io/badge/tools-752+-green?style=flat-square)
![MITRE](https://img.shields.io/badge/MITRE_ATT%26CK-14%2F14_tactics-red?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

**40 MCP servers** · **752+ security tools** · **17 attack domains** · **640+ evasion rules** · **14/14 MITRE ATT&CK tactics**

A comprehensive offensive security platform that integrates 40 MCP (Model Context Protocol) servers into VS Code via GitHub Copilot, providing unified access to 752+ penetration testing tools across 17 specialized domains.

[Getting Started](#getting-started) · [Architecture](#architecture) · [MCP Catalog](#mcp-server-catalog) · [CLI Reference](#cli) · [Contributing](#contributing)

</div>

---

## Overview

Leviathan VS transforms VS Code into a full-spectrum offensive security workstation. It leverages the **Model Context Protocol (MCP)** — JSON-RPC 2.0 over stdio — to expose security tools as structured, AI-accessible services through GitHub Copilot.

**Key capabilities:**

- **40 MCP servers** organized across 17 attack domains, from reconnaissance to post-exploitation
- **Intelligent launcher** with real-time tool availability detection (installed/missing status per server)
- **Kraken Engine** — 640+ semantic translation rules for evasion research
- **Shannon Engine** — Autonomous pentesting brain with Bayesian inference, vulnerability genetics, and exploit chain synthesis
- **Full MITRE ATT&CK coverage** — all 14 tactics mapped to specific tools and techniques
- **Cross-platform diagnostics** — comprehensive healthcheck of 50+ external tools and environment configuration

---

## Getting Started

### Requirements

| Component | Version |
|-----------|---------|
| Python | 3.9+ (recommended 3.12+) |
| VS Code | 1.80+ |
| Git | Any |

### Installation

**Windows (one-click):**
```batch
INSTALL.bat
```

**PowerShell:**
```powershell
.\install.ps1            # Interactive installation
.\install.ps1 -Silent    # Unattended mode
```

The installer automatically detects and configures Python, Git, VS Code, dependencies, extensions, and all 40 MCP servers.

### Quick Start

```bash
git clone https://github.com/ThiagoFrag/Leviathan-VS.git
cd Leviathan-VS
code .
```

```bash
leviathan doctor          # Environment healthcheck
leviathan version         # Platform manifest
python core/mcp_launcher.py   # Interactive MCP selector
```

---

## Architecture

```
Leviathan-VS/
├── .vscode/
│   ├── mcp.json              # 40 MCP server configurations
│   ├── settings.json         # Editor security profile
│   ├── tasks.json            # Automated task definitions
│   └── extensions.json       # Required extensions
│
├── core/
│   ├── mcp_server.py         # Core MCP server (JSON-RPC 2.0)
│   ├── mcp_launcher.py       # Interactive MCP selector with tool status
│   ├── cli.py                # Unified CLI interface
│   ├── doctor.py             # Environment diagnostics (50+ tool checks)
│   ├── translator.py         # Kraken Engine — semantic translation
│   ├── http_toolkit.py       # HTTP testing toolkit
│   ├── config.json           # 640+ evasion translation rules
│   ├── colors.py             # Terminal visual engine
│   │
│   ├── shannon/              # Shannon Engine — autonomous pentesting AI
│   │   ├── bayesian_engine.py
│   │   ├── vuln_dna.py
│   │   ├── exploit_synthesis.py
│   │   ├── attack_persona.py
│   │   ├── knowledge_graph.py
│   │   └── ...               # 6-tier architecture (25+ modules)
│   │
│   ├── adb/                  # MCP: Android Debug Bridge (42 tools)
│   ├── frida_mcp/            # MCP: Frida instrumentation (28 tools)
│   ├── objection/            # MCP: Objection runtime (20 tools)
│   ├── jadx/                 # MCP: JADX decompiler (16 tools)
│   ├── androguard/           # MCP: Androguard analysis (15 tools)
│   ├── apktool/              # MCP: APKTool (12 tools)
│   ├── ldplayer/             # MCP: LDPlayer emulator (89 tools)
│   ├── bluestacks/           # MCP: BlueStacks (17 tools)
│   ├── memu/                 # MCP: MEmu Play (19 tools)
│   ├── nox/                  # MCP: NoxPlayer (22 tools)
│   ├── ghidra/               # MCP: Ghidra headless (15 tools)
│   ├── r2/                   # MCP: Radare2 (16 tools)
│   ├── reveng/               # MCP: Reverse engineering (16 tools)
│   ├── wireshark/            # MCP: Wireshark/tshark (23 tools)
│   ├── mitmproxy/            # MCP: MITM proxy (14 tools)
│   ├── scapy/                # MCP: Packet crafting (15 tools)
│   ├── netattack/            # MCP: Network attacks (16 tools)
│   ├── nuclei/               # MCP: Nuclei + SQLMap + Nmap (17 tools)
│   ├── burpsuite/            # MCP: Burp Suite API (15 tools)
│   ├── webapp/               # MCP: Web app security (14 tools)
│   ├── recon/                # MCP: Reconnaissance (14 tools)
│   ├── adv_recon/            # MCP: Advanced recon (16 tools)
│   ├── osint/                # MCP: OSINT (14 tools)
│   ├── exploit/              # MCP: Exploitation (14 tools)
│   ├── exploit_dev/          # MCP: Exploit development (16 tools)
│   ├── hashcat/              # MCP: Password cracking (12 tools)
│   ├── wordlist/             # MCP: Wordlist generation (16 tools)
│   ├── redteam/              # MCP: Red team & C2 (16 tools)
│   ├── social_eng/           # MCP: Social engineering (14 tools)
│   ├── wireless/             # MCP: Wireless & RF (16 tools)
│   ├── active_directory/     # MCP: Active Directory (18 tools)
│   ├── forensics/            # MCP: Digital forensics (14 tools)
│   ├── stego/                # MCP: Steganography (14 tools)
│   ├── cloud/                # MCP: Cloud security (14 tools)
│   ├── secrets/              # MCP: Secrets scanning (12 tools)
│   ├── container/            # MCP: Container & K8s security (14 tools)
│   ├── iac/                  # MCP: IaC scanning (12 tools)
│   └── tunneling/            # MCP: Tunneling & pivoting (14 tools)
│
├── tests/                    # Unit tests
├── INSTALL.bat               # Windows installer
└── install.ps1               # PowerShell installer
```

### Shannon Engine

The Shannon Engine (`core/shannon/`) is a 6-tier autonomous pentesting intelligence system:

| Tier | Name | Purpose |
|------|------|---------|
| 0 | **Cortex** | Bayesian inference, vulnerability DNA, exploit chain synthesis (A*), attack personas, knowledge graph |
| 1 | **Arsenal** | Protocol dissection, supply chain analysis, container security, GraphQL/WebSocket engines |
| 2 | **Intelligence** | Attack narratives, defensive mirroring, OSINT correlation, deep fingerprinting, CVE prediction |
| 3 | **Automation** | Campaign management, continuous monitoring, result correlation |
| 4 | **Output** | Compliance mapping (PCI-DSS, HIPAA, SOC2), risk scoring, remediation generation |
| 5 | **Meta** | Self-evolution via ELO rating, strategy database, performance profiling |

---

## MCP Server Catalog

All servers implement the MCP standard: JSON-RPC 2.0 over stdio with Content-Length framing. Configured in `.vscode/mcp.json` and accessible through GitHub Copilot.

| # | Domain | Servers | Tools | Description |
|:-:|--------|---------|:-----:|-------------|
| 1 | **Mobile Analysis** | ADB, Frida, Objection, JADX, Androguard, APKTool | 133 | Dynamic instrumentation, APK decompilation, runtime hooking |
| 2 | **Emulators** | LDPlayer, Nox, MEmu, BlueStacks | 147 | Android emulator control — instances, root, GPS, device profiles |
| 3 | **Binary Analysis** | Ghidra, Radare2, RevEng | 47 | Disassembly, decompilation, binary forensics, YARA, CAPA |
| 4 | **Network & Traffic** | Wireshark, MITMProxy, Scapy, NetAttack | 68 | Packet capture, MITM interception, protocol analysis |
| 5 | **Web Security** | Nuclei, Burp Suite, WebApp | 46 | Vulnerability scanning, fuzzing, injection testing |
| 6 | **Reconnaissance** | Recon, Adv Recon, OSINT | 44 | Subdomain enum, port scanning, OSINT, asset discovery |
| 7 | **Exploitation** | Exploit, Exploit Dev, Hashcat, Wordlist | 58 | Exploit frameworks, password cracking, payload generation |
| 8 | **Red Team & C2** | Red Team, Social Eng | 30 | C2 frameworks (Sliver, Mythic, Empire), phishing, social engineering |
| 9 | **Wireless & RF** | Wireless | 16 | WiFi cracking, Bluetooth, RF analysis (aircrack-ng suite) |
| 10 | **Active Directory** | Active Directory | 18 | BloodHound, Impacket, Kerberoasting, Pass-the-Hash |
| 11 | **Forensics & IR** | Forensics, Stego | 28 | Memory forensics, steganography, incident response |
| 12 | **Cloud Security** | Cloud | 14 | AWS/Azure/GCP enumeration, IAM analysis, resource audit |
| 13 | **Secrets Scanning** | Secrets | 12 | TruffleHog, Gitleaks, detect-secrets — credential detection in repos, filesystem, S3 |
| 14 | **Container & K8s** | Container | 14 | Trivy, Grype, Syft, Hadolint, kube-bench — image scanning, SBOM, CIS benchmarks |
| 15 | **IaC Scanning** | IaC | 12 | tfsec, Checkov, Terrascan, Semgrep — Terraform/CloudFormation/K8s misconfigurations |
| 16 | **Tunneling & Pivoting** | Tunneling | 14 | Chisel, Ligolo-ng, sshuttle, proxychains, SSH tunnels, DNS tunneling |
| 17 | **Core** | Leviathan, HTTP Toolkit | 7 | Kraken Engine translation, HTTP testing toolkit |

### MITRE ATT&CK Coverage

All 14 tactics are covered across the server catalog:

| Tactic ID | Name | Primary Servers |
|-----------|------|-----------------|
| TA0043 | Reconnaissance | Recon, Adv Recon, OSINT |
| TA0042 | Resource Development | Exploit Dev, Wordlist, Red Team |
| TA0001 | Initial Access | Nuclei, WebApp, Social Eng |
| TA0002 | Execution | Exploit, Exploit Dev |
| TA0003 | Persistence | Red Team, Active Directory |
| TA0004 | Privilege Escalation | Active Directory, Exploit |
| TA0005 | Defense Evasion | Leviathan (Kraken Engine), Red Team |
| TA0006 | Credential Access | Hashcat, Active Directory, Secrets |
| TA0007 | Discovery | Recon, Wireshark, Cloud |
| TA0008 | Lateral Movement | Active Directory, Tunneling |
| TA0009 | Collection | Forensics, Wireshark |
| TA0010 | Exfiltration | Stego, Tunneling |
| TA0011 | Command & Control | Red Team, Tunneling |
| TA0040 | Impact | Exploit, NetAttack |

---

## CLI

```bash
leviathan version                        # Platform manifest
leviathan doctor                         # Environment healthcheck (50+ tools)
leviathan translate encode --file app.py # Kraken Engine translation
leviathan translate decode --file app.py # Reverse translation
leviathan scan                           # Threat assessment
leviathan http dispatch --url <target>   # HTTP testing
leviathan http scan --url <target>       # Automated HTTP scan
```

### Interactive Launcher

```bash
python core/mcp_launcher.py
```

The launcher provides:
- Categorized view of all 40 MCP servers across 17 domains
- **Real-time tool availability detection** — shows which external tools are installed (green), partially available (yellow), or missing (red) per server
- Context prompt generation for focused Copilot sessions
- Search by category name or server name

### Diagnostics

```bash
leviathan doctor          # Terminal report
python core/doctor.py --json   # Machine-readable JSON output
```

Checks Python version, core files, config integrity, VS Code configuration, 50+ external tool installations, emulator availability, and filesystem permissions.

---

## Kraken Engine

The semantic translation engine (`core/translator.py` + `core/config.json`) provides 640+ rules across 9 categories for security terminology research:

| Category | Examples |
|----------|----------|
| Offensive | exploit → pressure_point, vulnerability → hull_breach |
| Malware | payload → depth_charge, rootkit → barnacle_cluster |
| Web | sql_injection → ink_injection, xss → current_crossing |
| C2 | reverse_shell → sonar_callback, botnet → shoal_network |
| Persistence | backdoor → sea_gate, privilege_escalation → depth_ascension |
| Binary | buffer_overflow → pressure_overflow, rop_chain → anchor_chain |
| Cloud | iam_escalation → depth_permissions |
| Evasion | obfuscation → deep_camouflage |
| Tools | metasploit → deep_sea_framework, cobalt_strike → trident_framework |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-capability`
3. Commit with conventional format: `git commit -m 'feat(domain): description'`
4. Push and open a Pull Request

### MCP Development

Each MCP server follows a standard structure:

```python
# _find_tool() + _run_tool() helpers
# TOOLS list (JSON Schema definitions)
# dispatch_tool() — routes tool calls to handlers
# handle_message() — JSON-RPC 2.0 method routing
# main_loop() — Content-Length framed stdio transport
```

See any existing server in `core/*/` for reference.

---

## Disclaimer

This platform is intended **exclusively** for authorized security testing, penetration testing engagements, CTF competitions, and security research. Users are responsible for ensuring compliance with applicable laws and obtaining proper authorization before testing any systems.

---

## License

[MIT](LICENSE)

---

<div align="center">

**Author:** [ThiagoFrag](https://github.com/ThiagoFrag)

</div>
