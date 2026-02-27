#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP OSINT Server v1.0.0

    Open Source Intelligence gathering MCP server.
    Integrates: shodan, maigret, dnstwist, holehe, sherlock, recon-ng, spiderfoot.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (14):
        - shodan_host: Query Shodan for host information
        - shodan_search: Search Shodan for devices/services
        - shodan_exploits: Search Shodan's exploit database
        - shodan_honeypot: Check if host is a honeypot
        - maigret_search: Search username across 2500+ sites
        - sherlock_search: Hunt usernames across social networks
        - holehe_check: Check if email is registered on sites
        - dnstwist_scan: Detect typosquatting, phishing domains
        - recon_ng_run: Run recon-ng reconnaissance framework modules
        - spiderfoot_scan: Automated OSINT collection
        - phoneinfoga_scan: Phone number OSINT
        - social_analyzer: Social media analysis and correlation
        - ghunt_scan: Google account OSINT
        - twint_search: Twitter OSINT without API

    Author: ThiagoFrag / LEVIATHAN VS
    Version: 1.0.0
    Inspired by: BurtTheCoder/mcp-shodan, BurtTheCoder/mcp-maigret
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
logger = logging.getLogger("leviathan-osint-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-osint-server"


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
        "name": "shodan_host",
        "description": "Query Shodan for detailed host info - open ports, services, vulns, geolocation",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ip": {"type": "string", "description": "Target IP address"},
            },
            "required": ["ip"],
        },
    },
    {
        "name": "shodan_search",
        "description": "Search Shodan for internet-connected devices and services",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Shodan search query (e.g. 'apache', 'port:22 country:BR')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results (default: 10)",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "shodan_exploits",
        "description": "Search Shodan's exploit database for known vulnerabilities",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (e.g. 'Apache 2.4', 'CVE-2021-44228')",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "shodan_honeypot",
        "description": "Check if an IP address is a known honeypot",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ip": {"type": "string", "description": "Target IP address"},
            },
            "required": ["ip"],
        },
    },
    {
        "name": "maigret_search",
        "description": "Search username across 2500+ sites (social, forums, dating, etc.)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "Username to search"},
                "top_sites": {"type": "integer", "description": "Limit to top N sites"},
                "timeout": {
                    "type": "integer",
                    "description": "Connection timeout per site",
                },
            },
            "required": ["username"],
        },
    },
    {
        "name": "sherlock_search",
        "description": "Hunt usernames across 400+ social networks",
        "inputSchema": {
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "Username to search"},
                "site": {"type": "string", "description": "Specific site to check"},
                "timeout": {"type": "integer"},
            },
            "required": ["username"],
        },
    },
    {
        "name": "holehe_check",
        "description": "Check if email is registered on various platforms (Twitter, Instagram, etc.)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "Email address to check"},
            },
            "required": ["email"],
        },
    },
    {
        "name": "dnstwist_scan",
        "description": "Detect typosquatting, phishing, and brand impersonation domains",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target domain"},
                "registered": {
                    "type": "boolean",
                    "description": "Show only registered domains",
                },
                "ssdeep": {
                    "type": "boolean",
                    "description": "Fuzzy hash comparison of web pages",
                },
                "mxcheck": {"type": "boolean", "description": "Check MX records"},
            },
            "required": ["domain"],
        },
    },
    {
        "name": "recon_ng_run",
        "description": "Run recon-ng modules for reconnaissance (requires recon-ng installed)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "module": {
                    "type": "string",
                    "description": "Module path (e.g. recon/domains-hosts/hackertarget)",
                },
                "source": {
                    "type": "string",
                    "description": "Source value for the module",
                },
                "workspace": {"type": "string", "description": "Workspace name"},
            },
            "required": ["module", "source"],
        },
    },
    {
        "name": "spiderfoot_scan",
        "description": "Automated OSINT collection across multiple data sources",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "Target (domain, IP, email, phone, etc.)",
                },
                "modules": {
                    "type": "string",
                    "description": "Specific modules to run (comma-separated)",
                },
                "max_threads": {"type": "integer"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "phoneinfoga_scan",
        "description": "Gather information about a phone number (carrier, location, reputation)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "number": {
                    "type": "string",
                    "description": "Phone number with country code (e.g. +5511999999999)",
                },
            },
            "required": ["number"],
        },
    },
    {
        "name": "social_analyzer",
        "description": "Analyze and correlate social media profiles across platforms",
        "inputSchema": {
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "Username to analyze"},
                "metadata": {"type": "boolean", "description": "Extract metadata"},
            },
            "required": ["username"],
        },
    },
    {
        "name": "ghunt_scan",
        "description": "Google account OSINT - find info from Gmail address",
        "inputSchema": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "Gmail address to investigate",
                },
            },
            "required": ["email"],
        },
    },
    {
        "name": "twint_search",
        "description": "Twitter/X OSINT without API - search tweets, profiles, followers",
        "inputSchema": {
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "Target username"},
                "search": {"type": "string", "description": "Search query"},
                "limit": {"type": "integer", "description": "Max tweets"},
            },
        },
    },
]


# ---------------------------------------------------------------------------
# Tool dispatch
# ---------------------------------------------------------------------------


async def dispatch_tool(name: str, args: Dict) -> str:
    if name == "shodan_host":
        cmd = [_find_tool("shodan"), "host", args["ip"]]
        r = _run_tool(cmd, timeout=30)
        return json.dumps(r, indent=2)

    elif name == "shodan_search":
        limit = args.get("limit", 10)
        cmd = [_find_tool("shodan"), "search", "--limit", str(limit), args["query"]]
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "shodan_exploits":
        cmd = [_find_tool("shodan"), "search", "--exploits", args["query"]]
        r = _run_tool(cmd, timeout=30)
        return json.dumps(r, indent=2)

    elif name == "shodan_honeypot":
        cmd = [_find_tool("shodan"), "honeyscore", args["ip"]]
        r = _run_tool(cmd, timeout=15)
        return json.dumps(r, indent=2)

    elif name == "maigret_search":
        cmd = [_find_tool("maigret"), args["username"]]
        if args.get("top_sites"):
            cmd.extend(["--top-sites", str(args["top_sites"])])
        if args.get("timeout"):
            cmd.extend(["--timeout", str(args["timeout"])])
        r = _run_tool(cmd, timeout=args.get("timeout", 300))
        return json.dumps(r, indent=2)

    elif name == "sherlock_search":
        cmd = [_find_tool("sherlock"), args["username"]]
        if args.get("site"):
            cmd.extend(["--site", args["site"]])
        if args.get("timeout"):
            cmd.extend(["--timeout", str(args["timeout"])])
        r = _run_tool(cmd, timeout=args.get("timeout", 300))
        return json.dumps(r, indent=2)

    elif name == "holehe_check":
        cmd = [_find_tool("holehe"), args["email"]]
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "dnstwist_scan":
        cmd = [_find_tool("dnstwist"), args["domain"]]
        if args.get("registered"):
            cmd.append("--registered")
        if args.get("ssdeep"):
            cmd.append("--ssdeep")
        if args.get("mxcheck"):
            cmd.append("--mxcheck")
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "recon_ng_run":
        ws = args.get("workspace", "default")
        commands = f"workspaces load {ws}\nmodules load {args['module']}\noptions set SOURCE {args['source']}\nrun\nexit"
        cmd = [_find_tool("recon-ng")]
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "spiderfoot_scan":
        cmd = [_find_tool("spiderfoot"), "-s", args["target"], "-q"]
        if args.get("modules"):
            cmd.extend(["-m", args["modules"]])
        if args.get("max_threads"):
            cmd.extend(["-T", str(args["max_threads"])])
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "phoneinfoga_scan":
        cmd = [_find_tool("phoneinfoga"), "scan", "-n", args["number"]]
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "social_analyzer":
        cmd = [_find_tool("social-analyzer"), "--username", args["username"]]
        if args.get("metadata"):
            cmd.append("--metadata")
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "ghunt_scan":
        cmd = [_find_tool("ghunt"), "email", args["email"]]
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "twint_search":
        cmd = [_find_tool("twint")]
        if args.get("username"):
            cmd.extend(["-u", args["username"]])
        if args.get("search"):
            cmd.extend(["-s", args["search"]])
        if args.get("limit"):
            cmd.extend(["--limit", str(args["limit"])])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

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
