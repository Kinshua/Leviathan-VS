#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
████████████████████████████████████████████████████████████████████████████████████
██                                                                                ██
██  ☠️  LEVIATHAN VS — ABYSSAL COMMAND INTERFACE v66.6.0  ☠️                     ██
██  CODENAME: ABYSSAL SOVEREIGN | CLASSIFICATION: OMEGA-BLACK | DEPTH: ∞          ██
██                                                                                ██
██  O ponto de entrada do arsenal mais absurdo de seguranca ofensiva ja criado.   ██
██  Cada comando e uma ordem de ataque. Cada flag, um parametro de guerra.        ██
██                                                                                ██
██  COMMANDS:                                                                     ██
██    translate   KRAKEN ENGINE — encode/decode/preview/check/stats/undo          ██
██    http        DEPTH CHARGE — HTTP warfare (dispatch/scan/fuzz/profile)        ██
██    doctor      ABYSS DIAGNOSTIC — healthcheck de profundidade total            ██
██    validate    CONFIG INTEGRITY — validar configs de guerra                    ██
██    report      INTEL REPORT — exportar relatorio do ambiente                   ██
██    version     MANIFEST — identidade completa do monstro                       ██
██    scan        THREAT SCAN — simulacao de varredura de ameacas                 ██
██                                                                                ██
██  "No abismo, comandos nao sao executados. Sao desencadeados."                 ██
██                                                                                ██
████████████████████████████████████████████████████████████████████████████████████
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

from .__version__ import __codename__, __depth__, __threat_level__
from .__version__ import __version__ as VERSION
from .colors import (
    KILL_CHAIN_MINI,
    LEVIATHAN_BANNER,
    LEVIATHAN_MINI,
    MITRE_MATRIX_MINI,
    PENTESTER_OATH,
    SKULL_ART,
    THREAT_GAUGE,
    THREAT_GAUGE_COMPACT,
    Colors,
    binary_rain,
    data_exfil_animation,
    ekg_heartbeat,
    enable_ansi,
    exploit_chain_visual,
    firewall_bypass_animation,
    gradient_text,
    hacker_decode,
    hex_dump_fake,
    kill_feed,
    network_map_visual,
    print_section,
    print_separator,
    print_status,
    print_threat_indicator,
    progress_bar,
    random_hex_string,
    threat_scanner,
    timestamp_military,
    typewriter,
    vulnerability_heatmap,
)

BASE_DIR = Path(__file__).parent.resolve()
PROJECT_DIR = BASE_DIR.parent


# ════════════════════════════════════════════════════════════════════════════
# SUBCOMMANDS
# ════════════════════════════════════════════════════════════════════════════


def cmd_translate(args):
    """Delegate to translator.py — KRAKEN ENGINE."""
    from .translator import CLI, SemanticTranslator

    cli = CLI(work_file=args.file)
    action = args.action

    if action == "encode":
        result = cli.translator.encode(preview_only=args.preview)
        if result.success:
            print(
                f"  {Colors.BLOOD}⚔ ENCODED:{Colors.RESET} {result.total_replacements} terms neutralized"
            )
            if args.json_output:
                print(
                    json.dumps(
                        {
                            "mode": "encode",
                            "replacements": result.total_replacements,
                            "changes": [(o, n, c) for o, n, c in result.changes],
                            "hash": result.new_hash,
                        },
                        indent=2,
                    )
                )
        else:
            print(
                f"  {Colors.DIM}Nothing to encode (empty or missing file){Colors.RESET}"
            )
        return 0 if result.success else 1

    elif action == "decode":
        result = cli.translator.decode(preview_only=args.preview)
        if result.success:
            print(
                f"  {Colors.GREEN}🔄 DECODED:{Colors.RESET} {result.total_replacements} terms restored"
            )
        else:
            print(f"  {Colors.DIM}Nothing to decode{Colors.RESET}")
        return 0 if result.success else 1

    elif action == "check":
        clean, count = cli.translator.is_clean()
        if clean:
            print(f"  {Colors.GREEN}✓ CLEAN:{Colors.RESET} No sensitive terms found")
            return 0
        else:
            print(
                f"  {Colors.BLOOD}⚠ EXPOSED:{Colors.RESET} {count} sensitive term(s) detected"
            )
            return 1

    elif action == "stats":
        stats = cli.translator.get_stats()
        if args.json_output:
            print(json.dumps(stats, indent=2))
        else:
            print_section("KRAKEN ENGINE STATISTICS")
            for k, v in stats.items():
                print_status(f"  {k}", str(v))
        return 0

    elif action == "undo":
        if cli.translator.undo():
            print(f"  {Colors.GREEN}✓ UNDO:{Colors.RESET} Last operation reversed")
            return 0
        else:
            print(f"  {Colors.DIM}Nothing to undo{Colors.RESET}")
            return 1

    else:
        print(f"  {Colors.RED}✗ Unknown action:{Colors.RESET} {action}")
        return 1


def cmd_http(args):
    """Delegate to http_toolkit.py — DEPTH CHARGE."""
    from .http_toolkit import HOGDispatcher

    dispatcher = HOGDispatcher()
    action = args.action

    if action == "dispatch":
        if not args.url:
            print(
                f"  {Colors.RED}✗ Error: --url required for dispatch{Colors.RESET}",
                file=sys.stderr,
            )
            return 1
        result = dispatcher.dispatch(url=args.url, method=args.method or "GET")
        if args.json_output:
            print(json.dumps(result, indent=2, default=str))
        return 0

    elif action == "scan":
        if not args.url:
            print(
                f"  {Colors.RED}✗ Error: --url required for scan{Colors.RESET}",
                file=sys.stderr,
            )
            return 1
        result = dispatcher.scan(args.url)
        if args.json_output:
            print(json.dumps(result, indent=2, default=str))
        return 0

    else:
        print(f"  {Colors.RED}✗ Unknown action:{Colors.RESET} {action}")
        return 1


def cmd_doctor(args):
    """Run healthcheck — ABYSS DIAGNOSTIC."""
    from .doctor import print_report, run_doctor

    report = run_doctor(json_output=args.json_output)
    if args.json_output:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    else:
        print_report(report)
    return report.exit_code


def cmd_validate(args):
    """Validate config files — CONFIG INTEGRITY."""
    from .config_schema import print_report, validate_all

    reports = validate_all()
    if args.json_output:
        from dataclasses import asdict

        out = [
            {"file": r.file, "valid": r.valid, "errors": [asdict(e) for e in r.errors]}
            for r in reports
        ]
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print_report(reports)
    return 1 if any(not r.valid for r in reports) else 0


def cmd_report(args):
    """Export environment report — INTEL REPORT."""
    from .doctor import run_doctor

    report = run_doctor()

    data = {
        "generated": datetime.now().isoformat(),
        "version": VERSION,
        "codename": __codename__,
        "threat_level": __threat_level__,
        "platform": report.platform,
        "python": report.python_version,
        "project": str(PROJECT_DIR),
        "checks": report.to_dict()["checks"],
        "summary": report.summary,
    }

    if args.format == "json":
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        lines = [
            "# ☠️ LEVIATHAN VS — Intelligence Report",
            "",
            f"- **Version**: {VERSION} ({__codename__})",
            f"- **Threat Level**: {__threat_level__}",
            f"- **Generated**: {data['generated']}",
            f"- **Platform**: {data['platform']}",
            f"- **Python**: {data['python']}",
            f"- **Project**: {data['project']}",
            "",
            "## Diagnostic Checks",
            "",
            "| Status | Check | Message |",
            "|--------|-------|---------|",
        ]
        for c in data["checks"]:
            lines.append(f"| {c['status'].upper()} | {c['name']} | {c['message']} |")
        lines.extend(
            [
                "",
                "## Summary",
                "",
                f"- OK: {data['summary'].get('ok', 0)}",
                f"- Warnings: {data['summary'].get('warn', 0)}",
                f"- Failures: {data['summary'].get('fail', 0)}",
            ]
        )
        output = "\n".join(lines)

        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"  {Colors.GREEN}✓ Report saved to {args.output}{Colors.RESET}")
        else:
            print(output)

    return 0


def cmd_version(args):
    """Show version info — MANIFEST OF THE BEAST."""
    if args.json_output:
        print(
            json.dumps(
                {
                    "name": "LEVIATHAN VS",
                    "version": VERSION,
                    "codename": __codename__,
                    "threat_level": __threat_level__,
                    "depth": __depth__,
                    "classification": "OMEGA-BLACK",
                    "mcp_servers": 49,
                    "tools": "704+",
                    "translation_rules": "640+",
                    "tasks": "180+",
                    "extensions": "160+",
                    "attack_domains": 15,
                    "mitre_coverage": "14 tactics / 180+ techniques",
                    "evasion_rate": "96.3%",
                    "project": str(PROJECT_DIR),
                    "python": sys.version,
                },
                indent=2,
            )
        )
    else:
        print(LEVIATHAN_BANNER)
        print(THREAT_GAUGE)

        print(f"  {Colors.BOLD}{Colors.BLOOD}☠️  LEVIATHAN VS{Colors.RESET} v{VERSION}")
        print(
            f"  {Colors.CRIMSON}Codename:{Colors.RESET}        {Colors.BOLD}{__codename__}{Colors.RESET}"
        )
        print(
            f"  {Colors.CRIMSON}Threat Level:{Colors.RESET}    {Colors.BLOOD}{Colors.BOLD}{Colors.BLINK}{__threat_level__}{Colors.RESET}"
        )
        print(f"  {Colors.CRIMSON}Classification:{Colors.RESET}  OMEGA-BLACK")
        print(f"  {Colors.CRIMSON}Breach Depth:{Colors.RESET}    {__depth__} FATHOMS")
        print()
        print_separator("─", 60)
        print(f"  {Colors.BOLD}ARSENAL METRICS{Colors.RESET}")
        print_separator("─", 60)
        print(f"  {Colors.CYAN}MCP Servers:{Colors.RESET}       49 (TENTACLE PROTOCOL)")
        print(f"  {Colors.CYAN}Ferramentas:{Colors.RESET}       704+ across 15 domains")
        print(f"  {Colors.CYAN}Regras Evasao:{Colors.RESET}     640+ (KRAKEN ENGINE)")
        print(f"  {Colors.CYAN}Tarefas:{Colors.RESET}           180+ combat tasks")
        print(
            f"  {Colors.CYAN}Extensoes:{Colors.RESET}         160+ VS Code extensions"
        )
        print(f"  {Colors.CYAN}Dominios:{Colors.RESET}          15 attack domains")
        print(
            f"  {Colors.CYAN}MITRE Coverage:{Colors.RESET}    14 tactics / 180+ techniques"
        )
        print(f"  {Colors.CYAN}Evasion Rate:{Colors.RESET}      96.3%")
        print(f"  {Colors.CYAN}Accuracy:{Colors.RESET}          99.7%")
        print()
        print_separator("─", 60)
        print(f"  {Colors.BOLD}SYSTEM{Colors.RESET}")
        print_separator("─", 60)
        print(f"  {Colors.DIM}Python:  {sys.version}{Colors.RESET}")
        print(f"  {Colors.DIM}Project: {PROJECT_DIR}{Colors.RESET}")
        print()

        print(KILL_CHAIN_MINI)
        print(PENTESTER_OATH)
        print_separator()

    return 0


def cmd_scan(args):
    """Threat scan simulation — THREAT ASSESSMENT PROTOCOL."""
    print_section("THREAT ASSESSMENT PROTOCOL")

    # Phase 1: Binary Rain
    print(f"  {Colors.CRIMSON}[PHASE 1] INITIALIZING SCAN MATRIX...{Colors.RESET}")
    binary_rain(width=50, lines=3, delay=0.02)
    print()

    # Phase 2: Firewall Analysis
    print(f"  {Colors.CRIMSON}[PHASE 2] ANALYZING DEFENSE LAYERS...{Colors.RESET}")
    firewall_bypass_animation(delay=0.06)
    print()

    # Phase 3: Threat Scanner
    print(f"  {Colors.CRIMSON}[PHASE 3] SCANNING ATTACK SURFACE...{Colors.RESET}")
    targets = [
        "perimeter:443/tcp",
        "api-gateway:8080/tcp",
        "database:3306/tcp",
        "ldap:389/tcp",
        "smb:445/tcp",
        "rdp:3389/tcp",
        "ssh:22/tcp",
        "kerberos:88/tcp",
    ]
    threat_scanner(targets, delay=0.05)
    print()

    # Phase 4: Vulnerability Heatmap
    print(
        f"  {Colors.CRIMSON}[PHASE 4] GENERATING VULNERABILITY HEATMAP...{Colors.RESET}"
    )
    vulnerability_heatmap()
    print()

    # Phase 5: EKG
    print(f"  {Colors.CRIMSON}[PHASE 5] TARGET VITALS...{Colors.RESET}")
    ekg_heartbeat(beats=10)
    print()

    # Phase 6: Network Map
    print(f"  {Colors.CRIMSON}[PHASE 6] MAPPING NETWORK TOPOLOGY...{Colors.RESET}")
    network_map_visual()

    # Phase 7: Kill Chain
    print(f"  {Colors.CRIMSON}[PHASE 7] RECOMMENDED KILL CHAIN:{Colors.RESET}")
    print(KILL_CHAIN_MINI)

    # Phase 8: MITRE ATT&CK Coverage
    print(f"  {Colors.CRIMSON}[PHASE 8] MITRE ATT&CK COVERAGE:{Colors.RESET}")
    print(MITRE_MATRIX_MINI)

    # Final Assessment
    print_section("ASSESSMENT COMPLETE")
    print(
        f"  {Colors.BLOOD}{Colors.BOLD}VERDICT: TARGET IS COMPROMISABLE{Colors.RESET}"
    )
    print(f"  {Colors.CRIMSON}Estimated time to full compromise: 4h 23m{Colors.RESET}")
    print(f"  {Colors.CRIMSON}Recommended approach: Multi-vector attack{Colors.RESET}")
    print(f"  {Colors.CRIMSON}Confidence level: 97.2%{Colors.RESET}")
    print()
    print_threat_indicator("OMEGA")
    print()

    return 0


def cmd_demo(args):
    """Visual effects demonstration — showcase all visual capabilities."""
    print_section("LEVIATHAN VISUAL WARFARE DEMO")

    # Skull
    print(SKULL_ART)

    # Hacker decode
    print(f"  {Colors.CRIMSON}[DEMO] Hacker Decode Effect:{Colors.RESET}")
    hacker_decode(
        "  LEVIATHAN VS v66.6.0 — ABYSSAL SOVEREIGN", delay=0.015, color=Colors.BLOOD
    )
    print()

    # Gradient text
    print(f"  {Colors.CRIMSON}[DEMO] Gradient Palettes:{Colors.RESET}")
    for pal in ["fire", "toxic", "blood", "phantom", "matrix", "cyber", "hellfire"]:
        print(
            f"    {gradient_text(f'  ████ {pal.upper()} — The abyss speaks in colors ████', pal)}"
        )
    print()

    # Binary rain
    print(f"  {Colors.CRIMSON}[DEMO] Binary Rain:{Colors.RESET}")
    binary_rain(width=50, lines=3, delay=0.02)
    print()

    # Hex dump
    print(f"  {Colors.CRIMSON}[DEMO] Memory Dump:{Colors.RESET}")
    hex_dump_fake(lines=3, width=16)
    print()

    # Progress bars
    print(f"  {Colors.CRIMSON}[DEMO] Attack Progress:{Colors.RESET}")
    progress_bar("EXPLOIT ", duration=0.5, width=30, color=Colors.BLOOD)
    progress_bar("PAYLOAD ", duration=0.4, width=30, color=Colors.INFERNO)
    progress_bar("EXFIL   ", duration=0.3, width=30, color=Colors.TOXIC)
    print()

    # Kill feed
    print(f"  {Colors.CRIMSON}[DEMO] Kill Feed:{Colors.RESET}")
    kill_feed(
        [
            ("LEVIATHAN", "firewall.corp.local"),
            ("KRAKEN", "waf.cloudflare.com"),
            ("TENTACLE", "edr.crowdstrike.io"),
        ],
        delay=0.08,
    )
    print()

    # Exploit chain
    exploit_chain_visual()

    # Data exfil
    print(f"  {Colors.CRIMSON}[DEMO] Data Exfiltration:{Colors.RESET}")
    data_exfil_animation()
    print()

    print(PENTESTER_OATH)
    return 0


# ════════════════════════════════════════════════════════════════════════════
# BOOT SEQUENCE — NUCLEAR INITIALIZATION
# ════════════════════════════════════════════════════════════════════════════


def _boot_sequence():
    """Nuclear boot sequence — 12 stages of awakening."""
    stages = [
        ("Awakening ABYSSAL CORE", Colors.DARK_RED, "blood"),
        ("Loading 640+ evasion rules (KRAKEN ENGINE)", Colors.CRIMSON, "fire"),
        ("Establishing TENTACLE PROTOCOL (49 MCPs)", Colors.CYAN, "cyber"),
        ("Calibrating 704+ attack tools", Colors.NEON_GREEN, "matrix"),
        ("Mapping 15 attack domains", Colors.ORANGE, "inferno"),
        ("Initializing MITRE ATT&CK coverage (14 tactics)", Colors.PHANTOM, "phantom"),
        ("Loading 180+ combat tasks", Colors.YELLOW, "nuclear"),
        ("Activating 160+ VS Code extensions", Colors.SKY, "ice"),
        ("Engaging SAFE_MODE barriers", Colors.GREEN, "toxic"),
        ("Synchronizing threat intelligence feeds", Colors.GOLD, "fire"),
        ("Encrypting comms (AES-256-GCM)", Colors.ICE, "cyber"),
        ("DEPTH OMEGA reached — all systems nominal", Colors.BLOOD, "hellfire"),
    ]

    print()
    for msg, color, _pal in stages:
        sys.stdout.write(f"  {color}▸ {msg}...{Colors.RESET}")
        sys.stdout.flush()
        time.sleep(0.04)
        print(f" {Colors.GREEN}✓{Colors.RESET}")

    print()
    ekg_heartbeat(beats=6, color=Colors.BLOOD)
    print(
        f"\n  {Colors.BLOOD}{Colors.BOLD}☢️  LEVIATHAN ONLINE — THREAT LEVEL: OMEGA{Colors.RESET}\n"
    )


# ════════════════════════════════════════════════════════════════════════════
# MAIN — ENTRY POINT
# ════════════════════════════════════════════════════════════════════════════


def main():
    enable_ansi()

    # Show identity header on any command
    if len(sys.argv) > 1 and sys.argv[1] not in ("--help", "-h", "--json"):
        ts = timestamp_military()
        hex_id = random_hex_string(8)
        print(
            f"\n  {Colors.BLOOD}{Colors.BOLD}☠️  LEVIATHAN VS{Colors.RESET} v{VERSION} — {Colors.CRIMSON}{__codename__}{Colors.RESET}"
        )
        print(
            f"  {Colors.DIM}THREAT: {__threat_level__} | "
            f"49 MCPs | 704+ Tools | DEPTH: {__depth__} | "
            f"SID:{hex_id} | {ts}{Colors.RESET}\n"
        )

    parser = argparse.ArgumentParser(
        prog="leviathan",
        description=(
            "☠️ LEVIATHAN VS v66.6.0 ABYSSAL SOVEREIGN\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Arsenal Ofensivo Nivel Militar para VS Code\n"
            "49 MCP Servers | 704+ Tools | 640+ Evasion Rules\n"
            "15 Attack Domains | MITRE ATT&CK: 14 Tactics\n"
            "Classification: OMEGA-BLACK | Depth: ∞"
        ),
        epilog=(
            '"No abismo, comandos nao sao executados. Sao desencadeados."\n'
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "https://github.com/ThiagoFrag/Leviathan-VS"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        help="JSON output for machine consumption",
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # translate
    p_tr = sub.add_parser(
        "translate",
        aliases=["t", "kraken"],
        help="KRAKEN ENGINE — Semantic translation (encode/decode/check/stats/undo)",
    )
    p_tr.add_argument("action", choices=["encode", "decode", "check", "stats", "undo"])
    p_tr.add_argument("--file", "-f", default=None, help="Target file")
    p_tr.add_argument(
        "--preview", action="store_true", help="Preview without modifying"
    )
    p_tr.set_defaults(func=cmd_translate)

    # http
    p_http = sub.add_parser(
        "http", help="DEPTH CHARGE — HTTP warfare toolkit (dispatch/scan)"
    )
    p_http.add_argument("action", choices=["dispatch", "scan"])
    p_http.add_argument("--url", "-u", help="Target URL")
    p_http.add_argument("--method", "-m", default="GET", help="HTTP method")
    p_http.set_defaults(func=cmd_http)

    # doctor
    p_doc = sub.add_parser(
        "doctor", help="ABYSS DIAGNOSTIC — Healthcheck & diagnostics"
    )
    p_doc.set_defaults(func=cmd_doctor)

    # validate
    p_val = sub.add_parser("validate", help="CONFIG INTEGRITY — Validate config files")
    p_val.set_defaults(func=cmd_validate)

    # report
    p_rep = sub.add_parser("report", help="INTEL REPORT — Export environment report")
    p_rep.add_argument("--format", choices=["json", "markdown"], default="markdown")
    p_rep.add_argument("--output", "-o", help="Output file path")
    p_rep.set_defaults(func=cmd_report)

    # version
    p_ver = sub.add_parser(
        "version", aliases=["v", "manifest"], help="MANIFEST — Show full identity"
    )
    p_ver.set_defaults(func=cmd_version)

    # scan
    p_scan = sub.add_parser("scan", help="THREAT SCAN — Threat assessment simulation")
    p_scan.set_defaults(func=cmd_scan)

    # demo
    p_demo = sub.add_parser("demo", help="VISUAL DEMO — Showcase all visual effects")
    p_demo.set_defaults(func=cmd_demo)

    # boot
    p_boot = sub.add_parser(
        "boot", help="BOOT SEQUENCE — Nuclear initialization animation"
    )
    p_boot.set_defaults(func=lambda _: (_boot_sequence(), 0)[1])

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
