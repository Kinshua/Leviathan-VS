#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP WebApp Security Server v1.0.0

    Web Application Security Testing MCP server.
    Integrates: xsstrike, wfuzz, arjun, gospider, paramspider, commix,
                dalfox, jwt_tool, nosqlmap, ssrfmap.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (14):
        - xsstrike_scan: Advanced XSS detection and exploitation
        - xsstrike_crawl: Crawl and find XSS across entire site
        - wfuzz_fuzz: Web application fuzzer (dirs, params, headers)
        - wfuzz_payloads: List available wfuzz payloads/encoders
        - arjun_discover: HTTP parameter discovery
        - gospider_crawl: Fast web spider/crawler in Go
        - paramspider_mine: Mine parameters from web archives
        - commix_inject: Automated command injection testing
        - dalfox_scan: Parameter analysis and XSS scanning
        - jwt_tool_analyze: JWT token analysis, cracking, and tampering
        - jwt_tool_tamper: Forge/tamper JWT tokens
        - nosqlmap_scan: NoSQL injection detection and exploitation
        - ssrfmap_scan: Server-Side Request Forgery exploitation
        - crlfuzz_scan: CRLF injection vulnerability scanner

    Author: ThiagoFrag / LEVIATHAN VS
    Version: 1.0.0
    Inspired by: securityfortech/secops-mcp, FuzzingLabs/mcp-security-hub
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
logger = logging.getLogger("leviathan-webapp-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-webapp-server"


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
        "name": "xsstrike_scan",
        "description": "Advanced XSS detection with smart payload generation and WAF bypass",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Target URL with parameter (e.g. http://target.com/page?q=test)",
                },
                "data": {
                    "type": "string",
                    "description": "POST data (triggers POST mode)",
                },
                "headers": {
                    "type": "string",
                    "description": "Custom headers as JSON string",
                },
                "blind": {"type": "boolean", "description": "Enable blind XSS mode"},
            },
            "required": ["url"],
        },
    },
    {
        "name": "xsstrike_crawl",
        "description": "Crawl a website and test all found parameters for XSS",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Starting URL to crawl"},
                "level": {"type": "integer", "description": "Crawl depth level (1-3)"},
            },
            "required": ["url"],
        },
    },
    {
        "name": "wfuzz_fuzz",
        "description": "Fuzz web applications - directories, parameters, headers, cookies",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Target URL with FUZZ keyword (e.g. http://target.com/FUZZ)",
                },
                "wordlist": {"type": "string", "description": "Path to wordlist file"},
                "method": {
                    "type": "string",
                    "description": "HTTP method (GET, POST, etc.)",
                },
                "data": {
                    "type": "string",
                    "description": "POST data with FUZZ keyword",
                },
                "header": {
                    "type": "string",
                    "description": "Custom header (e.g. 'Cookie: FUZZ')",
                },
                "hide_code": {
                    "type": "string",
                    "description": "Hide responses with these status codes (e.g. '404,403')",
                },
                "hide_chars": {
                    "type": "string",
                    "description": "Hide responses with this char count",
                },
            },
            "required": ["url", "wordlist"],
        },
    },
    {
        "name": "wfuzz_payloads",
        "description": "List available wfuzz payload types and encoders",
        "inputSchema": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "description": "List type: payloads, encoders, iterators, printers",
                },
            },
            "required": ["type"],
        },
    },
    {
        "name": "arjun_discover",
        "description": "Discover hidden HTTP parameters in web applications",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target URL"},
                "method": {
                    "type": "string",
                    "description": "HTTP method: GET, POST, JSON",
                },
                "wordlist": {
                    "type": "string",
                    "description": "Custom parameter wordlist",
                },
                "threads": {"type": "integer", "description": "Number of threads"},
            },
            "required": ["url"],
        },
    },
    {
        "name": "gospider_crawl",
        "description": "Fast web spider - find subdomains, JS files, links, forms",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target URL or site"},
                "depth": {"type": "integer", "description": "Crawl depth"},
                "concurrent": {"type": "integer", "description": "Concurrent requests"},
                "include_subs": {
                    "type": "boolean",
                    "description": "Include subdomains",
                },
            },
            "required": ["url"],
        },
    },
    {
        "name": "paramspider_mine",
        "description": "Mine parameters from web archives (Wayback Machine, CommonCrawl)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target domain"},
                "exclude": {
                    "type": "string",
                    "description": "Exclude extensions (e.g. 'css,jpg,png')",
                },
                "level": {"type": "string", "description": "high or low (strictness)"},
            },
            "required": ["domain"],
        },
    },
    {
        "name": "commix_inject",
        "description": "Automated command injection detection and exploitation",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target URL"},
                "data": {"type": "string", "description": "POST data"},
                "cookie": {"type": "string", "description": "HTTP cookie"},
                "level": {"type": "integer", "description": "Level of tests (1-3)"},
                "technique": {
                    "type": "string",
                    "description": "Injection technique: classic, eval-based, time-based, file-based",
                },
            },
            "required": ["url"],
        },
    },
    {
        "name": "dalfox_scan",
        "description": "Parameter analysis and XSS scanning with DOM analysis",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target URL"},
                "method": {"type": "string", "description": "HTTP method"},
                "blind": {"type": "string", "description": "Blind XSS callback URL"},
                "custom_payload": {
                    "type": "string",
                    "description": "Custom XSS payload",
                },
            },
            "required": ["url"],
        },
    },
    {
        "name": "jwt_tool_analyze",
        "description": "Analyze JWT tokens - decode, check algorithm, find weaknesses",
        "inputSchema": {
            "type": "object",
            "properties": {
                "token": {"type": "string", "description": "JWT token string"},
            },
            "required": ["token"],
        },
    },
    {
        "name": "jwt_tool_tamper",
        "description": "Tamper with JWT tokens - algorithm confusion, key injection, etc.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "token": {"type": "string", "description": "JWT token string"},
                "exploit": {
                    "type": "string",
                    "description": "Exploit: alg-none, kid-inject, jwks-spoof",
                },
                "sign_key": {
                    "type": "string",
                    "description": "Key to sign forged token",
                },
            },
            "required": ["token", "exploit"],
        },
    },
    {
        "name": "nosqlmap_scan",
        "description": "NoSQL injection detection for MongoDB, CouchDB, etc.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target URL"},
                "data": {"type": "string", "description": "POST data"},
                "dbtype": {
                    "type": "string",
                    "description": "Database type: MongoDB, CouchDB",
                },
            },
            "required": ["url"],
        },
    },
    {
        "name": "ssrfmap_scan",
        "description": "Server-Side Request Forgery detection and exploitation",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Vulnerable URL with FUZZ marker",
                },
                "data": {"type": "string", "description": "POST data with FUZZ marker"},
                "modules": {
                    "type": "string",
                    "description": "SSRF modules to use (e.g. readfiles, portscan)",
                },
            },
            "required": ["url"],
        },
    },
    {
        "name": "crlfuzz_scan",
        "description": "CRLF injection vulnerability scanning",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target URL"},
                "concurrent": {
                    "type": "integer",
                    "description": "Number of concurrent requests",
                },
            },
            "required": ["url"],
        },
    },
]


# ---------------------------------------------------------------------------
# Tool dispatch
# ---------------------------------------------------------------------------


async def dispatch_tool(name: str, args: Dict) -> str:
    if name == "xsstrike_scan":
        cmd = [sys.executable, _find_tool("xsstrike"), "-u", args["url"]]
        if args.get("data"):
            cmd.extend(["-d", args["data"]])
        if args.get("headers"):
            cmd.extend(["--headers", args["headers"]])
        if args.get("blind"):
            cmd.append("--blind")
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    elif name == "xsstrike_crawl":
        cmd = [sys.executable, _find_tool("xsstrike"), "-u", args["url"], "--crawl"]
        if args.get("level"):
            cmd.extend(["-l", str(args["level"])])
        return json.dumps(_run_tool(cmd, timeout=600), indent=2)

    elif name == "wfuzz_fuzz":
        cmd = [_find_tool("wfuzz"), "-w", args["wordlist"], args["url"]]
        if args.get("method"):
            cmd = [
                _find_tool("wfuzz"),
                "-X",
                args["method"],
                "-w",
                args["wordlist"],
                args["url"],
            ]
        if args.get("data"):
            cmd.extend(["-d", args["data"]])
        if args.get("header"):
            cmd.extend(["-H", args["header"]])
        if args.get("hide_code"):
            cmd.extend(["--hc", args["hide_code"]])
        if args.get("hide_chars"):
            cmd.extend(["--hh", args["hide_chars"]])
        return json.dumps(_run_tool(cmd, timeout=600), indent=2)

    elif name == "wfuzz_payloads":
        t = args.get("type", "payloads")
        cmd = [_find_tool("wfuzz"), f"--list-{t}"]
        return json.dumps(_run_tool(cmd, timeout=15), indent=2)

    elif name == "arjun_discover":
        cmd = [_find_tool("arjun"), "-u", args["url"]]
        if args.get("method"):
            cmd.extend(["-m", args["method"]])
        if args.get("wordlist"):
            cmd.extend(["-w", args["wordlist"]])
        if args.get("threads"):
            cmd.extend(["-t", str(args["threads"])])
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    elif name == "gospider_crawl":
        cmd = [_find_tool("gospider"), "-s", args["url"]]
        if args.get("depth"):
            cmd.extend(["-d", str(args["depth"])])
        if args.get("concurrent"):
            cmd.extend(["-c", str(args["concurrent"])])
        if args.get("include_subs"):
            cmd.append("--subs")
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    elif name == "paramspider_mine":
        cmd = [_find_tool("paramspider"), "-d", args["domain"]]
        if args.get("exclude"):
            cmd.extend(["--exclude", args["exclude"]])
        if args.get("level"):
            cmd.extend(["--level", args["level"]])
        return json.dumps(_run_tool(cmd, timeout=120), indent=2)

    elif name == "commix_inject":
        cmd = [sys.executable, _find_tool("commix"), "--url", args["url"], "--batch"]
        if args.get("data"):
            cmd.extend(["--data", args["data"]])
        if args.get("cookie"):
            cmd.extend(["--cookie", args["cookie"]])
        if args.get("level"):
            cmd.extend(["--level", str(args["level"])])
        if args.get("technique"):
            cmd.extend(["--technique", args["technique"]])
        return json.dumps(_run_tool(cmd, timeout=600), indent=2)

    elif name == "dalfox_scan":
        cmd = [_find_tool("dalfox"), "url", args["url"]]
        if args.get("method"):
            cmd.extend(["-X", args["method"]])
        if args.get("blind"):
            cmd.extend(["--blind", args["blind"]])
        if args.get("custom_payload"):
            cmd.extend(["--custom-payload", args["custom_payload"]])
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    elif name == "jwt_tool_analyze":
        cmd = [sys.executable, _find_tool("jwt_tool"), args["token"]]
        return json.dumps(_run_tool(cmd, timeout=30), indent=2)

    elif name == "jwt_tool_tamper":
        cmd = [
            sys.executable,
            _find_tool("jwt_tool"),
            args["token"],
            "-X",
            args["exploit"],
        ]
        if args.get("sign_key"):
            cmd.extend(["-pk", args["sign_key"]])
        return json.dumps(_run_tool(cmd, timeout=30), indent=2)

    elif name == "nosqlmap_scan":
        cmd = [sys.executable, _find_tool("nosqlmap"), "-u", args["url"]]
        if args.get("data"):
            cmd.extend(["-d", args["data"]])
        if args.get("dbtype"):
            cmd.extend(["--db", args["dbtype"]])
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    elif name == "ssrfmap_scan":
        cmd = [sys.executable, _find_tool("ssrfmap"), "-r", args["url"]]
        if args.get("data"):
            cmd.extend(["-p", args["data"]])
        if args.get("modules"):
            cmd.extend(["-m", args["modules"]])
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    elif name == "crlfuzz_scan":
        cmd = [_find_tool("crlfuzz"), "-u", args["url"]]
        if args.get("concurrent"):
            cmd.extend(["-c", str(args["concurrent"])])
        return json.dumps(_run_tool(cmd, timeout=120), indent=2)

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
