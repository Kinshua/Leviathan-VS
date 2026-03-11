#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP Secrets Scanner Server v1.0.0

    Credential and secret detection MCP server.
    Integrates: trufflehog, gitleaks, detect-secrets, git-secrets.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (12):
        - trufflehog_git: Scan git repo for secrets (high-signal detector)
        - trufflehog_filesystem: Scan filesystem for secrets
        - trufflehog_s3: Scan S3 bucket for exposed secrets
        - trufflehog_github_org: Scan entire GitHub org for secrets
        - gitleaks_detect: Detect secrets in git history
        - gitleaks_protect: Pre-commit secret detection (CI/CD gate)
        - gitleaks_report: Generate SARIF/JSON report of findings
        - detect_secrets_scan: Scan files with detect-secrets (Yelp)
        - detect_secrets_audit: Interactive audit of detected secrets
        - detect_secrets_baseline: Create/update secrets baseline
        - git_secrets_scan: AWS-focused credential scanner
        - git_secrets_install_hooks: Install pre-commit hooks

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
logger = logging.getLogger("leviathan-secrets-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-secrets-server"


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


# ============================================================================
# TOOL DEFINITIONS
# ============================================================================

TOOLS = [
    {
        "name": "trufflehog_git",
        "description": "Scan git repository for secrets using TruffleHog v3 (high-signal, verified detectors)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo": {"type": "string", "description": "Git repo URL or local path"},
                "branch": {"type": "string", "description": "Branch to scan (default: all)"},
                "only_verified": {"type": "boolean", "description": "Only show verified/active secrets"},
                "max_depth": {"type": "integer", "description": "Max commit depth to scan"},
                "include_detectors": {"type": "string", "description": "Comma-separated detector names (e.g. AWS,GitHub,Slack)"},
                "exclude_detectors": {"type": "string", "description": "Comma-separated detectors to skip"},
                "since_commit": {"type": "string", "description": "Scan commits after this SHA"},
                "json_output": {"type": "boolean", "description": "Output as JSON (default: true)"},
            },
            "required": ["repo"],
        },
    },
    {
        "name": "trufflehog_filesystem",
        "description": "Scan local filesystem directory for secrets with TruffleHog",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Directory path to scan"},
                "only_verified": {"type": "boolean", "description": "Only verified secrets"},
                "include_detectors": {"type": "string", "description": "Comma-separated detector names"},
                "exclude_paths": {"type": "string", "description": "Regex pattern for paths to exclude"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "trufflehog_s3",
        "description": "Scan AWS S3 bucket for exposed secrets",
        "inputSchema": {
            "type": "object",
            "properties": {
                "bucket": {"type": "string", "description": "S3 bucket name"},
                "only_verified": {"type": "boolean", "description": "Only verified secrets"},
                "role_arn": {"type": "string", "description": "AWS role ARN to assume"},
            },
            "required": ["bucket"],
        },
    },
    {
        "name": "trufflehog_github_org",
        "description": "Scan all repos in a GitHub organization for secrets",
        "inputSchema": {
            "type": "object",
            "properties": {
                "org": {"type": "string", "description": "GitHub organization name"},
                "token": {"type": "string", "description": "GitHub personal access token"},
                "only_verified": {"type": "boolean", "description": "Only verified secrets"},
                "include_members": {"type": "boolean", "description": "Include member repos (not just org repos)"},
            },
            "required": ["org"],
        },
    },
    {
        "name": "gitleaks_detect",
        "description": "Detect secrets in git history using Gitleaks",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Git repo path or URL"},
                "log_opts": {"type": "string", "description": "Git log options (e.g. --since='2024-01-01')"},
                "config": {"type": "string", "description": "Path to custom gitleaks config (.toml)"},
                "baseline": {"type": "string", "description": "Path to baseline file (ignore known secrets)"},
                "verbose": {"type": "boolean", "description": "Show verbose output"},
                "no_git": {"type": "boolean", "description": "Scan directory without git history"},
                "redact": {"type": "boolean", "description": "Redact secrets in output"},
            },
            "required": ["source"],
        },
    },
    {
        "name": "gitleaks_protect",
        "description": "Pre-commit secret detection — scan staged changes only",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Git repo path"},
                "staged": {"type": "boolean", "description": "Only scan staged changes (default: true)"},
                "config": {"type": "string", "description": "Path to custom config"},
                "verbose": {"type": "boolean", "description": "Verbose output"},
            },
            "required": ["source"],
        },
    },
    {
        "name": "gitleaks_report",
        "description": "Generate findings report in JSON or SARIF format",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Git repo path"},
                "format": {"type": "string", "description": "Output format: json, sarif, csv"},
                "output": {"type": "string", "description": "Output file path"},
                "config": {"type": "string", "description": "Custom config path"},
            },
            "required": ["source"],
        },
    },
    {
        "name": "detect_secrets_scan",
        "description": "Scan files for secrets using Yelp's detect-secrets",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File or directory to scan"},
                "all_files": {"type": "boolean", "description": "Scan all files (not just tracked)"},
                "exclude_files": {"type": "string", "description": "Regex pattern for files to exclude"},
                "exclude_lines": {"type": "string", "description": "Regex pattern for lines to exclude"},
                "word_list": {"type": "string", "description": "Path to custom word list for false positive filtering"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "detect_secrets_audit",
        "description": "Audit baseline file — mark findings as true/false positives",
        "inputSchema": {
            "type": "object",
            "properties": {
                "baseline": {"type": "string", "description": "Path to .secrets.baseline file"},
                "report": {"type": "boolean", "description": "Generate audit report (non-interactive)"},
            },
            "required": ["baseline"],
        },
    },
    {
        "name": "detect_secrets_baseline",
        "description": "Create or update secrets detection baseline",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Directory to baseline"},
                "output": {"type": "string", "description": "Output file (default: .secrets.baseline)"},
                "update": {"type": "boolean", "description": "Update existing baseline"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "git_secrets_scan",
        "description": "Scan for AWS credentials and other secrets using git-secrets",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Git repo path to scan"},
                "scan_history": {"type": "boolean", "description": "Scan entire git history"},
                "recursive": {"type": "boolean", "description": "Scan recursively"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "git_secrets_install_hooks",
        "description": "Install git-secrets pre-commit hooks in a repository",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Git repo path"},
                "add_aws": {"type": "boolean", "description": "Add AWS secret patterns (default: true)"},
            },
            "required": ["path"],
        },
    },
]


# ============================================================================
# TOOL DISPATCH
# ============================================================================


async def dispatch_tool(name: str, args: Dict) -> str:
    if name == "trufflehog_git":
        cmd = [_find_tool("trufflehog"), "git", args["repo"], "--json"]
        if args.get("only_verified"):
            cmd.append("--only-verified")
        if args.get("branch"):
            cmd.extend(["--branch", args["branch"]])
        if args.get("max_depth"):
            cmd.extend(["--max-depth", str(args["max_depth"])])
        if args.get("include_detectors"):
            cmd.extend(["--include-detectors", args["include_detectors"]])
        if args.get("exclude_detectors"):
            cmd.extend(["--exclude-detectors", args["exclude_detectors"]])
        if args.get("since_commit"):
            cmd.extend(["--since-commit", args["since_commit"]])
        r = _run_tool(cmd, timeout=900)
        return json.dumps(r, indent=2)

    elif name == "trufflehog_filesystem":
        cmd = [_find_tool("trufflehog"), "filesystem", args["path"], "--json"]
        if args.get("only_verified"):
            cmd.append("--only-verified")
        if args.get("include_detectors"):
            cmd.extend(["--include-detectors", args["include_detectors"]])
        if args.get("exclude_paths"):
            cmd.extend(["--exclude-paths", args["exclude_paths"]])
        r = _run_tool(cmd, timeout=900)
        return json.dumps(r, indent=2)

    elif name == "trufflehog_s3":
        cmd = [_find_tool("trufflehog"), "s3", "--bucket", args["bucket"], "--json"]
        if args.get("only_verified"):
            cmd.append("--only-verified")
        if args.get("role_arn"):
            cmd.extend(["--role-arn", args["role_arn"]])
        r = _run_tool(cmd, timeout=1200)
        return json.dumps(r, indent=2)

    elif name == "trufflehog_github_org":
        cmd = [_find_tool("trufflehog"), "github", "--org", args["org"], "--json"]
        if args.get("only_verified"):
            cmd.append("--only-verified")
        if args.get("token"):
            cmd.extend(["--token", args["token"]])
        if args.get("include_members"):
            cmd.append("--include-members")
        r = _run_tool(cmd, timeout=1800)
        return json.dumps(r, indent=2)

    elif name == "gitleaks_detect":
        cmd = [_find_tool("gitleaks"), "detect", "--source", args["source"], "--report-format", "json"]
        if args.get("log_opts"):
            cmd.extend(["--log-opts", args["log_opts"]])
        if args.get("config"):
            cmd.extend(["--config", args["config"]])
        if args.get("baseline"):
            cmd.extend(["--baseline-path", args["baseline"]])
        if args.get("verbose"):
            cmd.append("--verbose")
        if args.get("no_git"):
            cmd.append("--no-git")
        if args.get("redact"):
            cmd.append("--redact")
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "gitleaks_protect":
        cmd = [_find_tool("gitleaks"), "protect", "--source", args["source"]]
        if args.get("staged", True):
            cmd.append("--staged")
        if args.get("config"):
            cmd.extend(["--config", args["config"]])
        if args.get("verbose"):
            cmd.append("--verbose")
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "gitleaks_report":
        fmt = args.get("format", "json")
        cmd = [_find_tool("gitleaks"), "detect", "--source", args["source"],
               "--report-format", fmt]
        if args.get("output"):
            cmd.extend(["--report-path", args["output"]])
        if args.get("config"):
            cmd.extend(["--config", args["config"]])
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "detect_secrets_scan":
        cmd = [_find_tool("detect-secrets"), "scan", args["path"]]
        if args.get("all_files"):
            cmd.append("--all-files")
        if args.get("exclude_files"):
            cmd.extend(["--exclude-files", args["exclude_files"]])
        if args.get("exclude_lines"):
            cmd.extend(["--exclude-lines", args["exclude_lines"]])
        if args.get("word_list"):
            cmd.extend(["--word-list", args["word_list"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "detect_secrets_audit":
        cmd = [_find_tool("detect-secrets"), "audit", args["baseline"]]
        if args.get("report"):
            cmd.append("--report")
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "detect_secrets_baseline":
        path = args["path"]
        output = args.get("output", ".secrets.baseline")
        if args.get("update"):
            cmd = [_find_tool("detect-secrets"), "scan", "--update", output]
        else:
            cmd = [_find_tool("detect-secrets"), "scan", path]
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "git_secrets_scan":
        cmd = [_find_tool("git-secrets"), "--scan"]
        if args.get("scan_history"):
            cmd.append("--scan-history")
        if args.get("recursive"):
            cmd.append("-r")
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "git_secrets_install_hooks":
        path = args["path"]
        results = []
        cmd1 = [_find_tool("git-secrets"), "--install"]
        r1 = _run_tool(cmd1, timeout=30)
        results.append({"install_hooks": r1})
        if args.get("add_aws", True):
            cmd2 = [_find_tool("git-secrets"), "--register-aws"]
            r2 = _run_tool(cmd2, timeout=30)
            results.append({"register_aws": r2})
        return json.dumps(results, indent=2)

    return json.dumps({"error": f"Unknown tool: {name}"})


# ============================================================================
# JSON-RPC 2.0 PROTOCOL
# ============================================================================


async def handle_message(msg: Dict) -> Optional[Dict]:
    method = msg.get("method", "")
    mid = msg.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": mid,
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
            "jsonrpc": "2.0",
            "id": mid,
            "result": {"content": [{"type": "text", "text": result_text}]},
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    return {
        "jsonrpc": "2.0",
        "id": mid,
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
