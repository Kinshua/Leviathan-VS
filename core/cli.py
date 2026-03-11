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
██    pentest     SIREN ENGINE — autonomous AI pentest pipeline                  ██
██    auth        SIREN AUTH — authentication attack engine                      ██
██    crypto      SIREN CRYPTO — cryptographic attack engine                     ██
██    workspace   SIREN WORKSPACE — workspaces, checkpoints, config              ██
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
                    "classification": "OMEGA-ULTRABLACK",
                    "mcp_servers": 50,
                    "tools": "711+",
                    "translation_rules": "640+",
                    "tasks": "180+",
                    "extensions": "160+",
                    "attack_domains": 16,
                    "mitre_coverage": "14 tactics / 180+ techniques",
                    "evasion_rate": "97.1%",
                    "shannon_agents": 13,
                    "pipeline_phases": 5,
                    "ai_model_tiers": 3,
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
        print(f"  {Colors.CRIMSON}Classification:{Colors.RESET}  OMEGA-ULTRABLACK")
        print(f"  {Colors.CRIMSON}Breach Depth:{Colors.RESET}    {__depth__} FATHOMS")
        print()
        print_separator("─", 60)
        print(f"  {Colors.BOLD}ARSENAL METRICS{Colors.RESET}")
        print_separator("─", 60)
        print(
            f"  {Colors.CYAN}MCP Servers:{Colors.RESET}       50 (TENTACLE + ABYSSAL)"
        )
        print(f"  {Colors.CYAN}Ferramentas:{Colors.RESET}       711+ across 16 domains")
        print(f"  {Colors.CYAN}Regras Evasao:{Colors.RESET}     640+ (KRAKEN ENGINE)")
        print(f"  {Colors.CYAN}Tarefas:{Colors.RESET}           180+ combat tasks")
        print(
            f"  {Colors.CYAN}Extensoes:{Colors.RESET}         160+ VS Code extensions"
        )
        print(f"  {Colors.CYAN}Dominios:{Colors.RESET}          16 attack domains")
        print(
            f"  {Colors.CYAN}MITRE Coverage:{Colors.RESET}    14 tactics / 180+ techniques"
        )
        print(f"  {Colors.CYAN}Evasion Rate:{Colors.RESET}      97.1%")
        print(f"  {Colors.CYAN}Accuracy:{Colors.RESET}          99.8%")
        print()
        print_separator("─", 60)
        print(f"  {Colors.BOLD}⚡ SHANNON ENGINE{Colors.RESET}")
        print_separator("─", 60)
        print(f"  {Colors.CYAN}AI Agents:{Colors.RESET}         13 autonomous agents")
        print(
            f"  {Colors.CYAN}Pipeline:{Colors.RESET}          5-phase (pre-recon → report)"
        )
        print(f"  {Colors.CYAN}AI Tiers:{Colors.RESET}          3 (haiku/sonnet/opus)")
        print(
            f"  {Colors.CYAN}Origin:{Colors.RESET}            KeygraphHQ/shannon (AGPL-3.0)"
        )
        print(f"  {Colors.CYAN}Kill Chain:{Colors.RESET}        FULL+AI (autonomous)")
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


def cmd_pentest(args):
    """SIREN ENGINE — Shannon Intelligence Recon & Exploitation Nexus."""
    import asyncio

    action = args.action

    if action == "start":
        if not args.target or not args.repo:
            print(
                f"  {Colors.RED}✗ --target and --repo are required{Colors.RESET}",
                file=sys.stderr,
            )
            return 1

        print_section("SIREN — Shannon Intelligence Recon & Exploitation Nexus")
        print(
            f"  {Colors.BLOOD}⚡ SIREN online. Initiating autonomous pipeline...{Colors.RESET}"
        )
        print(f"  {Colors.CRIMSON}Target:{Colors.RESET}    {args.target}")
        print(f"  {Colors.CRIMSON}Repo:{Colors.RESET}      {args.repo}")
        print(f"  {Colors.CRIMSON}Workspace:{Colors.RESET} {args.workspace or 'auto'}")
        print()

        from .shannon.engine import AbyssalEngine, EngineConfig
        from .shannon.reporter import AbyssalReporter

        workspace = args.workspace or datetime.now().strftime("audit_%Y%m%d_%H%M%S")
        config = EngineConfig(
            target_url=args.target,
            repo_path=args.repo,
            output_dir=args.output or "./audit-logs",
            workspace=workspace,
            auth_login_url=getattr(args, "auth_url", None),
            auth_username=getattr(args, "auth_user", None),
            enable_kraken_evasion=not getattr(args, "no_kraken", False),
            enable_safe_mode=not getattr(args, "unsafe", False),
            pipeline_testing=getattr(args, "testing", False),
        )

        engine = AbyssalEngine(config)

        # Preflight
        print(
            f"  {Colors.CYAN}▸ Running preflight checks...{Colors.RESET}",
            end="",
            flush=True,
        )
        preflight = asyncio.run(engine.preflight())
        if preflight["valid"]:
            print(f" {Colors.GREEN}✓{Colors.RESET}")
        else:
            print(f" {Colors.RED}✗{Colors.RESET}")
            for check in preflight["checks"]:
                if check.get("status") == "fail":
                    print(
                        f"    {Colors.RED}✗ {check['name']}: {check.get('error', 'failed')}{Colors.RESET}"
                    )
            return 1

        # Pipeline execution
        print(
            f"  {Colors.CYAN}▸ Executing 5-phase pipeline (13 agents)...{Colors.RESET}"
        )
        phases = [
            "Pre-Recon",
            "Recon",
            "Vuln Analysis (5 parallel)",
            "Exploitation (5 parallel)",
            "Reporting",
        ]
        for i, phase in enumerate(phases, 1):
            print(f"    {Colors.CRIMSON}Phase {i}: {phase}{Colors.RESET}")

        print()
        try:
            result = engine.run_sync()

            # Generate report
            reporter = AbyssalReporter(
                pipeline_result=result,
                output_dir=config.output_dir,
                target_url=config.target_url,
                workspace=workspace,
            )
            paths = reporter.save_report()

            print()
            print_section("PIPELINE COMPLETE")
            print(f"  {Colors.GREEN}✓ State:{Colors.RESET}       {result.state.value}")
            print(
                f"  {Colors.GREEN}✓ Phases:{Colors.RESET}      {result.phases_completed}"
            )
            print(
                f"  {Colors.GREEN}✓ Succeeded:{Colors.RESET}   {result.agents_succeeded}"
            )
            print(
                f"  {Colors.GREEN}✓ Failed:{Colors.RESET}      {result.agents_failed}"
            )
            print(
                f"  {Colors.GREEN}✓ Duration:{Colors.RESET}    {result.total_duration_ms / 1000:.2f}s"
            )
            print()
            print(f"  {Colors.CYAN}Report:{Colors.RESET}  {paths['report']}")
            print(f"  {Colors.CYAN}Metrics:{Colors.RESET} {paths['metrics']}")
            print(f"  {Colors.CYAN}Findings:{Colors.RESET} {paths['findings']}")
            print()
        except Exception as e:
            print(f"  {Colors.RED}✗ Pipeline failed: {e}{Colors.RESET}")
            return 1

        return 0

    elif action == "status":
        workspace = args.workspace
        if not workspace:
            print(
                f"  {Colors.RED}✗ --workspace required{Colors.RESET}", file=sys.stderr
            )
            return 1

        output_dir = Path(args.output or "./audit-logs") / workspace
        if not output_dir.exists():
            print(f"  {Colors.RED}✗ Workspace '{workspace}' not found{Colors.RESET}")
            return 1

        metrics_file = output_dir / "metrics.json"
        if metrics_file.exists():
            metrics = json.loads(metrics_file.read_text(encoding="utf-8"))
            if args.json_output:
                print(json.dumps(metrics, indent=2))
            else:
                print_section(f"PENTEST STATUS — {workspace}")
                print(
                    f"  {Colors.CYAN}Target:{Colors.RESET}    {metrics.get('target', 'unknown')}"
                )
                print(
                    f"  {Colors.CYAN}Findings:{Colors.RESET}  {metrics.get('findings_count', 0)}"
                )
                dist = metrics.get("severity_distribution", {})
                for sev, count in dist.items():
                    print(f"    {sev.upper()}: {count}")
        else:
            print(
                f"  {Colors.YELLOW}⚠ Pipeline in progress or incomplete{Colors.RESET}"
            )
            deliverables_dir = output_dir / "deliverables"
            if deliverables_dir.exists():
                count = len(list(deliverables_dir.glob("*.md")))
                print(f"  {Colors.CYAN}Deliverables found:{Colors.RESET} {count}")
        return 0

    elif action == "agents":
        from .shannon.agents import AGENTS

        if args.json_output:
            agents_data = []
            for a in AGENTS.values():
                agents_data.append(
                    {
                        "name": a.name,
                        "phase": a.phase,
                        "display_name": a.display_name,
                        "model_tier": a.model_tier,
                        "leviathan_domains": list(a.leviathan_domains),
                    }
                )
            print(json.dumps(agents_data, indent=2))
        else:
            print_section("SIREN AUTONOMOUS AGENTS")
            current_phase = ""
            for agent in AGENTS.values():
                if agent.phase != current_phase:
                    current_phase = agent.phase
                    print(
                        f"\n  {Colors.CRIMSON}━━━ {current_phase.upper()} ━━━{Colors.RESET}"
                    )
                print(f"    {Colors.CYAN}{agent.display_name}{Colors.RESET}")
                print(
                    f"      Model: {agent.model_tier} | Domains: {', '.join(list(agent.leviathan_domains)[:3])}"
                )
        return 0

    elif action == "preflight":
        if not args.target or not args.repo:
            print(
                f"  {Colors.RED}✗ --target and --repo are required{Colors.RESET}",
                file=sys.stderr,
            )
            return 1
        from .shannon.engine import AbyssalEngine, EngineConfig

        config = EngineConfig(target_url=args.target, repo_path=args.repo)
        engine = AbyssalEngine(config)
        report = asyncio.run(engine.preflight())
        if args.json_output:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print_section("PREFLIGHT CHECK")
            for check in report["checks"]:
                icon = (
                    Colors.GREEN + "✓"
                    if check["status"] == "ok"
                    else (
                        Colors.YELLOW + "⚠"
                        if check["status"] == "warn"
                        else Colors.RED + "✗"
                    )
                )
                print(f"  {icon} {check['name']}{Colors.RESET}")
            print(f"\n  {'PASS' if report['valid'] else 'FAIL'}")
        return 0 if report["valid"] else 1

    elif action == "workspaces":
        output_dir = Path(args.output or "./audit-logs")
        if not output_dir.exists():
            print(f"  {Colors.DIM}No workspaces found{Colors.RESET}")
            return 0
        print_section("AUDIT WORKSPACES")
        for d in sorted(output_dir.iterdir()):
            if d.is_dir():
                metrics_file = d / "metrics.json"
                if metrics_file.exists():
                    try:
                        m = json.loads(metrics_file.read_text(encoding="utf-8"))
                        print(
                            f"  {Colors.GREEN}✓{Colors.RESET} {d.name} — {m.get('target', '?')} ({m.get('findings_count', 0)} findings)"
                        )
                    except Exception:
                        print(f"  {Colors.YELLOW}?{Colors.RESET} {d.name} — corrupted")
                else:
                    print(f"  {Colors.CYAN}…{Colors.RESET} {d.name} — in progress")
        return 0

    else:
        print(f"  {Colors.RED}✗ Unknown action: {action}{Colors.RESET}")
        return 1


def cmd_auth(args):
    """SIREN AUTH — Authentication attack engine."""
    import asyncio

    action = args.action
    target = args.target

    # Load wordlists if provided
    usernames = None
    passwords = None
    if getattr(args, "userlist", None):
        try:
            usernames = (
                Path(args.userlist).read_text(encoding="utf-8").strip().splitlines()
            )
        except Exception:
            pass
    if getattr(args, "passlist", None):
        try:
            passwords = (
                Path(args.passlist).read_text(encoding="utf-8").strip().splitlines()
            )
        except Exception:
            pass

    from .shannon.auth_engine import (
        AccountEnumerator,
        AuthFingerprint,
        AuthFingerprinter,
        BruteForceEngine,
        DefaultCredentialScanner,
        MFABypassEngine,
        PasswordSprayer,
        SessionAnalyzer,
        SirenAuthEngine,
    )

    if action == "audit":
        print_section("SIREN AUTH — Full Authentication Audit")
        print(f"  {Colors.BLOOD}⚡ Target: {target}{Colors.RESET}")
        print()

        engine = SirenAuthEngine()
        result = asyncio.run(
            engine.full_auth_audit(
                target=target,
                login_url=getattr(args, "login_url", None),
                usernames=usernames,
                passwords=passwords,
            )
        )

        if getattr(args, "json_output", False):
            print(json.dumps(result, indent=2, default=str))
        else:
            report = engine.generate_report()
            print(report)

        return 0

    elif action == "brute":
        print_section("SIREN AUTH — Brute Force Attack")
        fp = AuthFingerprint()
        fp.login_url = getattr(args, "login_url", None) or target

        engine = BruteForceEngine(fp)
        result = asyncio.run(
            engine.brute_force(
                usernames=usernames or [],
                passwords=passwords or [],
            )
        )
        print(f"  {Colors.CYAN}{result.details}{Colors.RESET}")
        for c in result.credentials:
            if c.valid:
                print(
                    f"  {Colors.GREEN}✓ {c.username}:{c.password[:3]}***{Colors.RESET}"
                )
        return 0

    elif action == "spray":
        print_section("SIREN AUTH — Password Spray")
        fp = AuthFingerprint()
        fp.login_url = getattr(args, "login_url", None) or target

        sprayer = PasswordSprayer(fp)
        result = asyncio.run(
            sprayer.spray(
                usernames=usernames or [],
                passwords=passwords or [],
            )
        )
        print(f"  {Colors.CYAN}{result.details}{Colors.RESET}")
        return 0

    elif action == "session":
        print_section("SIREN AUTH — Session Analysis")
        analyzer = SessionAnalyzer()
        result = asyncio.run(analyzer.analyze_session(target))
        print(f"  {Colors.CYAN}{result.details}{Colors.RESET}")
        for s in result.sessions:
            print(f"    {s.name}: type={s.token_type.value} entropy={s.entropy:.1f}")
        return 0

    elif action == "enum":
        print_section("SIREN AUTH — Account Enumeration")
        fp = AuthFingerprint()
        fp.login_url = target
        enumerator = AccountEnumerator(fp)
        result = asyncio.run(enumerator.enumerate(usernames or []))
        print(f"  {Colors.CYAN}{result.details}{Colors.RESET}")
        for c in result.credentials:
            if c.valid:
                print(f"  {Colors.GREEN}✓ {c.username}{Colors.RESET}")
        return 0

    elif action == "defaults":
        print_section("SIREN AUTH — Default Credentials Scan")
        scanner = DefaultCredentialScanner()
        result = asyncio.run(scanner.scan_defaults(target))
        print(f"  {Colors.CYAN}{result.details}{Colors.RESET}")
        for c in result.credentials:
            if c.valid:
                print(
                    f"  {Colors.GREEN}✓ {c.username}:{c.password[:3]}*** ({c.source}){Colors.RESET}"
                )
        return 0

    elif action == "mfa":
        print_section("SIREN AUTH — MFA Bypass Testing")
        engine = MFABypassEngine()
        result = asyncio.run(engine.test_mfa_bypass(target, {}))
        print(f"  {Colors.CYAN}{result.details}{Colors.RESET}")
        return 0

    else:
        print(f"  {Colors.RED}✗ Unknown auth action: {action}{Colors.RESET}")
        return 1


def cmd_crypto(args):
    """SIREN CRYPTO — Cryptographic attack engine."""
    import asyncio

    action = args.action
    target = getattr(args, "target", "") or ""

    from .shannon.crypto import (
        CipherAnalyzer,
        HashEngine,
        JWTAttackEngine,
        PaddingOracleEngine,
        SirenCryptoEngine,
        TLSScanner,
    )

    if action == "audit":
        print_section("SIREN CRYPTO — Full Cryptographic Audit")
        print(f"  {Colors.BLOOD}⚡ Target: {target}{Colors.RESET}")
        print()

        engine = SirenCryptoEngine()
        result = asyncio.run(engine.full_crypto_audit(target=target))

        if getattr(args, "json_output", False):
            print(json.dumps(result, indent=2, default=str))
        else:
            report = engine.generate_report()
            print(report)
        return 0

    elif action == "jwt":
        print_section("SIREN CRYPTO — JWT Attack")
        token = getattr(args, "token", None) or target
        if not token:
            print(f"  {Colors.RED}✗ --token required{Colors.RESET}")
            return 1

        engine = JWTAttackEngine()
        result = asyncio.run(engine.full_jwt_audit(token))
        print(f"  {Colors.CYAN}{result.details}{Colors.RESET}")
        if result.evidence:
            for key, val in result.evidence.items():
                print(f"    {key}: {val}")
        return 0

    elif action == "hash":
        print_section("SIREN CRYPTO — Hash Cracker")
        hash_val = getattr(args, "hash_value", None) or target
        if not hash_val:
            print(f"  {Colors.RED}✗ --hash required{Colors.RESET}")
            return 1

        wordlist = []
        if getattr(args, "wordlist", None):
            try:
                wordlist = (
                    Path(args.wordlist).read_text(encoding="utf-8").strip().splitlines()
                )
            except Exception:
                pass

        cracker = HashEngine()
        result = asyncio.run(cracker.crack(hash_val, wordlist=wordlist or None))
        print(f"  {Colors.CYAN}{result.details}{Colors.RESET}")
        if result.success and result.evidence.get("cracked_value"):
            print(
                f"  {Colors.GREEN}✓ CRACKED: {result.evidence['cracked_value']}{Colors.RESET}"
            )
        return 0

    elif action == "tls":
        print_section("SIREN CRYPTO — TLS/SSL Scanner")
        if not target:
            print(f"  {Colors.RED}✗ --target required{Colors.RESET}")
            return 1

        scanner = TLSScanner()
        result = asyncio.run(scanner.scan(target))
        print(f"  {Colors.CYAN}{result.details}{Colors.RESET}")
        return 0

    elif action == "cipher":
        print_section("SIREN CRYPTO — Cipher Analysis")
        data = getattr(args, "token", None) or target
        if not data:
            print(f"  {Colors.RED}✗ --target or --token required{Colors.RESET}")
            return 1

        analyzer = CipherAnalyzer()
        result = asyncio.run(analyzer.analyze(data))
        print(f"  {Colors.CYAN}{result.details}{Colors.RESET}")
        return 0

    elif action == "padding":
        print_section("SIREN CRYPTO — Padding Oracle Attack")
        if not target:
            print(f"  {Colors.RED}✗ --target required{Colors.RESET}")
            return 1

        oracle = PaddingOracleEngine()
        result = asyncio.run(oracle.attack(target, b""))
        print(f"  {Colors.CYAN}{result.details}{Colors.RESET}")
        return 0

    else:
        print(f"  {Colors.RED}✗ Unknown crypto action: {action}{Colors.RESET}")
        return 1


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
# API SECURITY AUDIT COMMAND — OWASP API Security Testing
# ════════════════════════════════════════════════════════════════════════════


def cmd_api_audit(args):
    """SIREN API AUDIT — API Security Testing Engine (OWASP Top 10)."""
    import asyncio

    action = args.action
    target = args.target

    from .shannon.api_security import SirenAPISecurityEngine

    if action == "full":
        if not target:
            print(f"  {Colors.RED}✗ --target required{Colors.RESET}", file=sys.stderr)
            return 1

        print_section("SIREN API SECURITY — Full OWASP Audit")
        print(f"  {Colors.BLOOD}⚡ Target: {target}{Colors.RESET}")
        print()
        print(f"  {Colors.CYAN}▸ Phase 1: Unauthenticated Access Control{Colors.RESET}")
        print(
            f"  {Colors.CYAN}▸ Phase 2: Security Headers & Data Exposure{Colors.RESET}"
        )
        print(f"  {Colors.CYAN}▸ Phase 3: CORS Policy Testing{Colors.RESET}")
        print(f"  {Colors.CYAN}▸ Phase 4: JWT Security{Colors.RESET}")
        print(f"  {Colors.CYAN}▸ Phase 5: IDOR & Privilege Escalation{Colors.RESET}")
        print(f"  {Colors.CYAN}▸ Phase 6: HTTP Method Tampering{Colors.RESET}")
        print(f"  {Colors.CYAN}▸ Phase 7: Rate Limiting{Colors.RESET}")
        print(f"  {Colors.CYAN}▸ Phase 8: User Enumeration{Colors.RESET}")
        print()

        engine = SirenAPISecurityEngine()
        result = asyncio.run(
            engine.full_api_audit(
                target=target,
                jwt_token=getattr(args, "token", None),
                login_url=getattr(args, "login_url", None),
                endpoints=getattr(args, "endpoints", None),
            )
        )

        if getattr(args, "json_output", False):
            print(engine.generate_json_report())
        else:
            report = engine.generate_report()
            print(report)

        # Save report
        output_dir = Path(getattr(args, "output", None) or "./audit-logs")
        output_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = output_dir / f"api_security_{ts}.md"
        report_path.write_text(engine.generate_report(), encoding="utf-8")
        json_path = output_dir / f"api_security_{ts}.json"
        json_path.write_text(engine.generate_json_report(), encoding="utf-8")

        print()
        print_section("AUDIT COMPLETE")
        print(f"  {Colors.GREEN}✓ Findings:{Colors.RESET}    {len(result.findings)}")
        print(f"  {Colors.RED}✗ Critical:{Colors.RESET}    {result.critical_count}")
        print(f"  {Colors.YELLOW}⚠ High:{Colors.RESET}       {result.high_count}")
        print(f"  {Colors.CYAN}◉ Requests:{Colors.RESET}   {result.total_requests}")
        print(
            f"  {Colors.CYAN}◉ Duration:{Colors.RESET}   {result.duration_seconds:.1f}s"
        )
        print(f"  {Colors.CYAN}Report:{Colors.RESET}       {report_path}")
        print(f"  {Colors.CYAN}JSON:{Colors.RESET}         {json_path}")
        return 0

    elif action == "access":
        if not target:
            print(f"  {Colors.RED}✗ --target required{Colors.RESET}", file=sys.stderr)
            return 1

        print_section("SIREN API — Broken Access Control Test (A01:2021)")
        from .shannon.api_security import APISecurityHTTP, BrokenAccessControlScanner

        http = APISecurityHTTP()
        scanner = BrokenAccessControlScanner(http)
        try:
            findings = asyncio.run(
                scanner.scan_unauthenticated_access(
                    target, getattr(args, "endpoints", None)
                )
            )
        finally:
            asyncio.run(http.close())

        for f in findings:
            icon = f.severity.icon
            print(f"  {icon} {f.title}")
            print(f"    CVSS: {f.cvss_score} | CWE-{f.cwe_id} | {f.owasp_ref}")
        if not findings:
            print(f"  {Colors.GREEN}✓ No broken access control found{Colors.RESET}")
        return 0

    elif action == "jwt":
        token = getattr(args, "token", None)
        if not target or not token:
            print(
                f"  {Colors.RED}✗ --target and --token required{Colors.RESET}",
                file=sys.stderr,
            )
            return 1

        print_section("SIREN API — JWT Security Test")
        from .shannon.api_security import APISecurityHTTP, JWTSecurityScanner

        http = APISecurityHTTP()
        scanner = JWTSecurityScanner(http)
        try:
            findings = asyncio.run(scanner.scan_jwt_security(target, token))
        finally:
            asyncio.run(http.close())

        for f in findings:
            icon = f.severity.icon
            print(f"  {icon} {f.title}")
        if not findings:
            print(f"  {Colors.GREEN}✓ No JWT vulnerabilities found{Colors.RESET}")
        return 0

    elif action == "idor":
        if not target:
            print(f"  {Colors.RED}✗ --target required{Colors.RESET}", file=sys.stderr)
            return 1

        print_section("SIREN API — IDOR Test")
        from .shannon.api_security import APISecurityHTTP, BrokenAccessControlScanner

        http = APISecurityHTTP()
        scanner = BrokenAccessControlScanner(http)
        try:
            findings = asyncio.run(
                scanner.scan_idor(target, getattr(args, "token", None))
            )
        finally:
            asyncio.run(http.close())

        for f in findings:
            print(f"  {f.severity.icon} {f.title}")
        if not findings:
            print(f"  {Colors.GREEN}✓ No IDOR vulnerabilities found{Colors.RESET}")
        return 0

    elif action == "ratelimit":
        if not target:
            print(f"  {Colors.RED}✗ --target required{Colors.RESET}", file=sys.stderr)
            return 1

        print_section("SIREN API — Rate Limit Test")
        from .shannon.api_security import APISecurityHTTP, RateLimitScanner

        http = APISecurityHTTP()
        scanner = RateLimitScanner(http)
        try:
            findings = asyncio.run(
                scanner.scan_rate_limit(target, getattr(args, "endpoints", None))
            )
        finally:
            asyncio.run(http.close())

        for f in findings:
            print(f"  {f.severity.icon} {f.title}")
        if not findings:
            print(f"  {Colors.GREEN}✓ Rate limiting detected{Colors.RESET}")
        return 0

    elif action == "cors":
        if not target:
            print(f"  {Colors.RED}✗ --target required{Colors.RESET}", file=sys.stderr)
            return 1

        print_section("SIREN API — CORS Policy Test")
        from .shannon.api_security import APISecurityHTTP, DataExposureScanner

        http = APISecurityHTTP()
        scanner = DataExposureScanner(http)
        try:
            findings = asyncio.run(
                scanner.scan_cors_policy(target, getattr(args, "endpoints", None))
            )
        finally:
            asyncio.run(http.close())

        for f in findings:
            print(f"  {f.severity.icon} {f.title}")
        if not findings:
            print(f"  {Colors.GREEN}✓ CORS policy appears secure{Colors.RESET}")
        return 0

    elif action == "headers":
        if not target:
            print(f"  {Colors.RED}✗ --target required{Colors.RESET}", file=sys.stderr)
            return 1

        print_section("SIREN API — Security Headers Test")
        from .shannon.api_security import APISecurityHTTP, DataExposureScanner

        http = APISecurityHTTP()
        scanner = DataExposureScanner(http)
        try:
            findings = asyncio.run(scanner.scan_response_headers(target))
        finally:
            asyncio.run(http.close())

        for f in findings:
            print(f"  {f.severity.icon} {f.title}")
        if not findings:
            print(f"  {Colors.GREEN}✓ Security headers look good{Colors.RESET}")
        return 0

    elif action == "enum":
        if not target:
            print(f"  {Colors.RED}✗ --target required{Colors.RESET}", file=sys.stderr)
            return 1

        print_section("SIREN API — User Enumeration Test")
        from .shannon.api_security import APISecurityHTTP, UserEnumerationScanner

        http = APISecurityHTTP()
        scanner = UserEnumerationScanner(http)
        try:
            findings = asyncio.run(
                scanner.scan_response_enumeration(
                    target, getattr(args, "login_url", None)
                )
            )
        finally:
            asyncio.run(http.close())

        for f in findings:
            print(f"  {f.severity.icon} {f.title}")
        if not findings:
            print(f"  {Colors.GREEN}✓ No enumeration vectors found{Colors.RESET}")
        return 0

    else:
        print(f"  {Colors.RED}✗ Unknown api-audit action: {action}{Colors.RESET}")
        return 1


# WORKSPACE COMMAND — Manage SIREN workspaces
# ════════════════════════════════════════════════════════════════════════════


def cmd_workspace(args):
    """SIREN WORKSPACE — Manage audit workspaces, checkpoints & sessions."""
    action = args.action
    output_dir = args.output or "./audit-logs"

    from .shannon.workspace import (
        ConfigFileLoader,
        WorkspaceManager,
    )

    mgr = WorkspaceManager(output_dir)

    if action == "list":
        workspaces = mgr.list_all()
        if not workspaces:
            print(f"  {Colors.DIM}No workspaces found in {output_dir}{Colors.RESET}")
            return 0
        print_section("SIREN AUDIT WORKSPACES")
        for ws in workspaces:
            icon = (
                Colors.GREEN + "✓"
                if ws.status.value in ("completed",)
                else (
                    Colors.CYAN + "▸"
                    if ws.status.value in ("running",)
                    else Colors.YELLOW + "⏸"
                )
            )
            deliv_count = len(ws.deliverables) if ws.deliverables else 0
            print(
                f"  {icon}{Colors.RESET} {ws.name}"
                f"  {Colors.DIM}({ws.status.value}, {deliv_count} deliverables){Colors.RESET}"
            )
            if ws.target_url:
                print(f"    {Colors.DIM}Target: {ws.target_url}{Colors.RESET}")
        return 0

    elif action == "status":
        name = args.workspace
        if not name:
            print(
                f"  {Colors.RED}✗ --workspace required{Colors.RESET}", file=sys.stderr
            )
            return 1
        status = mgr.get_status(name)
        if "error" in status:
            print(f"  {Colors.RED}✗ {status['error']}{Colors.RESET}")
            return 1
        if getattr(args, "json_output", False):
            print(json.dumps(status, indent=2, ensure_ascii=False, default=str))
        else:
            print_section(f"WORKSPACE STATUS — {name}")
            for key, val in status.items():
                if key == "deliverables":
                    print(f"  {Colors.CYAN}Deliverables:{Colors.RESET}")
                    for d in val:
                        print(f"    - {d}")
                elif key == "checkpoints":
                    print(f"  {Colors.CYAN}Checkpoints:{Colors.RESET} {len(val)}")
                else:
                    print(f"  {Colors.CYAN}{key}:{Colors.RESET} {val}")
        return 0

    elif action == "resume":
        name = args.workspace
        target = getattr(args, "target", None)
        if not name:
            print(
                f"  {Colors.RED}✗ --workspace required{Colors.RESET}", file=sys.stderr
            )
            return 1
        path, session, info = mgr.resume(name, target)
        if not path:
            print(f"  {Colors.RED}✗ {info.get('error', 'Resume failed')}{Colors.RESET}")
            return 1
        print(f"  {Colors.GREEN}✓ Resumed workspace: {name}{Colors.RESET}")
        agents_skip = info.get("agents_to_skip", [])
        agents_remain = info.get("agents_remaining", [])
        if agents_skip:
            print(
                f"  {Colors.DIM}Skipping completed agents: {', '.join(agents_skip)}{Colors.RESET}"
            )
        if agents_remain:
            print(
                f"  {Colors.CYAN}Remaining agents: {', '.join(agents_remain)}{Colors.RESET}"
            )
        return 0

    elif action == "cleanup":
        name = args.workspace
        if not name:
            print(
                f"  {Colors.RED}✗ --workspace required{Colors.RESET}", file=sys.stderr
            )
            return 1
        result = mgr.cleanup(name)
        if result.get("success"):
            print(f"  {Colors.GREEN}✓ Workspace '{name}' cleaned up{Colors.RESET}")
        else:
            print(
                f"  {Colors.RED}✗ {result.get('error', 'Cleanup failed')}{Colors.RESET}"
            )
        return 0

    elif action == "config-gen":
        path = ConfigFileLoader.generate_example()
        print(f"  {Colors.GREEN}✓ Example config generated: {path}{Colors.RESET}")
        return 0

    elif action == "config-check":
        config, errors = ConfigFileLoader.load(getattr(args, "config_path", None))
        if config:
            print(f"  {Colors.GREEN}✓ Config loaded successfully{Colors.RESET}")
            print(f"    Target: {config.target_url or '(not set)'}")
            print(f"    Repo: {config.repo_path or '(not set)'}")
            print(f"    Login: {config.login_type}")
            if config.totp_secret:
                from .shannon.orchestrator import TOTPGenerator

                valid, msg = TOTPGenerator.validate_secret(config.totp_secret)
                icon = Colors.GREEN + "✓" if valid else Colors.RED + "✗"
                print(f"    TOTP: {icon} {msg}{Colors.RESET}")
        if errors:
            for e in errors:
                print(f"  {Colors.YELLOW}⚠ {e}{Colors.RESET}")
        return 0 if config else 1

    else:
        print(f"  {Colors.RED}✗ Unknown action: {action}{Colors.RESET}")
        return 1


# ════════════════════════════════════════════════════════════════════════════
# BOOT SEQUENCE — NUCLEAR INITIALIZATION
# ════════════════════════════════════════════════════════════════════════════


def _boot_sequence():
    """Nuclear boot sequence — 12 stages of awakening."""
    stages = [
        ("Awakening ABYSSAL CORE", Colors.DARK_RED, "blood"),
        ("Loading 640+ evasion rules (KRAKEN ENGINE)", Colors.CRIMSON, "fire"),
        ("Establishing TENTACLE PROTOCOL (50 MCPs)", Colors.CYAN, "cyber"),
        ("Calibrating 711+ attack tools", Colors.NEON_GREEN, "matrix"),
        ("Mapping 16 attack domains", Colors.ORANGE, "inferno"),
        ("Initializing MITRE ATT&CK coverage (14 tactics)", Colors.PHANTOM, "phantom"),
        ("Activating Shannon Engine (13 AI agents)", Colors.YELLOW, "nuclear"),
        ("Loading 5-phase autonomous pipeline", Colors.SKY, "ice"),
        ("Connecting multi-tier AI models (haiku/sonnet/opus)", Colors.GREEN, "toxic"),
        ("Calibrating zero-hallucination reporter", Colors.GOLD, "fire"),
        ("Encrypting comms (AES-256-GCM)", Colors.ICE, "cyber"),
        ("DEPTH OMEGA² reached — ABYSSAL CONVERGENCE online", Colors.BLOOD, "hellfire"),
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
            f"50 MCPs | 711+ Tools | DEPTH: {__depth__} | "
            f"SID:{hex_id} | {ts}{Colors.RESET}\n"
        )

    parser = argparse.ArgumentParser(
        prog="leviathan",
        description=(
            "☠️ LEVIATHAN VS v69.0.0 ABYSSAL CONVERGENCE\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Arsenal Ofensivo Nivel Militar + Shannon AI Pipeline\n"
            "50 MCP Servers | 711+ Tools | 640+ Evasion Rules\n"
            "16 Attack Domains | 13 AI Agents | 5 Pipeline Phases\n"
            "Classification: OMEGA-ULTRABLACK | Depth: ∞²"
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

    # pentest (SIREN Engine)
    p_pt = sub.add_parser(
        "pentest",
        aliases=["pt", "siren", "shannon"],
        help="SIREN ENGINE — Autonomous AI pentest pipeline",
    )
    p_pt.add_argument(
        "action",
        choices=["start", "status", "agents", "preflight", "workspaces"],
        help="Pipeline action",
    )
    p_pt.add_argument("--target", "-t", help="Target URL")
    p_pt.add_argument(
        "--repo", "-r", help="Local repository path for white-box analysis"
    )
    p_pt.add_argument(
        "--workspace", "-w", help="Workspace name (default: auto-generated)"
    )
    p_pt.add_argument("--output", "-o", default="./audit-logs", help="Output directory")
    p_pt.add_argument("--auth-url", help="Login URL for authenticated testing")
    p_pt.add_argument("--auth-user", help="Username for authentication")
    p_pt.add_argument("--no-kraken", action="store_true", help="Disable Kraken evasion")
    p_pt.add_argument("--unsafe", action="store_true", help="Disable safe mode")
    p_pt.add_argument(
        "--testing", action="store_true", help="Testing mode (reduced retries)"
    )
    p_pt.set_defaults(func=cmd_pentest)

    # auth (SIREN Auth Engine)
    p_auth = sub.add_parser(
        "auth",
        aliases=["authattack"],
        help="SIREN AUTH — Authentication attack engine (brute, spray, session, MFA, OAuth)",
    )
    p_auth.add_argument(
        "action",
        choices=["audit", "brute", "spray", "session", "enum", "defaults", "mfa"],
        help="Auth attack action",
    )
    p_auth.add_argument("--target", "-t", help="Target URL", required=True)
    p_auth.add_argument("--login-url", help="Login endpoint URL")
    p_auth.add_argument("--userlist", help="File with usernames (one per line)")
    p_auth.add_argument("--passlist", help="File with passwords (one per line)")
    p_auth.add_argument("--token", help="Token for replay/analysis")
    p_auth.add_argument(
        "--output", "-o", default="./audit-logs", help="Output directory"
    )
    p_auth.add_argument(
        "--json", dest="json_output", action="store_true", help="JSON output"
    )
    p_auth.set_defaults(func=cmd_auth)

    # crypto (SIREN Crypto Engine)
    p_crypto = sub.add_parser(
        "crypto",
        aliases=["cryptoattack"],
        help="SIREN CRYPTO — Cryptographic attack engine (JWT, hash, TLS, cipher)",
    )
    p_crypto.add_argument(
        "action",
        choices=["audit", "jwt", "hash", "tls", "cipher", "padding"],
        help="Crypto attack action",
    )
    p_crypto.add_argument("--target", "-t", help="Target URL or token")
    p_crypto.add_argument("--token", help="JWT or other token to attack")
    p_crypto.add_argument("--hash", dest="hash_value", help="Hash value to crack")
    p_crypto.add_argument("--wordlist", help="Wordlist for hash cracking")
    p_crypto.add_argument(
        "--output", "-o", default="./audit-logs", help="Output directory"
    )
    p_crypto.add_argument(
        "--json", dest="json_output", action="store_true", help="JSON output"
    )
    p_crypto.set_defaults(func=cmd_crypto)

    # api-audit (SIREN API Security Audit)
    p_api = sub.add_parser(
        "api-audit",
        aliases=["api", "apisec"],
        help="SIREN API AUDIT — OWASP API Security Testing (access control, data exposure, JWT, IDOR, rate limit)",
    )
    p_api.add_argument(
        "action",
        choices=[
            "full",
            "access",
            "jwt",
            "idor",
            "ratelimit",
            "cors",
            "headers",
            "enum",
        ],
        help="API security test action",
    )
    p_api.add_argument("--target", "-t", help="Target API base URL", required=True)
    p_api.add_argument("--token", help="JWT token for authenticated tests")
    p_api.add_argument("--login-url", help="Login endpoint URL")
    p_api.add_argument("--endpoints", nargs="+", help="Specific API endpoints to test")
    p_api.add_argument(
        "--output", "-o", default="./audit-logs", help="Output directory"
    )
    p_api.add_argument(
        "--json", dest="json_output", action="store_true", help="JSON output"
    )
    p_api.set_defaults(func=cmd_api_audit)

    # workspace (SIREN Workspace Management)
    p_ws = sub.add_parser(
        "workspace",
        aliases=["ws"],
        help="SIREN WORKSPACE — Manage workspaces, checkpoints, config",
    )
    p_ws.add_argument(
        "action",
        choices=["list", "status", "resume", "cleanup", "config-gen", "config-check"],
        help="Workspace action",
    )
    p_ws.add_argument("--workspace", "-w", help="Workspace name")
    p_ws.add_argument("--target", "-t", help="Target URL (for resume verification)")
    p_ws.add_argument("--output", "-o", default="./audit-logs", help="Output directory")
    p_ws.add_argument("--config-path", help="Path to config file (for config-check)")
    p_ws.add_argument(
        "--json", dest="json_output", action="store_true", help="JSON output"
    )
    p_ws.set_defaults(func=cmd_workspace)

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
