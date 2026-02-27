#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS — MCP Launcher Interativo
    Terminal colorido com seletor de categorias e MCPs

    Uso:
        python core/mcp_launcher.py
        python -m core.mcp_launcher

    Mostra todos os 49 MCP servers organizados por categoria.
    Ao selecionar uma categoria, exibe as ferramentas disponiveis
    e gera o prompt de contexto para focar a conversa do Copilot.
================================================================================
"""

import os
import shutil
import sys
import textwrap

# ============================================================================
# ANSI COLORS
# ============================================================================


class C:
    """Cores ANSI para terminal."""

    RST = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UL = "\033[4m"
    # Foreground
    BLACK = "\033[30m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    ORANGE = "\033[38;5;208m"
    PINK = "\033[38;5;213m"
    LIME = "\033[38;5;118m"
    PURPLE = "\033[38;5;141m"
    TEAL = "\033[38;5;43m"
    GOLD = "\033[38;5;220m"
    CORAL = "\033[38;5;203m"
    SKY = "\033[38;5;117m"
    # Background
    BG_DARK = "\033[48;5;233m"
    BG_BLUE = "\033[48;5;17m"
    BG_RED = "\033[48;5;52m"
    BG_GREEN = "\033[48;5;22m"
    BG_CYAN = "\033[48;5;23m"


def enable_ansi():
    """Ativa sequencias ANSI no Windows."""
    if os.name == "nt":
        os.system("")
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass


# ============================================================================
# MCP CATALOG — Todos os 49 servidores organizados por categoria
# ============================================================================

CATEGORIES = [
    {
        "id": "mobile",
        "name": "ANALISE MOBILE",
        "icon": "📱",
        "color": C.GREEN,
        "desc": "Instrumentacao dinamica, decompilacao APK, emuladores Android",
        "servers": [
            {
                "name": "ADB",
                "tools": 42,
                "desc": "Android Debug Bridge — shell, install, logcat, screenshot, port forward, tcpdump",
            },
            {
                "name": "Frida",
                "tools": 28,
                "desc": "Instrumentacao dinamica — bypass SSL/root/emulator, hook Java/Native, XXTEA extract",
            },
            {
                "name": "Objection",
                "tools": 20,
                "desc": "Exploracao mobile runtime — bypass SSL, dump keystore, patch APK, listar activities",
            },
            {
                "name": "JADX",
                "tools": 16,
                "desc": "Decompilacao APK — busca crypto, keys, URLs, permissions, native libs",
            },
            {
                "name": "Androguard",
                "tools": 15,
                "desc": "Analise estatica Python APK — xrefs, security audit, comparacao de versoes",
            },
            {
                "name": "APKTool",
                "tools": 12,
                "desc": "Decode/rebuild/sign APK — patch smali, inject code, rebuild resources",
            },
        ],
    },
    {
        "id": "emulators",
        "name": "EMULADORES",
        "icon": "🖥️",
        "color": C.BLUE,
        "desc": "Controle total de emuladores Android — instancias, root, GPS, device profiles",
        "servers": [
            {
                "name": "LDPlayer",
                "tools": 89,
                "desc": "Emulador principal — 89 tools incluindo Frida integrado, clones, randomizacao",
            },
            {
                "name": "Nox",
                "tools": 22,
                "desc": "NoxPlayer — NoxConsole CLI, macros, root toggle, GPS spoofing",
            },
            {
                "name": "MEmu",
                "tools": 19,
                "desc": "MEmu Play — memuc CLI, clones, GPS, perfis de device",
            },
            {
                "name": "BlueStacks",
                "tools": 17,
                "desc": "BlueStacks — HD-Player, instancias multiplas, ADB connect",
            },
        ],
    },
    {
        "id": "binary",
        "name": "ANALISE BINARIA",
        "icon": "🔬",
        "color": C.MAGENTA,
        "desc": "Engenharia reversa de binarios — disassembly, decompile, strings, crypto",
        "servers": [
            {
                "name": "Ghidra",
                "tools": 15,
                "desc": "Analise headless — decompile, xrefs, strings, exports, JNI bridges",
            },
            {
                "name": "Radare2",
                "tools": 16,
                "desc": "Analise binaria CLI — disasm, patch, decompile, search bytes",
            },
            {
                "name": "RevEng",
                "tools": 16,
                "desc": "Engenharia reversa — objdump, readelf, binwalk, yara, capa, pefile, oletools",
            },
        ],
    },
    {
        "id": "network",
        "name": "REDE & TRAFEGO",
        "icon": "🌊",
        "color": C.CYAN,
        "desc": "Captura, analise e interceptacao de trafego de rede",
        "servers": [
            {
                "name": "Wireshark",
                "tools": 23,
                "desc": "Captura & analise — DNS, HTTP, TLS, credentials, protocol hierarchy",
            },
            {
                "name": "MITMProxy",
                "tools": 14,
                "desc": "Proxy MITM — intercept HTTPS, modify requests, scripts, HAR export",
            },
            {
                "name": "Scapy",
                "tools": 15,
                "desc": "Packet crafting — SYN scan, ARP scan, fuzzing, custom packets",
            },
            {
                "name": "NetAttack",
                "tools": 16,
                "desc": "Ataques de rede/MITM — bettercap, ettercap, hping3, sslstrip, snort, dnschef",
            },
        ],
    },
    {
        "id": "web",
        "name": "SEGURANCA WEB",
        "icon": "🕸️",
        "color": C.ORANGE,
        "desc": "Testes de seguranca web — scan, fuzzing, injection, XSS, SSRF",
        "servers": [
            {
                "name": "Nuclei",
                "tools": 17,
                "desc": "Scanner suite — nuclei + sqlmap + nmap + ffuf + nikto + subfinder",
            },
            {
                "name": "Burp Suite",
                "tools": 15,
                "desc": "Web security — active scan, spider, intruder, repeater via REST API",
            },
            {
                "name": "WebApp",
                "tools": 14,
                "desc": "Seguranca web avancada — xsstrike, wfuzz, arjun, dalfox, commix, paramspider",
            },
        ],
    },
    {
        "id": "recon",
        "name": "RECONHECIMENTO",
        "icon": "🔍",
        "color": C.SKY,
        "desc": "Descoberta de ativos, subdominios, portas, servicos, crawling",
        "servers": [
            {
                "name": "Recon",
                "tools": 14,
                "desc": "Reconhecimento base — amass, gobuster, masscan, whatweb, dnsrecon, fierce",
            },
            {
                "name": "Adv Recon",
                "tools": 16,
                "desc": "Recon avancado — rustscan, autorecon, feroxbuster, katana, wpscan, eyewitness",
            },
            {
                "name": "OSINT",
                "tools": 14,
                "desc": "Inteligencia de fontes abertas — shodan, sherlock, maigret, dnstwist, theharvester",
            },
        ],
    },
    {
        "id": "exploit",
        "name": "EXPLORACAO",
        "icon": "💀",
        "color": C.RED,
        "desc": "Ferramentas de exploracao, payloads, brute-force, cracking",
        "servers": [
            {
                "name": "Exploit",
                "tools": 14,
                "desc": "Exploracao base — searchsploit, msfvenom, hydra, john, medusa, crackmapexec",
            },
            {
                "name": "Exploit Dev",
                "tools": 16,
                "desc": "Dev de exploits — pwntools, angr, checksec, ROPgadget, afl, boofuzz, msfvenom",
            },
            {
                "name": "Hashcat",
                "tools": 12,
                "desc": "Cracking de senhas — hashcat, john the ripper, identify hash, wordlists",
            },
            {
                "name": "Wordlist",
                "tools": 16,
                "desc": "Geracao de wordlists — cewl, crunch, cupp, john rules, patator, hashid, rsmangler",
            },
        ],
    },
    {
        "id": "redteam",
        "name": "RED TEAM & C2",
        "icon": "🔥",
        "color": C.CORAL,
        "desc": "Command & Control, payloads evasivos, frameworks de ataque",
        "servers": [
            {
                "name": "Red Team",
                "tools": 16,
                "desc": "C2/payload — sliver, mythic, empire, havoc, covenant, donut, scarecrow, veil",
            },
            {
                "name": "Social Eng",
                "tools": 14,
                "desc": "Engenharia social — setoolkit, gophish, evilginx2, beef-xss, wifiphisher",
            },
        ],
    },
    {
        "id": "wireless",
        "name": "WIRELESS & RF",
        "icon": "📡",
        "color": C.LIME,
        "desc": "Ataques wireless, WiFi, Bluetooth, RF scanning",
        "servers": [
            {
                "name": "Wireless",
                "tools": 16,
                "desc": "WiFi/BLE/RF — aircrack-ng suite, wifite, reaver, bully, bettercap, kismet, cowpatty",
            },
        ],
    },
    {
        "id": "ad",
        "name": "ACTIVE DIRECTORY",
        "icon": "🏰",
        "color": C.GOLD,
        "desc": "Ataques AD, Kerberos, LDAP, SMB, WinRM, pass-the-hash",
        "servers": [
            {
                "name": "Active Directory",
                "tools": 18,
                "desc": "AD/Kerberos — bloodhound, impacket (8 tools), netexec, evil-winrm, mimikatz, rubeus, certipy",
            },
        ],
    },
    {
        "id": "forensics",
        "name": "FORENSE & IR",
        "icon": "🔎",
        "color": C.TEAL,
        "desc": "Forense digital, analise de memoria, incident response",
        "servers": [
            {
                "name": "Forensics",
                "tools": 14,
                "desc": "Forense digital — volatility3, yara, binwalk, capa, foremost, bulk_extractor",
            },
            {
                "name": "Stego",
                "tools": 14,
                "desc": "Esteganografia — steghide, zsteg, openstego, outguess, snow, stegseek, exiftool",
            },
        ],
    },
    {
        "id": "cloud",
        "name": "CLOUD & SUPPLY CHAIN",
        "icon": "☁️",
        "color": C.PURPLE,
        "desc": "Seguranca cloud, containers, IaC, secrets scanning",
        "servers": [
            {
                "name": "Cloud",
                "tools": 14,
                "desc": "Cloud security — trivy, gitleaks, trufflehog, semgrep, prowler, checkov, syft, grype",
            },
        ],
    },
    {
        "id": "core",
        "name": "CORE LEVIATHAN",
        "icon": "🐙",
        "color": C.WHITE,
        "desc": "Motor de traducao semantica, HTTP toolkit, servidor MCP core",
        "servers": [
            {
                "name": "Leviathan",
                "tools": 7,
                "desc": "Kraken Engine — encode/decode/check/find_terms/translate_file/reload_rules",
            },
            {
                "name": "HTTP Toolkit",
                "tools": 0,
                "desc": "Interceptador Abissal — dispatch, scan, interactive, cURL generation",
            },
        ],
    },
]


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================


def get_terminal_width():
    """Largura do terminal, fallback 100."""
    return shutil.get_terminal_size((100, 30)).columns


def clear():
    """Limpa a tela."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    """Exibe o banner do Leviathan."""
    w = get_terminal_width()
    banner = f"""{C.CYAN}{C.BOLD}
    ██╗     ███████╗██╗   ██╗██╗ █████╗ ████████╗██╗  ██╗ █████╗ ███╗   ██╗
    ██║     ██╔════╝██║   ██║██║██╔══██╗╚══██╔══╝██║  ██║██╔══██╗████╗  ██║
    ██║     █████╗  ██║   ██║██║███████║   ██║   ███████║███████║██╔██╗ ██║
    ██║     ██╔══╝  ╚██╗ ██╔╝██║██╔══██║   ██║   ██╔══██║██╔══██║██║╚██╗██║
    ███████╗███████╗ ╚████╔╝ ██║██║  ██║   ██║   ██║  ██║██║  ██║██║ ╚████║
    ╚══════╝╚══════╝  ╚═══╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
{C.RST}"""
    print(banner)
    subtitle = "MCP LAUNCHER — Seletor de Ferramentas"
    print(f"{C.DIM}{'─' * w}{C.RST}")
    print(f"{C.BOLD}{C.WHITE}    {subtitle}{C.RST}")
    print(f"{C.DIM}    49 Servidores MCP  |  704+ Ferramentas  |  13 Categorias{C.RST}")
    print(f"{C.DIM}{'─' * w}{C.RST}")
    print()


def print_categories():
    """Exibe todas as categorias numeradas."""
    total_tools = 0
    for i, cat in enumerate(CATEGORIES, 1):
        tools = sum(s["tools"] for s in cat["servers"])
        total_tools += tools
        servers_count = len(cat["servers"])
        num = f"{C.BOLD}{cat['color']}[{i:2d}]{C.RST}"
        icon = cat["icon"]
        name = f"{C.BOLD}{cat['color']}{cat['name']}{C.RST}"
        info = f"{C.DIM}({servers_count} MCP{'s' if servers_count > 1 else ''}, {tools} ferramentas){C.RST}"
        desc = f"{C.DIM}{cat['desc']}{C.RST}"
        print(f"    {num}  {icon}  {name}  {info}")
        print(f"         {desc}")
        print()

    print(f"{C.DIM}{'─' * get_terminal_width()}{C.RST}")
    print(f"    {C.BOLD}{C.YELLOW}[ 0]{C.RST}  🚪  {C.BOLD}{C.YELLOW}SAIR{C.RST}")
    print(
        f"    {C.BOLD}{C.CYAN}[99]{C.RST}  📋  {C.BOLD}{C.CYAN}VER TODAS AS FERRAMENTAS{C.RST}"
    )
    print(f"{C.DIM}{'─' * get_terminal_width()}{C.RST}")
    print()


def print_category_detail(cat):
    """Exibe detalhes de uma categoria com todas as ferramentas."""
    w = get_terminal_width()
    clear()
    total_tools = sum(s["tools"] for s in cat["servers"])
    print()
    print(f"{C.DIM}{'─' * w}{C.RST}")
    print(
        f"    {cat['icon']}  {C.BOLD}{cat['color']}{cat['name']}{C.RST}  —  {total_tools} ferramentas"
    )
    print(f"    {C.DIM}{cat['desc']}{C.RST}")
    print(f"{C.DIM}{'─' * w}{C.RST}")
    print()

    for s in cat["servers"]:
        print(
            f"    {C.BOLD}{cat['color']}■ {s['name']}{C.RST}  {C.DIM}({s['tools']} ferramentas){C.RST}"
        )
        # Word wrap a descricao
        wrapped = textwrap.fill(s["desc"], width=w - 10)
        for line in wrapped.split("\n"):
            print(f"      {C.WHITE}{line}{C.RST}")
        print()

    print(f"{C.DIM}{'─' * w}{C.RST}")
    print()
    print(f"    {C.BOLD}{C.GREEN}[C]{C.RST} Copiar prompt de contexto para Copilot")
    print(f"    {C.BOLD}{C.YELLOW}[V]{C.RST} Voltar ao menu principal")
    print()


def print_all_tools():
    """Exibe TODAS as ferramentas de TODAS as categorias."""
    w = get_terminal_width()
    clear()
    print()
    print(f"{C.DIM}{'═' * w}{C.RST}")
    print(f"    {C.BOLD}{C.CYAN}📋  CATALOGO COMPLETO — TODOS OS MCP SERVERS{C.RST}")
    print(f"{C.DIM}{'═' * w}{C.RST}")
    print()

    grand_total = 0
    server_count = 0
    for cat in CATEGORIES:
        cat_tools = sum(s["tools"] for s in cat["servers"])
        grand_total += cat_tools
        print(
            f"  {cat['icon']}  {C.BOLD}{cat['color']}{cat['name']}{C.RST}  ({cat_tools} ferramentas)"
        )
        print(f"  {C.DIM}{'─' * (w - 4)}{C.RST}")
        for s in cat["servers"]:
            server_count += 1
            print(
                f"    {cat['color']}▸{C.RST} {C.BOLD}{s['name']}{C.RST} [{s['tools']}] — {C.DIM}{s['desc']}{C.RST}"
            )
        print()

    print(f"{C.DIM}{'═' * w}{C.RST}")
    print(
        f"    {C.BOLD}{C.WHITE}TOTAL: {server_count} servidores MCP  |  {grand_total} ferramentas{C.RST}"
    )
    print(f"{C.DIM}{'═' * w}{C.RST}")
    print()


def generate_context_prompt(cat):
    """Gera o prompt de contexto para o Copilot focar na categoria."""
    servers_list = ", ".join(s["name"] for s in cat["servers"])
    tools_total = sum(s["tools"] for s in cat["servers"])

    prompt = f"""Foco: {cat['name']}
Categoria: {cat['desc']}
Servidores MCP disponiveis: {servers_list} ({tools_total} ferramentas)

"""
    for s in cat["servers"]:
        prompt += f"- {s['name']} ({s['tools']} tools): {s['desc']}\n"

    prompt += f"""
Instrucoes: Foque TOTALMENTE nesta categoria. Use APENAS os MCPs listados acima como prioridade.
Quando eu pedir algo, route automaticamente para as ferramentas desta categoria.
Encadeie multiplas ferramentas quando possivel para resultado maximo.
"""
    return prompt


def copy_to_clipboard(text):
    """Copia texto para o clipboard."""
    try:
        if os.name == "nt":
            import subprocess

            p = subprocess.Popen(["clip"], stdin=subprocess.PIPE)
            p.communicate(text.encode("utf-8"))
            return True
        else:
            import subprocess

            p = subprocess.Popen(
                ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE
            )
            p.communicate(text.encode("utf-8"))
            return True
    except Exception:
        return False


# ============================================================================
# CONTEXT MODE — Modo focado por categoria
# ============================================================================

CATEGORY_CONTEXTS = {
    "mobile": {
        "greeting": "Modo ANALISE MOBILE ativado. Pronto pra instrumentar, decompilar e hookear.",
        "focus": "APK, instrumentacao Frida, decompilacao JADX/Ghidra, bypass SSL/root, emuladores",
        "pipeline": "jadx decompile -> androguard audit -> ghidra analyze .so -> frida bypass_all -> wireshark capture",
    },
    "emulators": {
        "greeting": "Modo EMULADORES ativado. Controle total dos Android VMs.",
        "focus": "LDPlayer, BlueStacks, MEmu, Nox — instancias, root, GPS, clones, device profiles",
        "pipeline": "ldplayer start -> adb install -> frida attach -> randomize device -> batch ops",
    },
    "binary": {
        "greeting": "Modo ANALISE BINARIA ativado. Vamos disassemblar e decompilar.",
        "focus": "Ghidra headless, Radare2, objdump, readelf, binwalk, YARA, CAPA, strings",
        "pipeline": "ghidra analyze -> list_functions -> decompile targets -> radare2 xrefs -> frida hook_native",
    },
    "network": {
        "greeting": "Modo REDE & TRAFEGO ativado. Captura e interceptacao prontas.",
        "focus": "Wireshark, MITMProxy, Scapy, bettercap, ettercap, hping3, sslstrip, snort",
        "pipeline": "wireshark capture -> follow_stream -> mitmproxy intercept -> scapy craft -> netattack mitm",
    },
    "web": {
        "greeting": "Modo SEGURANCA WEB ativado. Scan, fuzz e exploit prontos.",
        "focus": "Nuclei, Burp Suite, SQLMap, XSStrike, wfuzz, arjun, dalfox, commix, ffuf",
        "pipeline": "nuclei scan -> burp active_scan -> sqlmap test -> xsstrike -> wfuzz fuzz",
    },
    "recon": {
        "greeting": "Modo RECONHECIMENTO ativado. Descoberta de ativos e superficie de ataque.",
        "focus": "Amass, gobuster, masscan, rustscan, feroxbuster, katana, wpscan, shodan, sherlock",
        "pipeline": "recon subdomain -> port_scan -> dir_fuzz -> screenshot -> osint gather",
    },
    "exploit": {
        "greeting": "Modo EXPLORACAO ativado. Payloads e cracking prontos.",
        "focus": "Searchsploit, msfvenom, hydra, john, hashcat, pwntools, angr, ROPgadget, AFL",
        "pipeline": "searchsploit search -> msfvenom generate -> hydra brute -> hashcat crack -> pwntools exploit",
    },
    "redteam": {
        "greeting": "Modo RED TEAM & C2 ativado. Command and Control operacional.",
        "focus": "Sliver, Mythic, Empire, Havoc, Covenant, donut, scarecrow, setoolkit, gophish",
        "pipeline": "redteam c2_setup -> listener -> stager -> agent_deploy -> social_eng phish",
    },
    "wireless": {
        "greeting": "Modo WIRELESS & RF ativado. Ataques WiFi e Bluetooth prontos.",
        "focus": "aircrack-ng suite, wifite, reaver, bully, bettercap BLE, kismet, cowpatty",
        "pipeline": "airmon start -> airodump scan -> aireplay deauth -> aircrack crack -> wifite auto",
    },
    "ad": {
        "greeting": "Modo ACTIVE DIRECTORY ativado. Domain domination pronta.",
        "focus": "Bloodhound, impacket (secretsdump/psexec/getTGT), netexec, evil-winrm, mimikatz, rubeus, certipy",
        "pipeline": "bloodhound collect -> analyze -> impacket getNPUsers -> getTGT -> secretsdump -> evil-winrm",
    },
    "forensics": {
        "greeting": "Modo FORENSE & IR ativado. Analise de artefatos e evidencias.",
        "focus": "Volatility3, YARA, binwalk, CAPA, foremost, steghide, zsteg, exiftool",
        "pipeline": "volatility pslist -> filescan -> dumpfiles -> yara scan -> binwalk extract -> stego analyze",
    },
    "cloud": {
        "greeting": "Modo CLOUD & SUPPLY CHAIN ativado. Auditoria de infra cloud.",
        "focus": "Trivy, gitleaks, trufflehog, semgrep, prowler, checkov, syft, grype",
        "pipeline": "trivy scan -> gitleaks detect -> semgrep audit -> prowler assess -> checkov iac",
    },
    "core": {
        "greeting": "Modo CORE LEVIATHAN. Motor de traducao e toolkit HTTP.",
        "focus": "Kraken Engine encode/decode, HTTP toolkit dispatch/scan, traducao semantica",
        "pipeline": "leviathan encode -> process -> decode -> check -> translate_file",
    },
}


def context_mode(cat):
    """Entra no modo de contexto focado para uma categoria."""
    ctx = CATEGORY_CONTEXTS.get(cat["id"], {})
    w = get_terminal_width()

    clear()
    print()
    print(f"{C.DIM}{'═' * w}{C.RST}")
    print(
        f"    {cat['icon']}  {C.BOLD}{cat['color']}{cat['name']}{C.RST}  —  MODO FOCADO"
    )
    print(f"{C.DIM}{'═' * w}{C.RST}")
    print()
    print(f"    {C.GREEN}{C.BOLD}{ctx.get('greeting', '')}{C.RST}")
    print()
    print(f"    {C.BOLD}Foco:{C.RST} {ctx.get('focus', '')}")
    print()
    print(f"    {C.BOLD}Pipeline sugerido:{C.RST}")
    print(f"    {C.CYAN}{ctx.get('pipeline', '')}{C.RST}")
    print()
    print(f"{C.DIM}{'─' * w}{C.RST}")
    print()
    print(f"    {C.BOLD}Servidores MCP nesta categoria:{C.RST}")
    for s in cat["servers"]:
        print(
            f"    {cat['color']}▸{C.RST} {C.BOLD}{s['name']}{C.RST} [{s['tools']}] — {s['desc']}"
        )
    print()
    print(f"{C.DIM}{'─' * w}{C.RST}")
    print()
    print(
        f"    {C.BOLD}{C.GREEN}[C]{C.RST} Copiar prompt de contexto para colar no Copilot"
    )
    print(f"    {C.BOLD}{C.YELLOW}[V]{C.RST} Voltar ao menu")
    print()

    while True:
        try:
            choice = (
                input(f"    {C.BOLD}{cat['color']}LEVIATHAN [{cat['name']}]>{C.RST} ")
                .strip()
                .upper()
            )
        except (EOFError, KeyboardInterrupt):
            return

        if choice == "V":
            return
        elif choice == "C":
            prompt = generate_context_prompt(cat)
            if copy_to_clipboard(prompt):
                print(f"\n    {C.GREEN}{C.BOLD}Prompt copiado para o clipboard!{C.RST}")
                print(
                    f"    {C.DIM}Cole no chat do Copilot para ativar o modo focado.{C.RST}\n"
                )
            else:
                print(f"\n    {C.YELLOW}Nao foi possivel copiar. Prompt:{C.RST}\n")
                print(prompt)
                print()
        else:
            print(f"    {C.RED}Opcao invalida. Use [C] ou [V].{C.RST}")


# ============================================================================
# MAIN LOOP
# ============================================================================


def main():
    """Loop principal do launcher."""
    enable_ansi()

    # Setar titulo do terminal
    if os.name == "nt":
        os.system("title LEVIATHAN VS — MCP Launcher")

    while True:
        clear()
        print_banner()
        print_categories()

        try:
            raw = input(f"    {C.BOLD}{C.CYAN}LEVIATHAN >{C.RST} ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n    {C.DIM}Retornando a superficie...{C.RST}")
            break

        if not raw:
            continue

        if raw == "0":
            clear()
            print(f"\n    {C.DIM}Retornando a superficie...{C.RST}\n")
            break

        if raw == "99":
            print_all_tools()
            input(f"\n    {C.DIM}Pressione ENTER para voltar...{C.RST}")
            continue

        try:
            idx = int(raw)
            if 1 <= idx <= len(CATEGORIES):
                cat = CATEGORIES[idx - 1]
                context_mode(cat)
            else:
                print(
                    f"    {C.RED}Numero invalido. Use 1-{len(CATEGORIES)}, 0 ou 99.{C.RST}"
                )
                input(f"    {C.DIM}Pressione ENTER...{C.RST}")
        except ValueError:
            # Busca por nome
            query = raw.lower()
            found = None
            for cat in CATEGORIES:
                if query in cat["name"].lower() or query in cat["id"]:
                    found = cat
                    break
                for s in cat["servers"]:
                    if query in s["name"].lower():
                        found = cat
                        break
                if found:
                    break

            if found:
                context_mode(found)
            else:
                print(
                    f"    {C.RED}Nao encontrado: '{raw}'. Use numero ou nome da categoria.{C.RST}"
                )
                input(f"    {C.DIM}Pressione ENTER...{C.RST}")


if __name__ == "__main__":
    main()
