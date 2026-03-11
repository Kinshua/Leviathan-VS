#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP Container Security Server v1.0.0

    Container and Kubernetes security MCP server.
    Integrates: trivy, kube-bench, grype, syft, hadolint, kubectl.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (14):
        - trivy_image: Scan container image for vulnerabilities
        - trivy_fs: Scan filesystem/project for vulnerabilities
        - trivy_repo: Scan git repo for vulnerabilities
        - trivy_k8s: Scan Kubernetes cluster for misconfigurations
        - trivy_sbom: Generate SBOM (Software Bill of Materials)
        - grype_scan: Scan image/directory for vulnerabilities (Anchore)
        - syft_analyze: Generate detailed SBOM with syft
        - hadolint_check: Lint Dockerfile for best practices
        - kube_bench_run: Run CIS Kubernetes Benchmark checks
        - kubectl_audit: Audit Kubernetes resources for security issues
        - kubectl_secrets: List and analyze Kubernetes secrets
        - kubectl_rbac: Analyze RBAC permissions and over-privileges
        - kubectl_netpol: Check network policies and exposure
        - kubectl_pods_security: Check pod security standards compliance

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
logger = logging.getLogger("leviathan-container-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-container-server"


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
        "name": "trivy_image",
        "description": "Scan container image for vulnerabilities, misconfigurations, and secrets",
        "inputSchema": {
            "type": "object",
            "properties": {
                "image": {"type": "string", "description": "Image name (e.g. nginx:latest, ubuntu:22.04)"},
                "severity": {"type": "string", "description": "Filter by severity: CRITICAL,HIGH,MEDIUM,LOW"},
                "ignore_unfixed": {"type": "boolean", "description": "Ignore vulnerabilities without fixes"},
                "format": {"type": "string", "description": "Output format: table, json, sarif, cyclonedx"},
                "scanners": {"type": "string", "description": "Scanners: vuln,misconfig,secret,license"},
                "timeout": {"type": "integer", "description": "Timeout in seconds"},
            },
            "required": ["image"],
        },
    },
    {
        "name": "trivy_fs",
        "description": "Scan filesystem/project for vulnerabilities in dependencies",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Directory or file path to scan"},
                "severity": {"type": "string", "description": "Severity filter"},
                "format": {"type": "string", "description": "Output format: table, json, sarif"},
                "scanners": {"type": "string", "description": "Scanners: vuln,misconfig,secret,license"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "trivy_repo",
        "description": "Scan git repository for vulnerabilities",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo": {"type": "string", "description": "Git repo URL"},
                "branch": {"type": "string", "description": "Branch to scan"},
                "severity": {"type": "string", "description": "Severity filter"},
                "format": {"type": "string", "description": "Output format"},
            },
            "required": ["repo"],
        },
    },
    {
        "name": "trivy_k8s",
        "description": "Scan Kubernetes cluster for misconfigurations and vulnerabilities",
        "inputSchema": {
            "type": "object",
            "properties": {
                "context": {"type": "string", "description": "Kubernetes context name"},
                "namespace": {"type": "string", "description": "Namespace to scan (default: all)"},
                "severity": {"type": "string", "description": "Severity filter"},
                "report": {"type": "string", "description": "Report type: summary, all"},
                "format": {"type": "string", "description": "Output format"},
            },
        },
    },
    {
        "name": "trivy_sbom",
        "description": "Generate Software Bill of Materials for image or filesystem",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Image name or filesystem path"},
                "format": {"type": "string", "description": "SBOM format: cyclonedx, spdx, spdx-json"},
                "output": {"type": "string", "description": "Output file path"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "grype_scan",
        "description": "Scan image or directory for vulnerabilities using Anchore Grype",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Image, directory (dir:path), or SBOM file"},
                "fail_on": {"type": "string", "description": "Fail on severity: critical, high, medium, low"},
                "only_fixed": {"type": "boolean", "description": "Only show vulnerabilities with fixes"},
                "format": {"type": "string", "description": "Output format: table, json, cyclonedx, sarif"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "syft_analyze",
        "description": "Generate detailed SBOM with Syft (packages, licenses, metadata)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Image name or dir:path"},
                "format": {"type": "string", "description": "Output: syft-json, cyclonedx-json, spdx-json, table"},
                "scope": {"type": "string", "description": "Scope: squashed (default), all-layers"},
            },
            "required": ["source"],
        },
    },
    {
        "name": "hadolint_check",
        "description": "Lint Dockerfile for best practices and security issues",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dockerfile": {"type": "string", "description": "Path to Dockerfile"},
                "format": {"type": "string", "description": "Output format: tty, json, sarif, codeclimate"},
                "ignore": {"type": "string", "description": "Comma-separated rules to ignore (e.g. DL3008,DL3009)"},
                "trusted_registries": {"type": "string", "description": "Comma-separated trusted registries"},
            },
            "required": ["dockerfile"],
        },
    },
    {
        "name": "kube_bench_run",
        "description": "Run CIS Kubernetes Benchmark security checks",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target: master, node, controlplane, etcd, policies"},
                "benchmark": {"type": "string", "description": "Benchmark version (e.g. cis-1.8, eks-1.2)"},
                "json_output": {"type": "boolean", "description": "Output as JSON"},
            },
        },
    },
    {
        "name": "kubectl_audit",
        "description": "Audit Kubernetes resources for security issues",
        "inputSchema": {
            "type": "object",
            "properties": {
                "namespace": {"type": "string", "description": "Namespace (default: all)"},
                "resource": {"type": "string", "description": "Resource type: pods, deployments, services, all"},
                "context": {"type": "string", "description": "Kubernetes context"},
            },
        },
    },
    {
        "name": "kubectl_secrets",
        "description": "List and analyze Kubernetes secrets (detect sensitive data exposure)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "namespace": {"type": "string", "description": "Namespace (default: all)"},
                "decode": {"type": "boolean", "description": "Base64-decode secret values"},
                "context": {"type": "string", "description": "Kubernetes context"},
            },
        },
    },
    {
        "name": "kubectl_rbac",
        "description": "Analyze RBAC permissions — find over-privileged service accounts",
        "inputSchema": {
            "type": "object",
            "properties": {
                "namespace": {"type": "string", "description": "Namespace (default: all)"},
                "subject": {"type": "string", "description": "Filter by subject (user/serviceaccount name)"},
                "context": {"type": "string", "description": "Kubernetes context"},
            },
        },
    },
    {
        "name": "kubectl_netpol",
        "description": "Check network policies — find exposed pods without ingress/egress rules",
        "inputSchema": {
            "type": "object",
            "properties": {
                "namespace": {"type": "string", "description": "Namespace (default: all)"},
                "context": {"type": "string", "description": "Kubernetes context"},
            },
        },
    },
    {
        "name": "kubectl_pods_security",
        "description": "Check pod security standards compliance (privileged, hostPID, capabilities)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "namespace": {"type": "string", "description": "Namespace (default: all)"},
                "context": {"type": "string", "description": "Kubernetes context"},
            },
        },
    },
]


async def dispatch_tool(name: str, args: Dict) -> str:
    if name == "trivy_image":
        cmd = [_find_tool("trivy"), "image", args["image"]]
        if args.get("severity"):
            cmd.extend(["--severity", args["severity"]])
        if args.get("ignore_unfixed"):
            cmd.append("--ignore-unfixed")
        if args.get("format"):
            cmd.extend(["--format", args["format"]])
        else:
            cmd.extend(["--format", "json"])
        if args.get("scanners"):
            cmd.extend(["--scanners", args["scanners"]])
        r = _run_tool(cmd, timeout=args.get("timeout", 600))
        return json.dumps(r, indent=2)

    elif name == "trivy_fs":
        cmd = [_find_tool("trivy"), "fs", args["path"]]
        if args.get("severity"):
            cmd.extend(["--severity", args["severity"]])
        if args.get("format"):
            cmd.extend(["--format", args["format"]])
        else:
            cmd.extend(["--format", "json"])
        if args.get("scanners"):
            cmd.extend(["--scanners", args["scanners"]])
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "trivy_repo":
        cmd = [_find_tool("trivy"), "repo", args["repo"]]
        if args.get("branch"):
            cmd.extend(["--branch", args["branch"]])
        if args.get("severity"):
            cmd.extend(["--severity", args["severity"]])
        if args.get("format"):
            cmd.extend(["--format", args["format"]])
        else:
            cmd.extend(["--format", "json"])
        r = _run_tool(cmd, timeout=900)
        return json.dumps(r, indent=2)

    elif name == "trivy_k8s":
        cmd = [_find_tool("trivy"), "k8s", "--format", "json"]
        if args.get("context"):
            cmd.extend(["--context", args["context"]])
        if args.get("namespace"):
            cmd.extend(["--namespace", args["namespace"]])
        else:
            cmd.append("--all-namespaces")
        if args.get("severity"):
            cmd.extend(["--severity", args["severity"]])
        if args.get("report"):
            cmd.extend(["--report", args["report"]])
        r = _run_tool(cmd, timeout=900)
        return json.dumps(r, indent=2)

    elif name == "trivy_sbom":
        cmd = [_find_tool("trivy"), "sbom", args["target"]]
        fmt = args.get("format", "cyclonedx")
        cmd.extend(["--format", fmt])
        if args.get("output"):
            cmd.extend(["--output", args["output"]])
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "grype_scan":
        cmd = [_find_tool("grype"), args["target"]]
        if args.get("fail_on"):
            cmd.extend(["--fail-on", args["fail_on"]])
        if args.get("only_fixed"):
            cmd.append("--only-fixed")
        if args.get("format"):
            cmd.extend(["-o", args["format"]])
        else:
            cmd.extend(["-o", "json"])
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "syft_analyze":
        cmd = [_find_tool("syft"), args["source"]]
        fmt = args.get("format", "syft-json")
        cmd.extend(["-o", fmt])
        if args.get("scope"):
            cmd.extend(["--scope", args["scope"]])
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "hadolint_check":
        cmd = [_find_tool("hadolint"), args["dockerfile"]]
        if args.get("format"):
            cmd.extend(["--format", args["format"]])
        else:
            cmd.extend(["--format", "json"])
        if args.get("ignore"):
            for rule in args["ignore"].split(","):
                cmd.extend(["--ignore", rule.strip()])
        if args.get("trusted_registries"):
            for reg in args["trusted_registries"].split(","):
                cmd.extend(["--trusted-registry", reg.strip()])
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "kube_bench_run":
        cmd = [_find_tool("kube-bench"), "run"]
        if args.get("target"):
            cmd.extend(["--targets", args["target"]])
        if args.get("benchmark"):
            cmd.extend(["--benchmark", args["benchmark"]])
        if args.get("json_output", True):
            cmd.append("--json")
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "kubectl_audit":
        ns = args.get("namespace")
        resource = args.get("resource", "all")
        cmd = [_find_tool("kubectl"), "get", resource, "-o", "json"]
        if args.get("context"):
            cmd.extend(["--context", args["context"]])
        if ns:
            cmd.extend(["-n", ns])
        else:
            cmd.append("--all-namespaces")
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "kubectl_secrets":
        cmd = [_find_tool("kubectl"), "get", "secrets", "-o", "json"]
        if args.get("context"):
            cmd.extend(["--context", args["context"]])
        if args.get("namespace"):
            cmd.extend(["-n", args["namespace"]])
        else:
            cmd.append("--all-namespaces")
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "kubectl_rbac":
        cmd = [_find_tool("kubectl"), "get", "clusterrolebindings,rolebindings", "-o", "json"]
        if args.get("context"):
            cmd.extend(["--context", args["context"]])
        if args.get("namespace"):
            cmd.extend(["-n", args["namespace"]])
        else:
            cmd.append("--all-namespaces")
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "kubectl_netpol":
        cmd = [_find_tool("kubectl"), "get", "networkpolicies", "-o", "json"]
        if args.get("context"):
            cmd.extend(["--context", args["context"]])
        if args.get("namespace"):
            cmd.extend(["-n", args["namespace"]])
        else:
            cmd.append("--all-namespaces")
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "kubectl_pods_security":
        cmd = [_find_tool("kubectl"), "get", "pods", "-o", "json"]
        if args.get("context"):
            cmd.extend(["--context", args["context"]])
        if args.get("namespace"):
            cmd.extend(["-n", args["namespace"]])
        else:
            cmd.append("--all-namespaces")
        r = _run_tool(cmd, timeout=60)
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
