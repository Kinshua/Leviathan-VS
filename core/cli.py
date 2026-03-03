#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    ☠️  LEVIATHAN VS — ABYSSAL COMMAND INTERFACE  ☠️
    v66.6.0 ABYSSAL SOVEREIGN | Threat Level: OMEGA

    leviathan <command> [options]

    Commands:
        translate   Kraken Engine — encode/decode/preview/check
        http        Depth Charge — HTTP warfare toolkit
        doctor      Abyss Diagnostic — healthcheck de profundidade
        validate    Config Integrity — validar configs de guerra
        report      Intel Report — exportar relatorio do ambiente
        version     Manifest — mostrar identidade do monstro

    Usage:
        leviathan translate encode --file target.txt
        leviathan doctor --json
        leviathan validate
        leviathan report --format json

    "O abismo nao responde. Ele executa."
================================================================================
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

from .__version__ import __codename__, __threat_level__
from .__version__ import __version__ as VERSION
from .colors import (
    LEVIATHAN_MINI,
    THREAT_GAUGE,
    Colors,
    enable_ansi,
    print_separator,
)

BASE_DIR = Path(__file__).parent.resolve()
PROJECT_DIR = BASE_DIR.parent


# ============================================================================
# SUBCOMMANDS
# ============================================================================


def cmd_translate(args):
    """Delegate to translator.py."""
    from .translator import CLI, SemanticTranslator

    cli = CLI(work_file=args.file)
    action = args.action

    if action == "encode":
        result = cli.translator.encode(preview_only=args.preview)
        if result.success:
            print(f"Encoded: {result.total_replacements} replacements")
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
            print("Nothing to encode (empty or missing file)")
        return 0 if result.success else 1

    elif action == "decode":
        result = cli.translator.decode(preview_only=args.preview)
        if result.success:
            print(f"Decoded: {result.total_replacements} replacements")
        else:
            print("Nothing to decode")
        return 0 if result.success else 1

    elif action == "check":
        clean, count = cli.translator.is_clean()
        if clean:
            print("File is clean — no sensitive terms found")
            return 0
        else:
            print(f"Found {count} sensitive term(s)")
            return 1

    elif action == "stats":
        stats = cli.translator.get_stats()
        if args.json_output:
            print(json.dumps(stats, indent=2))
        else:
            for k, v in stats.items():
                print(f"  {k}: {v}")
        return 0

    elif action == "undo":
        if cli.translator.undo():
            print("Last operation undone")
            return 0
        else:
            print("Nothing to undo")
            return 1

    else:
        print(f"Unknown action: {action}")
        return 1


def cmd_http(args):
    """Delegate to http_toolkit.py."""
    from .http_toolkit import HOGDispatcher

    dispatcher = HOGDispatcher()
    action = args.action

    if action == "dispatch":
        if not args.url:
            print("Error: --url required for dispatch", file=sys.stderr)
            return 1
        result = dispatcher.dispatch(
            url=args.url,
            method=args.method or "GET",
        )
        if args.json_output:
            print(json.dumps(result, indent=2, default=str))
        return 0

    elif action == "scan":
        if not args.url:
            print("Error: --url required for scan", file=sys.stderr)
            return 1
        result = dispatcher.scan(args.url)
        if args.json_output:
            print(json.dumps(result, indent=2, default=str))
        return 0

    else:
        print(f"Unknown action: {action}")
        return 1


def cmd_doctor(args):
    """Run healthcheck."""
    from .doctor import print_report, run_doctor

    report = run_doctor(json_output=args.json_output)
    if args.json_output:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    else:
        print_report(report)
    return report.exit_code


def cmd_validate(args):
    """Validate config files."""
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
    """Export environment report."""
    from .doctor import run_doctor

    report = run_doctor()

    data = {
        "generated": datetime.now().isoformat(),
        "version": VERSION,
        "platform": report.platform,
        "python": report.python_version,
        "project": str(PROJECT_DIR),
        "checks": report.to_dict()["checks"],
        "summary": report.summary,
    }

    if args.format == "json":
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        # Markdown
        lines = [
            f"# LEVIATHAN VS — Environment Report",
            f"",
            f"- **Version**: {VERSION}",
            f"- **Generated**: {data['generated']}",
            f"- **Platform**: {data['platform']}",
            f"- **Python**: {data['python']}",
            f"- **Project**: {data['project']}",
            f"",
            f"## Checks",
            f"",
            f"| Status | Name | Message |",
            f"|--------|------|---------|",
        ]
        for c in data["checks"]:
            lines.append(f"| {c['status'].upper()} | {c['name']} | {c['message']} |")
        lines.extend(
            [
                f"",
                f"## Summary",
                f"",
                f"- OK: {data['summary'].get('ok', 0)}",
                f"- Warnings: {data['summary'].get('warn', 0)}",
                f"- Failures: {data['summary'].get('fail', 0)}",
            ]
        )
        output = "\n".join(lines)

        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"Report saved to {args.output}")
        else:
            print(output)

    return 0


def cmd_version(args):
    """Show version info — manifest of the beast."""
    if args.json_output:
        print(
            json.dumps(
                {
                    "name": "LEVIATHAN VS",
                    "version": VERSION,
                    "codename": __codename__,
                    "threat_level": __threat_level__,
                    "mcp_servers": 49,
                    "tools": "704+",
                    "translation_rules": "640+",
                    "tasks": "180+",
                    "extensions": "160+",
                    "attack_domains": 13,
                    "project": str(PROJECT_DIR),
                    "python": sys.version,
                },
                indent=2,
            )
        )
    else:
        print(LEVIATHAN_MINI)
        print(THREAT_GAUGE)
        print(f"  {Colors.BOLD}{Colors.BLOOD}LEVIATHAN VS{Colors.RESET} v{VERSION}")
        print(f"  {Colors.CRIMSON}Codename:{Colors.RESET}      {__codename__}")
        print(
            f"  {Colors.CRIMSON}Threat Level:{Colors.RESET}   {Colors.BLOOD}{Colors.BOLD}{__threat_level__}{Colors.RESET}"
        )
        print(f"  {Colors.CRIMSON}MCP Servers:{Colors.RESET}    49")
        print(f"  {Colors.CRIMSON}Ferramentas:{Colors.RESET}    704+")
        print(f"  {Colors.CRIMSON}Regras Evasao:{Colors.RESET}  640+")
        print(f"  {Colors.CRIMSON}Tarefas:{Colors.RESET}        180+")
        print(f"  {Colors.CRIMSON}Extensoes:{Colors.RESET}      160+")
        print(f"  {Colors.CRIMSON}Dominios:{Colors.RESET}       13")
        print(f"  {Colors.DIM}Python {sys.version}{Colors.RESET}")
        print(f"  {Colors.DIM}Project: {PROJECT_DIR}{Colors.RESET}")
        print()
        print_separator()
    return 0


# ============================================================================
# MAIN — BOOT SEQUENCE
# ============================================================================


def _boot_sequence():
    """Dramatic boot sequence for the abyss."""
    stages = [
        ("Inicializando nucleo abissal", Colors.CRIMSON),
        ("Carregando 640+ regras de evasao", Colors.BLOOD),
        ("Ativando Tentacle Protocol (49 MCPs)", Colors.CYAN),
        ("Calibrando 704+ ferramentas de ataque", Colors.GREEN),
        ("Profundidade OMEGA alcancada", Colors.BLOOD),
    ]
    for msg, color in stages:
        sys.stdout.write(f"  {color}▸ {msg}...{Colors.RESET}")
        sys.stdout.flush()
        time.sleep(0.08)
        print(f" {Colors.GREEN}✓{Colors.RESET}")


def main():
    enable_ansi()

    # Show mini banner on any command
    if len(sys.argv) > 1 and sys.argv[1] not in ("--help", "-h", "--json"):
        print(
            f"\n  {Colors.BLOOD}{Colors.BOLD}☠️  LEVIATHAN VS v{VERSION} — {__codename__}{Colors.RESET}"
        )
        print(
            f"  {Colors.DIM}Threat Level: {__threat_level__} | 49 MCPs | 704+ Tools{Colors.RESET}\n"
        )

    parser = argparse.ArgumentParser(
        prog="leviathan",
        description="☠️ LEVIATHAN VS — Arsenal Ofensivo Nivel Militar para VS Code",
        epilog='"O abismo nao responde. Ele executa."',
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
        help="Semantic translation (encode/decode/check)",
    )
    p_tr.add_argument("action", choices=["encode", "decode", "check", "stats", "undo"])
    p_tr.add_argument("--file", "-f", default=None, help="Target file")
    p_tr.add_argument(
        "--preview", action="store_true", help="Preview without modifying"
    )
    p_tr.set_defaults(func=cmd_translate)

    # http
    p_http = sub.add_parser("http", help="HTTP toolkit (dispatch/scan)")
    p_http.add_argument("action", choices=["dispatch", "scan"])
    p_http.add_argument("--url", "-u", help="Target URL")
    p_http.add_argument("--method", "-m", default="GET", help="HTTP method")
    p_http.set_defaults(func=cmd_http)

    # doctor
    p_doc = sub.add_parser("doctor", help="Healthcheck & diagnostics")
    p_doc.set_defaults(func=cmd_doctor)

    # validate
    p_val = sub.add_parser("validate", help="Validate config files")
    p_val.set_defaults(func=cmd_validate)

    # report
    p_rep = sub.add_parser("report", help="Export environment report")
    p_rep.add_argument("--format", choices=["json", "markdown"], default="markdown")
    p_rep.add_argument("--output", "-o", help="Output file path")
    p_rep.set_defaults(func=cmd_report)

    # version
    p_ver = sub.add_parser("version", help="Show version info")
    p_ver.set_defaults(func=cmd_version)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
