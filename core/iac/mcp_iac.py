#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP Infrastructure as Code Scanner Server v1.0.0

    IaC security scanning MCP server.
    Integrates: tfsec, checkov, terrascan, semgrep.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (12):
        - tfsec_scan: Scan Terraform files for security issues
        - tfsec_custom: Run tfsec with custom rules
        - checkov_scan: Scan IaC files (Terraform, CloudFormation, K8s, Dockerfile)
        - checkov_framework: Scan specific framework only
        - checkov_check: Run specific check by ID
        - terrascan_scan: Scan IaC for policy violations
        - terrascan_list_policies: List available policies
        - semgrep_scan: Run Semgrep SAST rules on code
        - semgrep_ci: Run Semgrep in CI mode with SARIF output
        - kics_scan: Scan IaC with KICS (Checkmarx)
        - tflint_check: Lint Terraform files for errors and best practices
        - cfn_lint_check: Lint CloudFormation templates

    Author: ThiagoFrag / LEVIATHAN VS
    Version: 1.0.0
================================================================================
"""

import asyncio
import json
import logging
import os
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger("leviathan-iac-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-iac-server"


def _find_tool(name: str) -> str:
    p = shutil.which(name)
    return p if p else name


def _run_tool(cmd: List[str], timeout: int = 600) -> Dict:
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
        return {
            "success": proc.returncode == 0,
            "stdout": proc.stdout.strip()[:50000],
            "stderr": proc.stderr.strip()[:5000],
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"Timeout after {timeout}s"}
    except FileNotFoundError:
        return {
            "success": False,
            "error": f"Tool not found: {cmd[0]}. Install it first.",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


TOOLS = [
    {
        "name": "tfsec_scan",
        "description": "Scan Terraform files for security misconfigurations (Aqua tfsec)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to Terraform directory"},
                "format": {"type": "string", "description": "Output: default, json, sarif, csv, junit"},
                "severity": {"type": "string", "description": "Minimum severity: CRITICAL, HIGH, MEDIUM, LOW"},
                "exclude": {"type": "string", "description": "Comma-separated rule IDs to exclude"},
                "tfvars": {"type": "string", "description": "Path to .tfvars file"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "tfsec_custom",
        "description": "Run tfsec with custom rule definitions",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Terraform directory"},
                "config": {"type": "string", "description": "Path to custom tfsec config"},
                "custom_rules": {"type": "string", "description": "Path to custom rules directory"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "checkov_scan",
        "description": "Scan IaC files for misconfigurations (Terraform, CloudFormation, K8s, Docker, ARM)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Directory or file to scan"},
                "framework": {"type": "string", "description": "Framework: terraform, cloudformation, kubernetes, dockerfile, arm, helm"},
                "format": {"type": "string", "description": "Output: cli, json, sarif, junitxml"},
                "check": {"type": "string", "description": "Specific check IDs to run (comma-separated)"},
                "skip_check": {"type": "string", "description": "Check IDs to skip (comma-separated)"},
                "compact": {"type": "boolean", "description": "Compact output (failed checks only)"},
                "soft_fail": {"type": "boolean", "description": "Return exit code 0 even if checks fail"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "checkov_framework",
        "description": "Scan specific IaC framework only",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Directory to scan"},
                "framework": {"type": "string", "description": "Framework: terraform, cloudformation, kubernetes, dockerfile, arm, helm, bicep"},
                "format": {"type": "string", "description": "Output format"},
            },
            "required": ["path", "framework"],
        },
    },
    {
        "name": "checkov_check",
        "description": "Run a specific Checkov check by ID",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File or directory"},
                "check_id": {"type": "string", "description": "Check ID (e.g. CKV_AWS_1, CKV_DOCKER_1)"},
            },
            "required": ["path", "check_id"],
        },
    },
    {
        "name": "terrascan_scan",
        "description": "Scan IaC for policy violations using Terrascan",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "IaC directory or file"},
                "iac_type": {"type": "string", "description": "IaC type: terraform, k8s, helm, kustomize, docker, cloudformation"},
                "policy_type": {"type": "string", "description": "Policy: aws, azure, gcp, k8s, docker, github"},
                "format": {"type": "string", "description": "Output: human, json, sarif, yaml"},
                "severity": {"type": "string", "description": "Minimum severity: HIGH, MEDIUM, LOW"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "terrascan_list_policies",
        "description": "List all available Terrascan policies",
        "inputSchema": {
            "type": "object",
            "properties": {
                "policy_type": {"type": "string", "description": "Filter by type: aws, azure, gcp, k8s, docker"},
            },
        },
    },
    {
        "name": "semgrep_scan",
        "description": "Run Semgrep SAST rules on source code",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File or directory to scan"},
                "config": {"type": "string", "description": "Rule config: auto, p/security-audit, p/owasp-top-ten, p/ci, or path to rules"},
                "lang": {"type": "string", "description": "Language filter: python, javascript, go, java, etc."},
                "severity": {"type": "string", "description": "Severity: ERROR, WARNING, INFO"},
                "format": {"type": "string", "description": "Output: text, json, sarif, emacs, vim"},
                "exclude": {"type": "string", "description": "Glob patterns to exclude"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "semgrep_ci",
        "description": "Run Semgrep in CI mode with diff-aware scanning and SARIF output",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Directory to scan"},
                "config": {"type": "string", "description": "Rule config (default: auto)"},
                "baseline_ref": {"type": "string", "description": "Git ref for diff-aware scan (e.g. main)"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "kics_scan",
        "description": "Scan IaC with KICS (Checkmarx) — Terraform, K8s, Docker, Ansible, CloudFormation",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Directory or file to scan"},
                "type": {"type": "string", "description": "IaC type filter: Terraform, Kubernetes, Dockerfile, Ansible, CloudFormation"},
                "format": {"type": "string", "description": "Output: json, sarif, html, pdf"},
                "severity": {"type": "string", "description": "Severity: critical, high, medium, low, info"},
                "exclude_queries": {"type": "string", "description": "Comma-separated query IDs to exclude"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "tflint_check",
        "description": "Lint Terraform files for errors, deprecated syntax, and best practices",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Terraform directory"},
                "format": {"type": "string", "description": "Output: default, json, sarif"},
                "module": {"type": "boolean", "description": "Enable module inspection"},
                "config": {"type": "string", "description": "Path to .tflint.hcl config"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "cfn_lint_check",
        "description": "Lint AWS CloudFormation templates for errors and best practices",
        "inputSchema": {
            "type": "object",
            "properties": {
                "template": {"type": "string", "description": "Path to CloudFormation template (YAML/JSON)"},
                "format": {"type": "string", "description": "Output: default, json, sarif"},
                "regions": {"type": "string", "description": "AWS regions to validate against (comma-separated)"},
                "ignore_checks": {"type": "string", "description": "Comma-separated check IDs to ignore"},
            },
            "required": ["template"],
        },
    },
]


async def dispatch_tool(name: str, args: Dict) -> str:
    if name == "tfsec_scan":
        cmd = [_find_tool("tfsec"), args["path"]]
        if args.get("format"):
            cmd.extend(["--format", args["format"]])
        else:
            cmd.extend(["--format", "json"])
        if args.get("severity"):
            cmd.extend(["--minimum-severity", args["severity"]])
        if args.get("exclude"):
            cmd.extend(["--exclude", args["exclude"]])
        if args.get("tfvars"):
            cmd.extend(["--tfvars-file", args["tfvars"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "tfsec_custom":
        cmd = [_find_tool("tfsec"), args["path"], "--format", "json"]
        if args.get("config"):
            cmd.extend(["--config-file", args["config"]])
        if args.get("custom_rules"):
            cmd.extend(["--custom-check-dir", args["custom_rules"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "checkov_scan":
        cmd = [_find_tool("checkov"), "-d", args["path"]]
        if args.get("framework"):
            cmd.extend(["--framework", args["framework"]])
        if args.get("format"):
            cmd.extend(["-o", args["format"]])
        else:
            cmd.extend(["-o", "json"])
        if args.get("check"):
            cmd.extend(["--check", args["check"]])
        if args.get("skip_check"):
            cmd.extend(["--skip-check", args["skip_check"]])
        if args.get("compact"):
            cmd.append("--compact")
        if args.get("soft_fail"):
            cmd.append("--soft-fail")
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "checkov_framework":
        cmd = [_find_tool("checkov"), "-d", args["path"],
               "--framework", args["framework"]]
        if args.get("format"):
            cmd.extend(["-o", args["format"]])
        else:
            cmd.extend(["-o", "json"])
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "checkov_check":
        cmd = [_find_tool("checkov"), "-d", args["path"],
               "--check", args["check_id"], "-o", "json"]
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "terrascan_scan":
        cmd = [_find_tool("terrascan"), "scan", "-d", args["path"]]
        if args.get("iac_type"):
            cmd.extend(["-i", args["iac_type"]])
        if args.get("policy_type"):
            cmd.extend(["-t", args["policy_type"]])
        if args.get("format"):
            cmd.extend(["-o", args["format"]])
        else:
            cmd.extend(["-o", "json"])
        if args.get("severity"):
            cmd.extend(["--severity", args["severity"]])
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "terrascan_list_policies":
        cmd = [_find_tool("terrascan"), "list-policies"]
        if args.get("policy_type"):
            cmd.extend(["-t", args["policy_type"]])
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "semgrep_scan":
        cmd = [_find_tool("semgrep"), "scan", args["path"]]
        config = args.get("config", "auto")
        cmd.extend(["--config", config])
        if args.get("lang"):
            cmd.extend(["--lang", args["lang"]])
        if args.get("severity"):
            cmd.extend(["--severity", args["severity"]])
        if args.get("format"):
            if args["format"] == "json":
                cmd.append("--json")
            elif args["format"] == "sarif":
                cmd.append("--sarif")
            else:
                cmd.extend(["--output-format", args["format"]])
        else:
            cmd.append("--json")
        if args.get("exclude"):
            cmd.extend(["--exclude", args["exclude"]])
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "semgrep_ci":
        cmd = [_find_tool("semgrep"), "ci", args["path"]]
        config = args.get("config", "auto")
        cmd.extend(["--config", config, "--sarif"])
        if args.get("baseline_ref"):
            cmd.extend(["--baseline-commit", args["baseline_ref"]])
        r = _run_tool(cmd, timeout=900)
        return json.dumps(r, indent=2)

    elif name == "kics_scan":
        cmd = [_find_tool("kics"), "scan", "-p", args["path"]]
        if args.get("type"):
            cmd.extend(["-t", args["type"]])
        if args.get("format"):
            cmd.extend(["--report-formats", args["format"]])
        else:
            cmd.extend(["--report-formats", "json"])
        if args.get("severity"):
            cmd.extend(["--fail-on", args["severity"]])
        if args.get("exclude_queries"):
            cmd.extend(["--exclude-queries", args["exclude_queries"]])
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "tflint_check":
        cmd = [_find_tool("tflint"), "--chdir", args["path"]]
        if args.get("format"):
            cmd.extend(["--format", args["format"]])
        else:
            cmd.extend(["--format", "json"])
        if args.get("module"):
            cmd.append("--module")
        if args.get("config"):
            cmd.extend(["--config", args["config"]])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "cfn_lint_check":
        cmd = [_find_tool("cfn-lint"), args["template"]]
        if args.get("format"):
            cmd.extend(["--format", args["format"]])
        else:
            cmd.extend(["--format", "json"])
        if args.get("regions"):
            cmd.extend(["--regions", args["regions"]])
        if args.get("ignore_checks"):
            for check in args["ignore_checks"].split(","):
                cmd.extend(["--ignore-checks", check.strip()])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    return json.dumps({"error": f"Unknown tool: {name}"})


async def handle_message(msg: Dict) -> Optional[Dict]:
    method = msg.get("method", "")
    mid = msg.get("id")
    if method == "initialize":
        return {
            "jsonrpc": "2.0", "id": mid,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": SERVER_NAME, "version": VERSION},
            },
        }
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = msg.get("params", {})
        tname = params.get("name", "")
        targs = params.get("arguments", {})
        try:
            result_text = await dispatch_tool(tname, targs)
        except Exception as exc:
            result_text = json.dumps({"error": str(exc)})
        return {
            "jsonrpc": "2.0", "id": mid,
            "result": {"content": [{"type": "text", "text": result_text}]},
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    return {
        "jsonrpc": "2.0", "id": mid,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def _write_msg(data: Dict):
    body = json.dumps(data)
    frame = f"Content-Length: {len(body)}\r\n\r\n{body}"
    sys.stdout.buffer.write(frame.encode("utf-8"))
    sys.stdout.buffer.flush()


async def main_loop():
    if sys.platform == "win32":
        import msvcrt
        msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    buf = b""
    logger.info(f"{SERVER_NAME} v{VERSION} started")
    while True:
        chunk = sys.stdin.buffer.read(1)
        if not chunk:
            break
        buf += chunk
        while b"\r\n\r\n" in buf:
            header, rest = buf.split(b"\r\n\r\n", 1)
            cl = 0
            for line in header.decode("utf-8", errors="replace").split("\r\n"):
                if line.lower().startswith("content-length:"):
                    cl = int(line.split(":", 1)[1].strip())
            if len(rest) < cl:
                buf = header + b"\r\n\r\n" + rest
                break
            body = rest[:cl]
            buf = rest[cl:]
            try:
                msg = json.loads(body)
            except json.JSONDecodeError:
                continue
            resp = await handle_message(msg)
            if resp:
                _write_msg(resp)


def main():
    asyncio.run(main_loop())


if __name__ == "__main__":
    main()
