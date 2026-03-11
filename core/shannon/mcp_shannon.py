#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
████████████████████████████████████████████████████████████████████████████████████
██                                                                                ██
██  🌊  MCP ABYSSAL PENTEST SERVER — Shannon Pipeline como MCP Plugin  🌊       ██
██                                                                                ██
██  Expoe o pipeline autonomo de pentesting como ferramentas MCP,                 ██
██  permitindo que VS Code e qualquer client MCP iniciem, monitorem,              ██
██  e consumam resultados de auditorias de seguranca autonomas.                   ██
██                                                                                ██
██  TOOLS:                                                                        ██
██    start_pentest     — Inicia pipeline autonomo contra um target              ██
██    pentest_status    — Status em tempo real do pipeline                        ██
██    resume_pentest    — Retoma pipeline interrompido                            ██
██    get_report        — Recupera report final                                   ██
██    list_workspaces   — Lista workspaces de auditoria                           ██
██    list_agents       — Lista agentes disponiveis                               ██
██    preflight_check   — Verifica config antes de executar                       ██
██                                                                                ██
██  Server #50: O MCP definitivo. Shannon + Leviathan = Abyssal Pentest.         ██
██                                                                                ██
████████████████████████████████████████████████████████████████████████████████████
"""

from __future__ import annotations

import asyncio
import json
import logging
import os

# Import base class
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.mcp_plugin_base import MCPPluginBase

from .agents import AGENTS, get_agents_for_phase
from .engine import AbyssalEngine, EngineConfig
from .models import get_all_models, validate_credentials
from .reporter import AbyssalReporter

logger = logging.getLogger("leviathan.mcp.shannon")


class MCPAbyssalPentest(MCPPluginBase):
    """MCP Plugin Server #50 — Abyssal Autonomous Pentest.

    Transforms Shannon's AI pentesting pipeline into MCP tools,
    making autonomous security audits available to any MCP client
    (VS Code, Claude Desktop, etc).

    Combines:
    - Shannon's 13-agent autonomous pipeline
    - Leviathan's 704+ security tools
    - Multi-tier AI model system
    - Zero-hallucination reporting
    """

    server_name = "leviathan-abyssal-pentest"
    version = "1.0.0"

    tools = [
        {
            "name": "start_pentest",
            "description": (
                "⚡ Inicia pipeline autonomo de pentesting contra um target.\n"
                "Executa 5 fases: Pre-Recon → Recon → Vuln Analysis → Exploitation → Reporting.\n"
                "Usa 13 agentes AI especializados + 704 ferramentas Leviathan.\n"
                "Resultados salvos em audit-logs/{workspace}/"
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target_url": {
                        "type": "string",
                        "description": "URL do target (ex: https://app.example.com)",
                    },
                    "repo_path": {
                        "type": "string",
                        "description": "Caminho local do repositorio do target para analise white-box",
                    },
                    "workspace": {
                        "type": "string",
                        "description": "Nome do workspace (default: timestamp-based)",
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Diretorio de saida (default: ./audit-logs)",
                    },
                    "auth_login_url": {
                        "type": "string",
                        "description": "URL de login para testes autenticados",
                    },
                    "auth_username": {
                        "type": "string",
                        "description": "Username para autenticacao",
                    },
                    "auth_password": {
                        "type": "string",
                        "description": "Password para autenticacao",
                    },
                    "avoid_paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Paths a evitar durante testes",
                    },
                    "focus_paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Paths a priorizar",
                    },
                    "enable_kraken": {
                        "type": "boolean",
                        "description": "Ativar Kraken Evasion Engine (default: true)",
                    },
                    "enable_safe_mode": {
                        "type": "boolean",
                        "description": "Modo seguro (default: true)",
                    },
                    "testing_mode": {
                        "type": "boolean",
                        "description": "Modo teste com retries reduzidos (default: false)",
                    },
                },
                "required": ["target_url", "repo_path"],
            },
        },
        {
            "name": "pentest_status",
            "description": (
                "📊 Retorna status em tempo real do pipeline de pentesting.\n"
                "Mostra: fase atual, agentes executados, metricas, duração."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "workspace": {
                        "type": "string",
                        "description": "Nome do workspace para verificar",
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Diretorio de audit-logs (default: ./audit-logs)",
                    },
                },
                "required": ["workspace"],
            },
        },
        {
            "name": "resume_pentest",
            "description": (
                "🔄 Retoma pipeline de pentesting interrompido.\n"
                "Detecta deliverables existentes e pula fases concluidas."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "workspace": {
                        "type": "string",
                        "description": "Nome do workspace para retomar",
                    },
                    "target_url": {
                        "type": "string",
                        "description": "URL do target",
                    },
                    "repo_path": {
                        "type": "string",
                        "description": "Caminho do repositorio",
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Diretorio de audit-logs",
                    },
                },
                "required": ["workspace", "target_url", "repo_path"],
            },
        },
        {
            "name": "get_report",
            "description": (
                "📜 Recupera o report final de seguranca gerado pelo pipeline.\n"
                "Disponivel apos a fase de reporting ser concluida."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "workspace": {
                        "type": "string",
                        "description": "Nome do workspace",
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Diretorio de audit-logs",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["markdown", "json", "summary"],
                        "description": "Formato do report (default: markdown)",
                    },
                },
                "required": ["workspace"],
            },
        },
        {
            "name": "list_workspaces",
            "description": (
                "📁 Lista todos os workspaces de auditoria disponiveis.\n"
                "Mostra: target, estado, data, número de findings."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "output_dir": {
                        "type": "string",
                        "description": "Diretorio de audit-logs (default: ./audit-logs)",
                    },
                },
            },
        },
        {
            "name": "list_agents",
            "description": (
                "🤖 Lista todos os 13 agentes AI do pipeline Shannon.\n"
                "Mostra: nome, fase, tipo, domains Leviathan associados."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "phase": {
                        "type": "string",
                        "enum": [
                            "pre-recon",
                            "recon",
                            "vulnerability-analysis",
                            "exploitation",
                            "reporting",
                        ],
                        "description": "Filtrar por fase (optional)",
                    },
                },
            },
        },
        {
            "name": "preflight_check",
            "description": (
                "✅ Executa validacao pre-voo antes do pentesting.\n"
                "Verifica: credenciais AI, repositorio, configuração."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target_url": {
                        "type": "string",
                        "description": "URL do target",
                    },
                    "repo_path": {
                        "type": "string",
                        "description": "Caminho do repositorio",
                    },
                },
                "required": ["target_url", "repo_path"],
            },
        },
    ]

    def __init__(self):
        super().__init__()
        self._engines: Dict[str, AbyssalEngine] = {}
        self._running_tasks: Dict[str, asyncio.Task] = {}

    # ────────────────────────────────────────────────────────────────────
    # DISPATCH
    # ────────────────────────────────────────────────────────────────────

    async def dispatch_tool(self, name: str, args: dict) -> str:
        """Route tool calls to their handlers."""
        handlers = {
            "start_pentest": self._handle_start_pentest,
            "pentest_status": self._handle_pentest_status,
            "resume_pentest": self._handle_resume_pentest,
            "get_report": self._handle_get_report,
            "list_workspaces": self._handle_list_workspaces,
            "list_agents": self._handle_list_agents,
            "preflight_check": self._handle_preflight_check,
        }

        handler = handlers.get(name)
        if not handler:
            return f"❌ Unknown tool: {name}"

        try:
            result = await handler(args)
            return (
                result
                if isinstance(result, str)
                else json.dumps(result, indent=2, ensure_ascii=False)
            )
        except Exception as e:
            logger.error(f"Error in {name}: {e}", exc_info=True)
            return f"❌ Error: {e}"

    # ────────────────────────────────────────────────────────────────────
    # TOOL HANDLERS
    # ────────────────────────────────────────────────────────────────────

    async def _handle_start_pentest(self, args: dict) -> str:
        """Inicia pipeline autonomo de pentesting."""
        workspace = args.get("workspace") or datetime.now().strftime(
            "audit_%Y%m%d_%H%M%S"
        )
        output_dir = args.get("output_dir", "./audit-logs")

        config = EngineConfig(
            target_url=args["target_url"],
            repo_path=args["repo_path"],
            output_dir=output_dir,
            workspace=workspace,
            auth_login_url=args.get("auth_login_url"),
            auth_username=args.get("auth_username"),
            auth_password=args.get("auth_password"),
            avoid_paths=args.get("avoid_paths", []),
            focus_paths=args.get("focus_paths", []),
            enable_kraken_evasion=args.get("enable_kraken", True),
            enable_safe_mode=args.get("enable_safe_mode", True),
            pipeline_testing=args.get("testing_mode", False),
        )

        engine = AbyssalEngine(config)
        self._engines[workspace] = engine

        # Run pipeline
        try:
            result = await engine.run()

            # Generate report
            reporter = AbyssalReporter(
                pipeline_result=result,
                output_dir=output_dir,
                target_url=args["target_url"],
                workspace=workspace,
            )
            report_paths = reporter.save_report()

            return json.dumps(
                {
                    "status": "completed",
                    "workspace": workspace,
                    "state": result.state.value,
                    "phases_completed": result.phases_completed,
                    "agents_succeeded": result.agents_succeeded,
                    "agents_failed": result.agents_failed,
                    "duration_seconds": round(result.total_duration_ms / 1000, 2),
                    "report": report_paths["report"],
                    "metrics": report_paths["metrics"],
                    "findings": report_paths["findings"],
                },
                indent=2,
            )

        except Exception as e:
            return json.dumps(
                {
                    "status": "failed",
                    "workspace": workspace,
                    "error": str(e),
                },
                indent=2,
            )

    async def _handle_pentest_status(self, args: dict) -> str:
        """Retorna status do pipeline."""
        workspace = args["workspace"]
        output_dir = Path(args.get("output_dir", "./audit-logs")) / workspace

        if not output_dir.exists():
            return json.dumps({"error": f"Workspace '{workspace}' not found"})

        # Check metrics file
        metrics_file = output_dir / "metrics.json"
        if metrics_file.exists():
            metrics = json.loads(metrics_file.read_text(encoding="utf-8"))
            return json.dumps({"status": "completed", "metrics": metrics}, indent=2)

        # Check deliverables
        deliverables_dir = output_dir / "deliverables"
        deliverables = []
        if deliverables_dir.exists():
            deliverables = [f.name for f in deliverables_dir.glob("*.md")]

        # Check running engine
        engine = self._engines.get(workspace)
        if engine and engine._pipeline:
            summary = engine._pipeline.get_status_summary()
            return json.dumps(summary, indent=2)

        return json.dumps(
            {
                "status": "unknown",
                "workspace": workspace,
                "deliverables_found": deliverables,
            },
            indent=2,
        )

    async def _handle_resume_pentest(self, args: dict) -> str:
        """Retoma pipeline interrompido."""
        workspace = args["workspace"]
        output_dir = args.get("output_dir", "./audit-logs")

        config = EngineConfig(
            target_url=args["target_url"],
            repo_path=args["repo_path"],
            output_dir=output_dir,
            workspace=workspace,
        )

        engine = AbyssalEngine(config)
        self._engines[workspace] = engine

        try:
            result = await engine.run()

            reporter = AbyssalReporter(
                pipeline_result=result,
                output_dir=output_dir,
                target_url=args["target_url"],
                workspace=workspace,
            )
            report_paths = reporter.save_report()

            return json.dumps(
                {
                    "status": "resumed_and_completed",
                    "workspace": workspace,
                    "phases_completed": result.phases_completed,
                    "report": report_paths["report"],
                },
                indent=2,
            )

        except Exception as e:
            return json.dumps({"status": "failed", "error": str(e)}, indent=2)

    async def _handle_get_report(self, args: dict) -> str:
        """Recupera report final."""
        workspace = args["workspace"]
        output_dir = Path(args.get("output_dir", "./audit-logs")) / workspace
        fmt = args.get("format", "markdown")

        if fmt == "json":
            findings_file = output_dir / "findings.json"
            if findings_file.exists():
                return findings_file.read_text(encoding="utf-8")
            return json.dumps({"error": "No findings file found"})

        elif fmt == "summary":
            metrics_file = output_dir / "metrics.json"
            if metrics_file.exists():
                metrics = json.loads(metrics_file.read_text(encoding="utf-8"))
                summary = {
                    "target": metrics.get("target", "unknown"),
                    "findings_count": metrics.get("findings_count", 0),
                    "severity_distribution": metrics.get("severity_distribution", {}),
                    "pipeline_state": metrics.get("pipeline", {}).get(
                        "state", "unknown"
                    ),
                }
                return json.dumps(summary, indent=2)
            return json.dumps({"error": "No metrics file found"})

        else:  # markdown
            report_file = output_dir / "ABYSSAL_REPORT.md"
            if report_file.exists():
                return report_file.read_text(encoding="utf-8")
            return "❌ No report found. Run `start_pentest` first."

    async def _handle_list_workspaces(self, args: dict) -> str:
        """Lista workspaces disponiveis."""
        output_dir = Path(args.get("output_dir", "./audit-logs"))
        workspaces = []

        if output_dir.exists():
            for d in output_dir.iterdir():
                if d.is_dir():
                    ws_info = {
                        "name": d.name,
                        "path": str(d),
                    }
                    # Check for metrics
                    metrics_file = d / "metrics.json"
                    if metrics_file.exists():
                        try:
                            metrics = json.loads(
                                metrics_file.read_text(encoding="utf-8")
                            )
                            ws_info["target"] = metrics.get("target", "unknown")
                            ws_info["findings_count"] = metrics.get("findings_count", 0)
                            ws_info["timestamp"] = metrics.get("timestamp", "unknown")
                            ws_info["status"] = "completed"
                        except Exception:
                            ws_info["status"] = "corrupted"
                    else:
                        # Check deliverables
                        deliverables_dir = d / "deliverables"
                        if deliverables_dir.exists():
                            count = len(list(deliverables_dir.glob("*.md")))
                            ws_info["deliverables_count"] = count
                            ws_info["status"] = "in_progress"
                        else:
                            ws_info["status"] = "empty"

                    workspaces.append(ws_info)

        return json.dumps(
            {
                "total": len(workspaces),
                "workspaces": workspaces,
            },
            indent=2,
        )

    async def _handle_list_agents(self, args: dict) -> str:
        """Lista agentes do pipeline."""
        phase_filter = args.get("phase")

        if phase_filter:
            agents = get_agents_for_phase(phase_filter)
        else:
            agents = list(AGENTS.values())

        agent_list = []
        for agent in agents:
            agent_list.append(
                {
                    "name": agent.name,
                    "display_name": agent.display_name,
                    "phase": agent.phase,
                    "model_tier": agent.model_tier,
                    "vuln_type": agent.vuln_type,
                    "leviathan_domains": list(agent.leviathan_domains),
                    "preferred_tools": list(agent.preferred_tools),
                    "prerequisites": list(agent.prerequisites),
                }
            )

        return json.dumps(
            {
                "total": len(agent_list),
                "agents": agent_list,
            },
            indent=2,
        )

    async def _handle_preflight_check(self, args: dict) -> str:
        """Executa preflight check."""
        config = EngineConfig(
            target_url=args["target_url"],
            repo_path=args["repo_path"],
        )
        engine = AbyssalEngine(config)
        report = await engine.preflight()
        return json.dumps(report, indent=2, ensure_ascii=False)


# ════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    MCPAbyssalPentest.main()
