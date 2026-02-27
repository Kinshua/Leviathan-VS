#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP Cloud Security Server v1.0.0

    Cloud Security, Supply Chain & Static Analysis MCP server.
    Integrates: trivy, gitleaks, prowler, semgrep, trufflehog, checkov,
                kube-hunter, scout-suite, grype, syft.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (14):
        - trivy_image: Scan container images for vulnerabilities
        - trivy_fs: Scan filesystem/project for vulns and misconfigs
        - trivy_iac: Scan Infrastructure as Code (Terraform, CloudFormation, etc.)
        - trivy_sbom: Generate Software Bill of Materials
        - gitleaks_detect: Scan git repos for secrets/credentials
        - gitleaks_protect: Pre-commit secret detection
        - trufflehog_scan: Deep credential scanning (git history, S3, etc.)
        - semgrep_scan: Lightweight static analysis with custom rules
        - semgrep_ci: Run Semgrep in CI mode with SARIF output
        - checkov_scan: IaC static analysis (Terraform, K8s, Docker, etc.)
        - prowler_audit: AWS/Azure/GCP security auditing
        - kube_hunter_scan: Kubernetes cluster penetration testing
        - grype_scan: Container vulnerability scanner (anchore)
        - syft_sbom: Generate SBOM from container images

    Author: ThiagoFrag / LEVIATHAN VS
    Version: 1.0.0
    Inspired by: FuzzingLabs/mcp-security-hub cloud & supply chain
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
logger = logging.getLogger("leviathan-cloud-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-cloud-server"


def _find_tool(name: str) -> str:
    p = shutil.which(name)
    return p if p else name


def _run_tool(cmd: List[str], timeout: int = 300) -> Dict:
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
        "name": "trivy_image",
        "description": "Scan container images for OS and application vulnerabilities",
        "inputSchema": {
            "type": "object",
            "properties": {
                "image": {
                    "type": "string",
                    "description": "Container image (e.g. nginx:latest, ubuntu:22.04)",
                },
                "severity": {
                    "type": "string",
                    "description": "Filter by severity: CRITICAL,HIGH,MEDIUM,LOW",
                },
                "format": {
                    "type": "string",
                    "description": "Output format: table, json, sarif",
                },
            },
            "required": ["image"],
        },
    },
    {
        "name": "trivy_fs",
        "description": "Scan filesystem/project for vulnerabilities and misconfigurations",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to directory to scan"},
                "severity": {"type": "string", "description": "Filter by severity"},
                "scanners": {
                    "type": "string",
                    "description": "Scanners: vuln, misconfig, secret, license",
                },
            },
            "required": ["path"],
        },
    },
    {
        "name": "trivy_iac",
        "description": "Scan Infrastructure as Code files (Terraform, CloudFormation, Dockerfile, K8s)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to IaC files"},
                "severity": {"type": "string", "description": "Filter by severity"},
                "format": {"type": "string", "description": "Output format"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "trivy_sbom",
        "description": "Generate Software Bill of Materials from image or filesystem",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Image name or path"},
                "format": {
                    "type": "string",
                    "description": "SBOM format: cyclonedx, spdx, spdx-json",
                },
            },
            "required": ["target"],
        },
    },
    {
        "name": "gitleaks_detect",
        "description": "Scan git repositories for hardcoded secrets, API keys, credentials",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to git repository"},
                "config": {
                    "type": "string",
                    "description": "Path to custom gitleaks config",
                },
                "verbose": {"type": "boolean", "description": "Enable verbose output"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "gitleaks_protect",
        "description": "Pre-commit secret detection - scan staged changes only",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to git repository"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "trufflehog_scan",
        "description": "Deep credential scanning through git history, S3 buckets, filesystems",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source_type": {
                    "type": "string",
                    "description": "Source: git, github, s3, filesystem",
                },
                "target": {
                    "type": "string",
                    "description": "Target (repo URL, bucket name, path)",
                },
                "only_verified": {
                    "type": "boolean",
                    "description": "Only show verified credentials",
                },
            },
            "required": ["source_type", "target"],
        },
    },
    {
        "name": "semgrep_scan",
        "description": "Lightweight static analysis with 2000+ rules for security bugs",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to scan"},
                "config": {
                    "type": "string",
                    "description": "Rule config (e.g. p/security-audit, p/owasp-top-ten)",
                },
                "lang": {
                    "type": "string",
                    "description": "Language filter (python, javascript, etc.)",
                },
                "severity": {
                    "type": "string",
                    "description": "Filter: ERROR, WARNING, INFO",
                },
            },
            "required": ["path"],
        },
    },
    {
        "name": "semgrep_ci",
        "description": "Run Semgrep in CI mode with SARIF/JSON output for integration",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to scan"},
                "config": {"type": "string", "description": "Rule config"},
                "output": {"type": "string", "description": "Output file path"},
                "format": {
                    "type": "string",
                    "description": "Output format: sarif, json, text",
                },
            },
            "required": ["path"],
        },
    },
    {
        "name": "checkov_scan",
        "description": "IaC static analysis - Terraform, K8s manifests, Dockerfiles, ARM templates",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to IaC files or directory",
                },
                "framework": {
                    "type": "string",
                    "description": "Framework: terraform, kubernetes, dockerfile, cloudformation, arm",
                },
                "check": {"type": "string", "description": "Specific check IDs to run"},
                "output": {
                    "type": "string",
                    "description": "Output format: cli, json, sarif",
                },
            },
            "required": ["path"],
        },
    },
    {
        "name": "prowler_audit",
        "description": "Comprehensive cloud security auditing for AWS, Azure, GCP",
        "inputSchema": {
            "type": "object",
            "properties": {
                "provider": {
                    "type": "string",
                    "description": "Cloud provider: aws, azure, gcp",
                },
                "service": {
                    "type": "string",
                    "description": "Specific service to audit (e.g. s3, iam, ec2)",
                },
                "severity": {
                    "type": "string",
                    "description": "Filter: critical, high, medium, low",
                },
                "output_format": {
                    "type": "string",
                    "description": "Output: json, csv, html",
                },
            },
            "required": ["provider"],
        },
    },
    {
        "name": "kube_hunter_scan",
        "description": "Kubernetes cluster security assessment and penetration testing",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "Target: IP, CIDR range, or 'internal' for in-cluster",
                },
                "active": {
                    "type": "boolean",
                    "description": "Enable active hunting (exploitation attempts)",
                },
            },
            "required": ["target"],
        },
    },
    {
        "name": "grype_scan",
        "description": "Scan container images and filesystems for vulnerabilities (Anchore)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "Container image or dir: path (e.g. nginx:latest, dir:./project)",
                },
                "severity": {
                    "type": "string",
                    "description": "Filter: critical, high, medium, low, negligible",
                },
                "format": {
                    "type": "string",
                    "description": "Output format: table, json, cyclonedx, sarif",
                },
            },
            "required": ["target"],
        },
    },
    {
        "name": "syft_sbom",
        "description": "Generate SBOM from container images, filesystems, archives",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "Source: image, dir, archive (e.g. nginx:latest, dir:.)",
                },
                "format": {
                    "type": "string",
                    "description": "Output: syft-json, cyclonedx-json, spdx-json, table",
                },
            },
            "required": ["target"],
        },
    },
]


# ---------------------------------------------------------------------------
# Tool dispatch
# ---------------------------------------------------------------------------


async def dispatch_tool(name: str, args: Dict) -> str:
    if name == "trivy_image":
        cmd = [_find_tool("trivy"), "image"]
        if args.get("severity"):
            cmd.extend(["--severity", args["severity"]])
        if args.get("format"):
            cmd.extend(["--format", args["format"]])
        cmd.append(args["image"])
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    elif name == "trivy_fs":
        cmd = [_find_tool("trivy"), "fs"]
        if args.get("severity"):
            cmd.extend(["--severity", args["severity"]])
        if args.get("scanners"):
            cmd.extend(["--scanners", args["scanners"]])
        cmd.append(args["path"])
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    elif name == "trivy_iac":
        cmd = [_find_tool("trivy"), "config"]
        if args.get("severity"):
            cmd.extend(["--severity", args["severity"]])
        if args.get("format"):
            cmd.extend(["--format", args["format"]])
        cmd.append(args["path"])
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    elif name == "trivy_sbom":
        fmt = args.get("format", "cyclonedx")
        cmd = [_find_tool("trivy"), "sbom", "--format", fmt, args["target"]]
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    elif name == "gitleaks_detect":
        cmd = [_find_tool("gitleaks"), "detect", "--source", args["path"]]
        if args.get("config"):
            cmd.extend(["--config", args["config"]])
        if args.get("verbose"):
            cmd.append("-v")
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    elif name == "gitleaks_protect":
        cmd = [_find_tool("gitleaks"), "protect", "--source", args["path"], "--staged"]
        return json.dumps(_run_tool(cmd, timeout=60), indent=2)

    elif name == "trufflehog_scan":
        src_type = args["source_type"]
        cmd = [_find_tool("trufflehog"), src_type, args["target"]]
        if args.get("only_verified"):
            cmd.append("--only-verified")
        return json.dumps(_run_tool(cmd, timeout=600), indent=2)

    elif name == "semgrep_scan":
        config = args.get("config", "p/security-audit")
        cmd = [_find_tool("semgrep"), "scan", "--config", config, args["path"]]
        if args.get("lang"):
            cmd.extend(["--lang", args["lang"]])
        if args.get("severity"):
            cmd.extend(["--severity", args["severity"]])
        return json.dumps(_run_tool(cmd, timeout=600), indent=2)

    elif name == "semgrep_ci":
        config = args.get("config", "p/security-audit")
        cmd = [_find_tool("semgrep"), "ci", "--config", config]
        fmt = args.get("format", "sarif")
        if args.get("output"):
            cmd.extend([f"--{fmt}", "--output", args["output"]])
        cmd.append(args["path"])
        return json.dumps(_run_tool(cmd, timeout=600), indent=2)

    elif name == "checkov_scan":
        cmd = [_find_tool("checkov"), "-d", args["path"]]
        if args.get("framework"):
            cmd.extend(["--framework", args["framework"]])
        if args.get("check"):
            cmd.extend(["--check", args["check"]])
        if args.get("output"):
            cmd.extend(["--output", args["output"]])
        return json.dumps(_run_tool(cmd, timeout=600), indent=2)

    elif name == "prowler_audit":
        cmd = [_find_tool("prowler"), args["provider"]]
        if args.get("service"):
            cmd.extend(["--service", args["service"]])
        if args.get("severity"):
            cmd.extend(["--severity", args["severity"]])
        if args.get("output_format"):
            cmd.extend(["-M", args["output_format"]])
        return json.dumps(_run_tool(cmd, timeout=900), indent=2)

    elif name == "kube_hunter_scan":
        target = args["target"]
        cmd = [_find_tool("kube-hunter")]
        if target == "internal":
            cmd.append("--internal")
        else:
            cmd.extend(["--remote", target])
        if args.get("active"):
            cmd.append("--active")
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    elif name == "grype_scan":
        cmd = [_find_tool("grype"), args["target"]]
        if args.get("severity"):
            cmd.extend(["--only-fixed", "--fail-on", args["severity"]])
        if args.get("format"):
            cmd.extend(["-o", args["format"]])
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    elif name == "syft_sbom":
        fmt = args.get("format", "syft-json")
        cmd = [_find_tool("syft"), args["target"], "-o", fmt]
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    return json.dumps({"error": f"Unknown tool: {name}"})


# ---------------------------------------------------------------------------
# JSON-RPC / MCP boilerplate
# ---------------------------------------------------------------------------


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
