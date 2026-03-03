#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    ☠️  LEVIATHAN VS — ABYSS COLOR ENGINE  ☠️

    Paleta de cores do abismo. Cada cor e uma profundidade.
    Cada gradiente e uma ameaca. Cada efeito e um aviso.

    Usage:
        from colors import Colors, Fx, gradient_text, LEVIATHAN_BANNER
        print(LEVIATHAN_BANNER)
        print(gradient_text("SISTEMA ONLINE", "fire"))
        print(f"{Colors.BLOOD}CRITICO{Colors.RESET}")
================================================================================
"""

import os
import sys
import time


class Colors:
    """ANSI escape codes — Paleta Abissal."""

    # === BASICS ===
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    RESET = "\033[0m"

    # === BACKGROUNDS ===
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_BLACK = "\033[40m"
    BG_DARK = "\033[48;5;233m"

    # === ABYSS PALETTE (256 colors) ===
    BLOOD = "\033[38;5;196m"  # Vermelho sangue
    CRIMSON = "\033[38;5;160m"  # Carmesim profundo
    INFERNO = "\033[38;5;202m"  # Laranja infernal
    TOXIC = "\033[38;5;118m"  # Verde toxico
    ACID = "\033[38;5;46m"  # Verde acido
    NEON_GREEN = "\033[38;5;82m"  # Verde neon matrix
    ABYSS_BLUE = "\033[38;5;21m"  # Azul abissal
    DEEP_PURPLE = "\033[38;5;93m"  # Roxo profundo
    PHANTOM = "\033[38;5;141m"  # Roxo fantasma
    GHOST = "\033[38;5;250m"  # Cinza espectral
    VOID = "\033[38;5;232m"  # Vazio (quase preto)
    GOLD = "\033[38;5;220m"  # Ouro
    CORAL = "\033[38;5;203m"  # Coral
    SKY = "\033[38;5;117m"  # Ceu
    PINK = "\033[38;5;213m"  # Rosa
    ORANGE = "\033[38;5;208m"  # Laranja
    LIME = "\033[38;5;118m"  # Lima
    TEAL = "\033[38;5;43m"  # Teal
    SKULL = "\033[38;5;255m"  # Branco cranio

    # === TRUE COLOR (24-bit) ===
    LAVA = "\033[38;2;255;69;0m"
    OCEAN_DEEP = "\033[38;2;0;20;60m"
    PLASMA = "\033[38;2;180;0;255m"
    MATRIX = "\033[38;2;0;255;65m"
    MIDNIGHT = "\033[38;2;25;25;112m"


class Fx:
    """Efeitos especiais de terminal."""

    CLEAR = "\033[2J\033[H"
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"
    SAVE_POS = "\033[s"
    RESTORE_POS = "\033[u"

    @staticmethod
    def move_to(row: int, col: int) -> str:
        return f"\033[{row};{col}H"

    @staticmethod
    def up(n: int = 1) -> str:
        return f"\033[{n}A"

    @staticmethod
    def clear_line() -> str:
        return "\033[2K"


# === GRADIENT ENGINE ===

_GRADIENTS = {
    "fire": [(255, 0, 0), (255, 100, 0), (255, 200, 0), (255, 255, 0)],
    "ocean": [(0, 20, 80), (0, 60, 140), (0, 120, 200), (0, 200, 255)],
    "toxic": [(0, 80, 0), (0, 160, 0), (0, 255, 0), (100, 255, 100)],
    "blood": [(80, 0, 0), (160, 0, 0), (220, 0, 0), (255, 50, 50)],
    "phantom": [(60, 0, 80), (100, 0, 160), (140, 0, 220), (180, 80, 255)],
    "matrix": [(0, 40, 0), (0, 100, 0), (0, 200, 0), (0, 255, 65)],
    "skull": [(80, 80, 80), (140, 140, 140), (200, 200, 200), (255, 255, 255)],
    "abyss": [(0, 0, 40), (0, 0, 100), (20, 0, 160), (60, 0, 255)],
}


def _interp(c1: tuple, c2: tuple, t: float) -> tuple:
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def gradient_text(text: str, palette: str = "fire") -> str:
    """Renderiza texto com gradiente de cores."""
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


def typewriter(text: str, delay: float = 0.02, color: str = "") -> None:
    """Efeito de digitacao no terminal."""
    for ch in text:
        sys.stdout.write(f"{color}{ch}{Colors.RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()


# === LEVIATHAN BANNERS ===

LEVIATHAN_BANNER = f"""{Colors.BLOOD}{Colors.BOLD}
  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
  ██                                                                         ██
  ██  ██╗     ███████╗██╗   ██╗██╗ █████╗ ████████╗██╗  ██╗ █████╗ ███╗   ████
  ██  ██║     ██╔════╝██║   ██║██║██╔══██╗╚══██╔══╝██║  ██║██╔══██╗████╗  ████
  ██  ██║     █████╗  ██║   ██║██║███████║   ██║   ███████║███████║██╔██╗ ████
  ██  ██║     ██╔══╝  ╚██╗ ██╔╝██║██╔══██║   ██║   ██╔══██║██╔══██║██║╚██╗████
  ██  ███████╗███████╗ ╚████╔╝ ██║██║  ██║   ██║   ██║  ██║██║  ██║██║ ╚██████
  ██  ╚══════╝╚══════╝  ╚═══╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝ ████
  ██                                                                         ██
  ██{Colors.RESET}{Colors.CRIMSON}  ▓▓▓  V U L N E R A B I L I T Y   S O V E R E I G N T Y  ▓▓▓       {Colors.RESET}{Colors.BLOOD}██
  ██                                                                         ██
  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
{Colors.RESET}"""

LEVIATHAN_MINI = f"""{Colors.BLOOD}{Colors.BOLD}
    ██╗     ███████╗██╗   ██╗██╗ █████╗ ████████╗██╗  ██╗ █████╗ ███╗   ██╗
    ██║     ██╔════╝██║   ██║██║██╔══██╗╚══██╔══╝██║  ██║██╔══██╗████╗  ██║
    ██║     █████╗  ██║   ██║██║███████║   ██║   ███████║███████║██╔██╗ ██║
    ██║     ██╔══╝  ╚██╗ ██╔╝██║██╔══██║   ██║   ██╔══██║██╔══██║██║╚██╗██║
    ███████╗███████╗ ╚████╔╝ ██║██║  ██║   ██║   ██║  ██║██║  ██║██║ ╚████║
    ╚══════╝╚══════╝  ╚═══╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
{Colors.RESET}"""

SKULL_ART = f"""{Colors.CRIMSON}
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ░░░░░▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄░░░░░░░
        ░░░▄█▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▄░░░░░
        ░░█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█░░░░
        ░█▓▓▓█▀░░▀▓▓▓▀░░▀█▓▓▓█░░░
        ░█▓▓▓░░{Colors.WHITE}▄█▓{Colors.CRIMSON}░▓▓▓░{Colors.WHITE}▓█▄{Colors.CRIMSON}░░▓▓▓█░░░
        ░█▓▓▓░{Colors.WHITE}████{Colors.CRIMSON}░▓▓▓░{Colors.WHITE}████{Colors.CRIMSON}░▓▓▓█░░░
        ░░█▓▓░░░░░▄▓▓▓▄░░░░░▓▓█░░░░
        ░░░█▓▓▓▓▓████████▓▓▓▓█░░░░░
        ░░░░█▓▓░░█░█░█░█░░▓▓█░░░░░░
        ░░░░░█▓▓░░▀▀▀▀▀░░▓▓█░░░░░░░
        ░░░░░░▀█▓▓▓▓▓▓▓▓▓█▀░░░░░░░░
        ░░░░░░░░░▀▀▀▀▀▀▀░░░░░░░░░░░
{Colors.RESET}"""

THREAT_GAUGE = f"""
{Colors.BLOOD}{Colors.BOLD}    ╔══════════════════════════════════════════════════════╗
    ║  ☢️  THREAT LEVEL: {Colors.BLINK}█████████████████████{Colors.RESET}{Colors.BLOOD}{Colors.BOLD} OMEGA  ☢️  ║
    ╚══════════════════════════════════════════════════════╝{Colors.RESET}
"""


def enable_ansi():
    """Enable ANSI escape sequences on Windows — awaken the abyss."""
    if os.name == "nt":
        os.system("")
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass


def colorize(text: str, color: str) -> str:
    """Wrap text in the given ANSI color code."""
    return f"{color}{text}{Colors.RESET}"


def print_separator(
    char: str = "═", width: int = 75, color: str = Colors.CRIMSON
) -> None:
    """Print a styled separator line."""
    print(f"{color}{char * width}{Colors.RESET}")


def print_section(title: str, color: str = Colors.BLOOD) -> None:
    """Print a dramatic section header."""
    w = 75
    print(f"\n{color}{Colors.BOLD}{'═' * w}")
    print(f"  ☠️  {title.upper()}")
    print(f"{'═' * w}{Colors.RESET}\n")
