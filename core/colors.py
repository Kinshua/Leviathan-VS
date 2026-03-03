#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
████████████████████████████████████████████████████████████████████████████████
██                                                                            ██
██   ☠️  LEVIATHAN VS — ABYSSAL VISUAL WARFARE ENGINE v66.6.0  ☠️            ██
██                                                                            ██
██   Modulo de guerra visual. Cada pixel e uma ameaca. Cada frame, um aviso.  ██
██   Engine grafico completo: cores, gradientes, particulas, glitch, matrix,  ██
██   EKG, binario, hex, progress bars, animacoes de hacking, simulacoes de   ██
██   intrusao, threat dial, kill feed, e muito mais.                          ██
██                                                                            ██
██   "A arte da destruicao comeca com a arte da apresentacao."                ██
██                                                                            ██
████████████████████████████████████████████████████████████████████████████████
"""

import os
import random
import sys
import time
from typing import List, Tuple

# ════════════════════════════════════════════════════════════════════════════
#  ANSI COLOR ARSENAL — 256 + TRUE COLOR + EFFECTS
# ════════════════════════════════════════════════════════════════════════════


class Colors:
    """Paleta do Abismo — 60+ cores do inferno digital."""

    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    WHITE = "\033[97m"
    BLACK = "\033[30m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    RAPID_BLINK = "\033[6m"
    REVERSE = "\033[7m"
    HIDDEN = "\033[8m"
    STRIKETHROUGH = "\033[9m"
    RESET = "\033[0m"

    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_BLACK = "\033[40m"
    BG_WHITE = "\033[47m"
    BG_DARK = "\033[48;5;233m"
    BG_BLOOD = "\033[48;5;52m"
    BG_CRIMSON = "\033[48;5;88m"
    BG_VOID = "\033[48;5;232m"

    BLOOD = "\033[38;5;196m"
    CRIMSON = "\033[38;5;160m"
    DARK_RED = "\033[38;5;88m"
    MAROON = "\033[38;5;52m"
    INFERNO = "\033[38;5;202m"
    EMBER = "\033[38;5;166m"
    TOXIC = "\033[38;5;118m"
    ACID = "\033[38;5;46m"
    NEON_GREEN = "\033[38;5;82m"
    RADIOACTIVE = "\033[38;5;76m"
    ABYSS_BLUE = "\033[38;5;21m"
    DEEP_BLUE = "\033[38;5;19m"
    ELECTRIC_BLUE = "\033[38;5;33m"
    ICE = "\033[38;5;159m"
    DEEP_PURPLE = "\033[38;5;93m"
    PHANTOM = "\033[38;5;141m"
    VIOLET = "\033[38;5;129m"
    GHOST = "\033[38;5;250m"
    ASH = "\033[38;5;245m"
    SHADOW = "\033[38;5;238m"
    VOID = "\033[38;5;232m"
    GOLD = "\033[38;5;220m"
    AMBER = "\033[38;5;214m"
    CORAL = "\033[38;5;203m"
    SKY = "\033[38;5;117m"
    PINK = "\033[38;5;213m"
    HOT_PINK = "\033[38;5;199m"
    ORANGE = "\033[38;5;208m"
    LIME = "\033[38;5;118m"
    TEAL = "\033[38;5;43m"
    SKULL = "\033[38;5;255m"
    BONE = "\033[38;5;230m"
    RUST = "\033[38;5;130m"
    COPPER = "\033[38;5;136m"

    LAVA = "\033[38;2;255;69;0m"
    HELLFIRE = "\033[38;2;200;16;0m"
    OCEAN_DEEP = "\033[38;2;0;20;60m"
    PLASMA = "\033[38;2;180;0;255m"
    MATRIX = "\033[38;2;0;255;65m"
    MIDNIGHT = "\033[38;2;25;25;112m"
    NEON_RED = "\033[38;2;255;0;60m"
    NEON_BLUE = "\033[38;2;0;150;255m"
    NEON_PURPLE = "\033[38;2;160;0;255m"
    CYBER_YELLOW = "\033[38;2;255;255;0m"
    TERMINAL_GREEN = "\033[38;2;0;200;0m"
    HACK_GREEN = "\033[38;2;32;194;14m"
    DEATH_BLACK = "\033[38;2;8;8;8m"
    BLOOD_MOON = "\033[38;2;120;10;10m"
    CRYPT_GRAY = "\033[38;2;60;60;70m"
    ABYSSAL_PURPLE = "\033[38;2;40;0;80m"
    WARZONE_ORANGE = "\033[38;2;255;100;0m"


class Fx:
    """Efeitos especiais de terminal — arsenal visual."""

    CLEAR = "\033[2J\033[H"
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"
    SAVE_POS = "\033[s"
    RESTORE_POS = "\033[u"
    ERASE_LINE = "\033[2K"
    ERASE_TO_END = "\033[K"

    @staticmethod
    def move_to(row: int, col: int) -> str:
        return f"\033[{row};{col}H"

    @staticmethod
    def up(n: int = 1) -> str:
        return f"\033[{n}A"

    @staticmethod
    def down(n: int = 1) -> str:
        return f"\033[{n}B"

    @staticmethod
    def right(n: int = 1) -> str:
        return f"\033[{n}C"

    @staticmethod
    def left(n: int = 1) -> str:
        return f"\033[{n}D"

    @staticmethod
    def clear_line() -> str:
        return "\033[2K"

    @staticmethod
    def rgb_fg(r: int, g: int, b: int) -> str:
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def rgb_bg(r: int, g: int, b: int) -> str:
        return f"\033[48;2;{r};{g};{b}m"


# ════════════════════════════════════════════════════════════════════════════
#  GRADIENT ENGINE — 16 PALETTES
# ════════════════════════════════════════════════════════════════════════════

_GRADIENTS = {
    "fire": [(80, 0, 0), (160, 30, 0), (255, 80, 0), (255, 160, 0), (255, 220, 50)],
    "ocean": [(0, 10, 40), (0, 40, 100), (0, 80, 160), (0, 140, 220), (80, 200, 255)],
    "toxic": [(0, 40, 0), (0, 100, 0), (0, 180, 0), (0, 255, 0), (120, 255, 120)],
    "blood": [(40, 0, 0), (80, 0, 0), (140, 0, 0), (200, 0, 0), (255, 40, 40)],
    "phantom": [
        (30, 0, 40),
        (60, 0, 100),
        (100, 0, 180),
        (150, 40, 255),
        (200, 120, 255),
    ],
    "matrix": [(0, 20, 0), (0, 60, 0), (0, 120, 0), (0, 200, 0), (0, 255, 65)],
    "skull": [
        (40, 40, 40),
        (80, 80, 80),
        (140, 140, 140),
        (200, 200, 200),
        (255, 255, 255),
    ],
    "abyss": [(0, 0, 20), (0, 0, 60), (10, 0, 120), (40, 0, 200), (80, 20, 255)],
    "inferno": [(40, 0, 0), (120, 20, 0), (200, 60, 0), (255, 120, 0), (255, 200, 0)],
    "ice": [(0, 10, 40), (0, 40, 80), (0, 80, 140), (40, 160, 220), (120, 220, 255)],
    "nuclear": [
        (40, 40, 0),
        (80, 100, 0),
        (140, 180, 0),
        (200, 255, 0),
        (255, 255, 80),
    ],
    "void": [(0, 0, 0), (15, 0, 15), (30, 0, 30), (50, 0, 50), (80, 0, 80)],
    "cyber": [(0, 20, 40), (0, 60, 100), (0, 100, 160), (0, 160, 200), (0, 220, 255)],
    "hellfire": [(20, 0, 0), (80, 0, 0), (160, 0, 0), (255, 60, 0), (255, 160, 0)],
    "plague": [(20, 30, 0), (40, 60, 0), (80, 120, 0), (160, 200, 0), (200, 255, 40)],
    "necrotic": [(20, 0, 20), (40, 0, 40), (80, 0, 60), (120, 0, 80), (160, 20, 120)],
}


def _interp(c1: tuple, c2: tuple, t: float) -> tuple:
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def gradient_text(text: str, palette: str = "fire") -> str:
    """Renderiza texto com gradiente de cores true-color."""
    colors = _GRADIENTS.get(palette, _GRADIENTS["fire"])
    if not text:
        return text
    result = []
    n = len(text)
    segments = len(colors) - 1
    for i, ch in enumerate(text):
        t = i / max(n - 1, 1)
        seg = min(int(t * segments), segments - 1)
        local_t = (t * segments) - seg
        r, g, b = _interp(colors[seg], colors[seg + 1], local_t)
        result.append(f"\033[38;2;{r};{g};{b}m{ch}")
    result.append(Colors.RESET)
    return "".join(result)


def multi_gradient(text: str, palettes: List[str]) -> str:
    """Aplicar multiplos gradientes em camadas alternadas."""
    if not palettes:
        return text
    lines = text.split("\n")
    result = []
    for i, line in enumerate(lines):
        pal = palettes[i % len(palettes)]
        result.append(gradient_text(line, pal))
    return "\n".join(result)


# ════════════════════════════════════════════════════════════════════════════
#  TERMINAL EFFECTS ENGINE
# ════════════════════════════════════════════════════════════════════════════


def typewriter(text: str, delay: float = 0.015, color: str = "") -> None:
    """Efeito de digitacao com velocidade variavel."""
    for ch in text:
        sys.stdout.write(f"{color}{ch}{Colors.RESET}")
        sys.stdout.flush()
        if ch in ".!?:":
            time.sleep(delay * 4)
        elif ch in ",;-":
            time.sleep(delay * 2)
        else:
            time.sleep(delay)
    print()


def glitch_text(text: str, intensity: int = 3) -> str:
    """Gerar texto com efeito glitch."""
    glitch_chars = "░▒▓█▀▄▌▐│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬"
    result = list(text)
    for _ in range(intensity):
        if result:
            pos = random.randint(0, len(result) - 1)
            result[pos] = random.choice(glitch_chars)
    return "".join(result)


def hacker_decode(text: str, delay: float = 0.02, color: str = "") -> None:
    """Animacao estilo hacker — caracteres randomicos decodificam para texto real."""
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"
    decoded = [False] * len(text)
    display = [random.choice(charset) if c != " " else " " for c in text]

    for _ in range(len(text) * 2):
        remaining = [i for i, d in enumerate(decoded) if not d and text[i] != " "]
        if not remaining:
            break
        idx = random.choice(remaining)
        decoded[idx] = True
        display[idx] = text[idx]
        for i in range(len(text)):
            if not decoded[i] and text[i] != " ":
                display[i] = random.choice(charset)
        sys.stdout.write(f"\r{color}{''.join(display)}{Colors.RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(f"\r{color}{text}{Colors.RESET}\n")
    sys.stdout.flush()


def binary_rain(width: int = 60, lines: int = 5, delay: float = 0.03) -> None:
    """Chuva de binarios estilo Matrix."""
    for _ in range(lines):
        line = "".join(random.choice("01") for _ in range(width))
        colored = ""
        for ch in line:
            shade = random.randint(0, 3)
            greens = [60, 120, 200, 255]
            colored += f"\033[38;2;0;{greens[shade]};0m{ch}"
        print(f"  {colored}{Colors.RESET}")
        time.sleep(delay)


def hex_dump_fake(lines: int = 4, width: int = 16) -> None:
    """Hex dump falso para efeito visual."""
    color_options = [196, 160, 208, 82, 117]
    for i in range(lines):
        addr = f"\033[38;5;240m{0x00401000 + i * width:08x}\033[0m"
        hexbytes = " ".join(
            f"\033[38;5;{random.choice(color_options)}m{random.randint(0, 255):02x}\033[0m"
            for _ in range(width)
        )
        ascii_repr = "".join(
            chr(random.randint(33, 126)) if random.random() > 0.3 else "."
            for _ in range(width)
        )
        print(f"  {addr}  {hexbytes}  \033[38;5;245m|{ascii_repr}|\033[0m")


def progress_bar(
    label: str,
    duration: float = 1.0,
    width: int = 40,
    color: str = "",
    fill: str = "█",
    empty: str = "░",
) -> None:
    """Barra de progresso animada."""
    if not color:
        color = Colors.BLOOD
    steps = 50
    for i in range(steps + 1):
        pct = i / steps
        filled = int(pct * width)
        bar = fill * filled + empty * (width - filled)
        sys.stdout.write(f"\r  {color}{label} [{bar}] {pct * 100:5.1f}%{Colors.RESET}")
        sys.stdout.flush()
        time.sleep(duration / steps)
    print()


def threat_scanner(targets: List[str], delay: float = 0.08) -> None:
    """Simulacao de scanner de ameacas."""
    threat_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL", "CATASTROPHIC"]
    threat_colors = [
        Colors.GREEN,
        Colors.YELLOW,
        Colors.ORANGE,
        Colors.RED,
        Colors.BLOOD,
    ]
    for target in targets:
        level_idx = random.randint(0, 4)
        sys.stdout.write(
            f"  {Colors.DIM}SCAN {Colors.RESET}{Colors.CYAN}{target}{Colors.RESET}"
        )
        sys.stdout.flush()
        time.sleep(delay)
        print(
            f" -> {threat_colors[level_idx]}{Colors.BOLD}{threat_levels[level_idx]}{Colors.RESET}"
        )
        time.sleep(delay / 2)


def ekg_heartbeat(beats: int = 8, color: str = "") -> None:
    """EKG heartbeat visual."""
    if not color:
        color = Colors.BLOOD
    line = ""
    for _ in range(beats):
        line += "───" + "╱╲" + "──"
    print(f"  {color}{line}{Colors.RESET}")


def kill_feed(entries: List[Tuple[str, str]], delay: float = 0.1) -> None:
    """Feed de eliminacoes estilo FPS."""
    icons = ["☠️", "💀", "🔪", "⚡", "💉", "🎯", "🔥"]
    for killer, victim in entries:
        icon = random.choice(icons)
        sys.stdout.write(
            f"  {Colors.BLOOD}{killer}{Colors.RESET} {icon} "
            f"{Colors.CRIMSON}{victim}{Colors.RESET}\n"
        )
        sys.stdout.flush()
        time.sleep(delay)


def data_exfil_animation(filename: str = "target_data.db", size: str = "2.4GB") -> None:
    """Animacao de exfiltracao de dados."""
    stages = [
        ("ESTABLISHING COVERT CHANNEL", Colors.CYAN),
        ("BYPASSING DLP CONTROLS", Colors.YELLOW),
        ("ENCRYPTING EXFIL STREAM (AES-256-GCM)", Colors.PHANTOM),
        (f"EXFILTRATING {filename} ({size})", Colors.BLOOD),
        ("WIPING FORENSIC TRACES", Colors.ASH),
        ("CHANNEL TERMINATED — CLEAN EXIT", Colors.GREEN),
    ]
    for msg, color in stages:
        sys.stdout.write(f"  {color}▸ {msg}...{Colors.RESET}")
        sys.stdout.flush()
        time.sleep(random.uniform(0.12, 0.35))
        print(f" {Colors.GREEN}✓{Colors.RESET}")


def firewall_bypass_animation(delay: float = 0.1) -> None:
    """Animacao de bypass de firewall."""
    layers = [
        (
            "Layer 1: Perimeter Firewall (pfSense)",
            "WAF FINGERPRINT → BYPASS VIA HTTP/2 DOWNGRADE",
        ),
        ("Layer 2: WAF (Cloudflare)", "UNICODE NORMALIZATION → POLYGLOT PAYLOAD"),
        ("Layer 3: IDS/IPS (Snort)", "FRAGMENTATION + ENCODING → EVASION COMPLETE"),
        ("Layer 4: EDR (CrowdStrike)", "SYSCALL DIRECT → UNHOOK NTDLL → CLEAN"),
        ("Layer 5: HIDS (OSSEC)", "LOG INJECTION → TIMESTOMP → INVISIBLE"),
    ]
    for name, technique in layers:
        sys.stdout.write(f"  {Colors.CRIMSON}⚡ {name}{Colors.RESET}")
        sys.stdout.flush()
        time.sleep(delay * 2)
        sys.stdout.write(f"\n    {Colors.DIM}→ {technique}{Colors.RESET}")
        sys.stdout.flush()
        time.sleep(delay)
        print(f"  {Colors.GREEN}✓ BYPASSED{Colors.RESET}")


def network_map_visual() -> None:
    """Mapa de rede visual ASCII."""
    c = Colors
    print(
        f"""
  {c.CYBER_YELLOW}╔══════════════════════════════════════════════════════════╗{c.RESET}
  {c.CYBER_YELLOW}║{c.RESET}  {c.BLOOD}☠ ATTACK SURFACE MAP — REAL-TIME{c.RESET}                    {c.CYBER_YELLOW}║{c.RESET}
  {c.CYBER_YELLOW}╠══════════════════════════════════════════════════════════╣{c.RESET}
  {c.CYBER_YELLOW}║{c.RESET}        {c.BLOOD}[ATTACKER]{c.RESET}                                  {c.CYBER_YELLOW}║{c.RESET}
  {c.CYBER_YELLOW}║{c.RESET}            │                                          {c.CYBER_YELLOW}║{c.RESET}
  {c.CYBER_YELLOW}║{c.RESET}     ┌──────┼──────┐                                  {c.CYBER_YELLOW}║{c.RESET}
  {c.CYBER_YELLOW}║{c.RESET}     ▼      ▼      ▼                                  {c.CYBER_YELLOW}║{c.RESET}
  {c.CYBER_YELLOW}║{c.RESET}  {c.ORANGE}[WEB]{c.RESET}  {c.CYAN}[API]{c.RESET}  {c.TOXIC}[NET]{c.RESET}                             {c.CYBER_YELLOW}║{c.RESET}
  {c.CYBER_YELLOW}║{c.RESET}   :443   :8080  :22                                  {c.CYBER_YELLOW}║{c.RESET}
  {c.CYBER_YELLOW}║{c.RESET}     └──────┼──────┘                                  {c.CYBER_YELLOW}║{c.RESET}
  {c.CYBER_YELLOW}║{c.RESET}            ▼                                          {c.CYBER_YELLOW}║{c.RESET}
  {c.CYBER_YELLOW}║{c.RESET}     {c.NEON_GREEN}[INTERNAL NET]{c.RESET}                                 {c.CYBER_YELLOW}║{c.RESET}
  {c.CYBER_YELLOW}║{c.RESET}     ┌──────┼──────┬──────┐                           {c.CYBER_YELLOW}║{c.RESET}
  {c.CYBER_YELLOW}║{c.RESET}     ▼      ▼      ▼      ▼                           {c.CYBER_YELLOW}║{c.RESET}
  {c.CYBER_YELLOW}║{c.RESET}  {c.YELLOW}[DB]{c.RESET}  {c.PHANTOM}[AD/DC]{c.RESET} {c.CRIMSON}[SCADA]{c.RESET} {c.GOLD}[VAULT]{c.RESET}                    {c.CYBER_YELLOW}║{c.RESET}
  {c.CYBER_YELLOW}╚══════════════════════════════════════════════════════════╝{c.RESET}
"""
    )


def exploit_chain_visual() -> None:
    """Visualizar cadeia de exploits MITRE ATT&CK."""
    c = Colors
    print(
        f"""
  {c.BLOOD}{c.BOLD}╔══════════════════════════════════════════════════════════════╗
  ║              ⚡ ACTIVE EXPLOIT CHAIN ⚡                      ║
  ╠══════════════════════════════════════════════════════════════╣{c.RESET}
  {c.CRIMSON}  ║  1. INITIAL ACCESS     → Spearphishing (T1566.001)         ║
  ║  2. EXECUTION          → PowerShell (T1059.001)             ║
  ║  3. PERSISTENCE        → Registry Run Key (T1547.001)       ║
  ║  4. PRIV ESCALATION    → Token Impersonation (T1134.001)    ║
  ║  5. DEFENSE EVASION    → Process Injection (T1055)          ║
  ║  6. CREDENTIAL ACCESS  → LSASS Memory (T1003.001)          ║
  ║  7. DISCOVERY          → AD Enumeration (T1087.002)        ║
  ║  8. LATERAL MOVEMENT   → PsExec (T1570)                    ║
  ║  9. COLLECTION         → Archive Collected (T1560.001)      ║
  ║ 10. EXFILTRATION       → C2 Channel (T1041)                ║{c.RESET}
  {c.BLOOD}{c.BOLD}╚══════════════════════════════════════════════════════════════╝{c.RESET}
"""
    )


def vulnerability_heatmap() -> None:
    """Heatmap de vulnerabilidades ASCII."""
    print(
        f"  {Colors.BOLD}{Colors.SKULL}VULNERABILITY HEATMAP — CVSSv4 DISTRIBUTION{Colors.RESET}"
    )
    print(f"  {Colors.DIM}{'─' * 58}{Colors.RESET}")
    categories = [
        ("CRITICAL (9.0-10.0)", 14, Colors.BLOOD),
        ("HIGH     (7.0-8.9) ", 23, Colors.RED),
        ("MEDIUM   (4.0-6.9) ", 18, Colors.YELLOW),
        ("LOW      (0.1-3.9) ", 8, Colors.GREEN),
        ("INFO     (0.0)     ", 5, Colors.CYAN),
    ]
    for label, count, color in categories:
        bar = "█" * count + "░" * (30 - count)
        print(f"  {color}{label} {bar} {count}{Colors.RESET}")


# ════════════════════════════════════════════════════════════════════════════
#  MEGA BANNERS — ASCII WARFARE
# ════════════════════════════════════════════════════════════════════════════

LEVIATHAN_BANNER = f"""{Colors.BLOOD}{Colors.BOLD}
  ╔══════════════════════════════════════════════════════════════════════════╗
  ║                                                                        ║
  ║  ██╗     ███████╗██╗   ██╗██╗ █████╗ ████████╗██╗  ██╗ █████╗ ███╗   ║
  ║  ██║     ██╔════╝██║   ██║██║██╔══██╗╚══██╔══╝██║  ██║██╔══██╗████╗  ║
  ║  ██║     █████╗  ██║   ██║██║███████║   ██║   ███████║███████║██╔██╗ ║
  ║  ██║     ██╔══╝  ╚██╗ ██╔╝██║██╔══██║   ██║   ██╔══██║██╔══██║██║╚██║
  ║  ███████╗███████╗ ╚████╔╝ ██║██║  ██║   ██║   ██║  ██║██║  ██║██║ ╚█║
  ║  ╚══════╝╚══════╝  ╚═══╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝║
  ║                                                                        ║
  ║{Colors.RESET}{Colors.CRIMSON}  ▓▓▓  V U L N E R A B I L I T Y   S O V E R E I G N T Y  ▓▓▓       {Colors.RESET}{Colors.BLOOD}║
  ║                                                                        ║
  ╚══════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""

LEVIATHAN_MINI = f"""{Colors.BLOOD}{Colors.BOLD}
    ██╗     ███████╗██╗   ██╗██╗ █████╗ ████████╗██╗  ██╗ █████╗ ███╗   ██╗
    ██║     ██╔════╝██║   ██║██║██╔══██╗╚══██╔══╝██║  ██║██╔══██╗████╗  ██║
    ██║     █████╗  ██║   ██║██║███████║   ██║   ███████║███████║██╔██╗ ██║
    ██║     ██╔══╝  ╚██╗ ██╔╝██║██╔══██║   ██║   ██╔══██║██╔══██║██║╚██╗██║
    ███████╗███████╗ ╚████╔╝ ██║██║  ██║   ██║   ██║  ██║██║  ██║██║ ╚████║
    ╚══════╝╚══════╝  ╚═══╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝ ╚══╝
{Colors.RESET}"""

SKULL_ART = f"""{Colors.CRIMSON}{Colors.BOLD}
          ██████████████████████████████████
          ██                              ██
          ██   ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄   ██
          ██  █▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█  ██
          ██ █▓▓▓▓█████▓▓▓▓▓█████▓▓▓▓█  ██
          ██ █▓▓▓█{Colors.WHITE}█████{Colors.CRIMSON}█▓▓▓█{Colors.WHITE}█████{Colors.CRIMSON}█▓▓▓█  ██
          ██ █▓▓▓█{Colors.WHITE}█████{Colors.CRIMSON}█▓▓▓█{Colors.WHITE}█████{Colors.CRIMSON}█▓▓▓█  ██
          ██ █▓▓▓▓█████▓▓▓▓▓█████▓▓▓▓█  ██
          ██  █▓▓▓▓▓▓▓▄███▄▓▓▓▓▓▓▓▓█   ██
          ██   █▓▓▓▓███████████▓▓▓▓█    ██
          ██    █▓▓█ █ █ █ █ █▓▓█      ██
          ██     █▓▓█ █ █ █ █▓▓█       ██
          ██      █▓▓▓▓▓▓▓▓▓▓▓█        ██
          ██       ██▓▓▓▓▓▓▓██         ██
          ██         ████████           ██
          ██                              ██
          ██████████████████████████████████
{Colors.RESET}"""

THREAT_GAUGE = f"""
{Colors.BLOOD}{Colors.BOLD}  ╔═══════════════════════════════════════════════════════════════╗
  ║                                                               ║
  ║  ☢️  THREAT LEVEL: {Colors.BLINK}██████████████████████████{Colors.RESET}{Colors.BLOOD}{Colors.BOLD} OMEGA  ☢️      ║
  ║  ☠️  BREACH DEPTH: ████████████████████████     ∞ FATHOMS     ║
  ║  ⚡  ATTACK POWER: █████████████████████████    MAXIMUM       ║
  ║  🎯  ACCURACY:     ████████████████████████░    99.7%%         ║
  ║  🛡️  EVASION RATE: ███████████████████████░░    96.3%%         ║
  ║                                                               ║
  ╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""

THREAT_GAUGE_COMPACT = f"""
{Colors.BLOOD}{Colors.BOLD}  ╔══════════════════════════════════════════════════════════╗
  ║  ☢️  THREAT: {Colors.BLINK}████████████████████{Colors.RESET}{Colors.BLOOD}{Colors.BOLD} OMEGA  |  DEPTH: ∞   ║
  ╚══════════════════════════════════════════════════════════╝{Colors.RESET}
"""

PENTESTER_OATH = f"""{Colors.DIM}{Colors.ITALIC}
  ┌─────────────────────────────────────────────────────────────────┐
  │  "Eu nao quebro sistemas. Eu revelo verdades que eles escondem."│
  │  "Cada vulnerabilidade encontrada e uma vida protegida."        │
  │  "O abismo nao e escuridao. E conhecimento sem filtro."         │
  └─────────────────────────────────────────────────────────────────┘
{Colors.RESET}"""

KILL_CHAIN_MINI = f"""{Colors.CRIMSON}
  RECON → WEAPONIZE → DELIVER → EXPLOIT → INSTALL → C2 → ACTIONS
    ▲         ▲          ▲         ▲         ▲       ▲       ▲
   {Colors.CYAN}OSINT{Colors.CRIMSON}    {Colors.YELLOW}PAYLOAD{Colors.CRIMSON}    {Colors.ORANGE}PHISH{Colors.CRIMSON}    {Colors.RED}0DAY{Colors.CRIMSON}    {Colors.PHANTOM}RAT{Colors.CRIMSON}    {Colors.NEON_GREEN}C2{Colors.CRIMSON}    {Colors.BLOOD}EXFIL{Colors.RESET}
"""

MITRE_MATRIX_MINI = f"""{Colors.BOLD}
  {Colors.BLOOD}╔═══════════════════════════════════════════════════════════════════╗
  ║                    MITRE ATT&CK COVERAGE MAP                    ║
  ╠═══════════════════════════════════════════════════════════════════╣{Colors.RESET}
  {Colors.RED}  TA0001 │ TA0002 │ TA0003 │ TA0004 │ TA0005 │ TA0006 │ TA0007 {Colors.RESET}
  {Colors.CRIMSON}  INIT   │ EXEC   │ PERSIST│ PRIVESC│ EVADE  │ CRED   │ DISCOV {Colors.RESET}
  {Colors.ORANGE}  ██████ │ ██████ │ █████░ │ ██████ │ █████░ │ ████░░ │ ██████ {Colors.RESET}
  {Colors.BLOOD}{Colors.BOLD}  TA0008 │ TA0009 │ TA0010 │ TA0011 │ TA0040 │ TA0042 │ TA0043 {Colors.RESET}
  {Colors.CRIMSON}  LATERAL│ COLLECT│ EXFIL  │ C2     │ IMPACT │ RECON  │ RESDEV {Colors.RESET}
  {Colors.ORANGE}  █████░ │ ████░░ │ ████░░ │ ██████ │ █████░ │ ██████ │ ██████ {Colors.RESET}
  {Colors.BLOOD}{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""


# ════════════════════════════════════════════════════════════════════════════
#  UTILITY FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════


def enable_ansi():
    """Enable ANSI escape sequences on Windows."""
    if os.name == "nt":
        os.system("")
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_ulong()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        except Exception:
            pass


def colorize(text: str, color: str) -> str:
    """Wrap text in ANSI color code."""
    return f"{color}{text}{Colors.RESET}"


def print_separator(char: str = "═", width: int = 75, color: str = "") -> None:
    """Print a styled separator line."""
    if not color:
        color = Colors.CRIMSON
    print(f"  {color}{char * width}{Colors.RESET}")


def print_section(title: str, color: str = "") -> None:
    """Print a dramatic section header with box."""
    if not color:
        color = Colors.BLOOD
    w = 70
    print(f"\n  {color}{Colors.BOLD}╔{'═' * w}╗")
    print(f"  ║  ☠️  {title.upper():<{w - 6}}║")
    print(f"  ╚{'═' * w}╝{Colors.RESET}\n")


def print_status(label: str, value: str, color: str = "") -> None:
    """Print a key-value status line."""
    if not color:
        color = Colors.CRIMSON
    print(f"  {color}{label}:{Colors.RESET} {value}")


def print_threat_indicator(level: str = "OMEGA") -> None:
    """Print inline threat level indicator."""
    levels = {
        "LOW": (Colors.GREEN, "░░░░░░░░░░"),
        "MEDIUM": (Colors.YELLOW, "████░░░░░░"),
        "HIGH": (Colors.ORANGE, "███████░░░"),
        "CRITICAL": (Colors.RED, "█████████░"),
        "OMEGA": (Colors.BLOOD, f"{Colors.BLINK}██████████{Colors.RESET}"),
    }
    color, bar = levels.get(level, levels["OMEGA"])
    print(f"  {color}{Colors.BOLD}THREAT [{bar}] {level}{Colors.RESET}")


def random_hex_string(length: int = 32) -> str:
    """Generate random hex string for visual effect."""
    return "".join(random.choice("0123456789abcdef") for _ in range(length))


def timestamp_military() -> str:
    """Military-style timestamp."""
    import datetime

    now = datetime.datetime.now()
    return now.strftime("%Y%m%d-%H%M%S-") + f"{now.microsecond // 1000:03d}Z"
