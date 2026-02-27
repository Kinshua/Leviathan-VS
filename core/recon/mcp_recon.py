#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP Reconnaissance Server v1.0.0

    Advanced reconnaissance and asset discovery MCP server.
    Integrates: amass, gobuster, masscan, whatweb, dnsrecon, wafw00f, fierce.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (14):
        - amass_enum: Attack surface mapping & subdomain enumeration
        - amass_intel: OSINT and org intelligence gathering
        - gobuster_dir: Directory/file brute-forcing on web servers
        - gobuster_dns: DNS subdomain brute-forcing
        - gobuster_vhost: Virtual host discovery
        - masscan_scan: High-speed port scanning (10M packets/sec)
        - masscan_banner: Banner grabbing on discovered ports
        - whatweb_scan: Web technology fingerprinting
        - dnsrecon_scan: DNS enumeration and zone transfer testing
        - dnsrecon_brute: DNS brute-force subdomain discovery
        - wafw00f_detect: Web Application Firewall detection
        - fierce_scan: DNS reconnaissance & zone transfer
        - theHarvester_scan: Email, subdomain & IP harvesting
        - assetfinder_enum: Find related domains & subdomains

    Author: ThiagoFrag / LEVIATHAN VS
    Version: 1.0.0
    Inspired by: FuzzingLabs/mcp-security-hub, secops-mcp
================================================================================
"""

import asyncio
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger("leviathan-recon-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-recon-server"


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
        "name": "amass_enum",
        "description": "Subdomain enumeration and attack surface mapping using OWASP Amass",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target domain"},
                "passive": {
                    "type": "boolean",
                    "description": "Passive mode only (no DNS brute-force)",
                },
                "timeout": {"type": "integer", "description": "Timeout in minutes"},
                "extra_args": {
                    "type": "string",
                    "description": "Additional amass arguments",
                },
            },
            "required": ["domain"],
        },
    },
    {
        "name": "amass_intel",
        "description": "OSINT intelligence gathering - find associated domains, ASNs, netblocks",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "Target domain or org name",
                },
                "whois": {
                    "type": "boolean",
                    "description": "Use WHOIS for reverse lookups",
                },
            },
            "required": ["domain"],
        },
    },
    {
        "name": "gobuster_dir",
        "description": "Directory and file brute-forcing on web servers",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target URL"},
                "wordlist": {
                    "type": "string",
                    "description": "Path to wordlist (default: common.txt)",
                },
                "extensions": {
                    "type": "string",
                    "description": "File extensions to search (e.g. php,html,js)",
                },
                "threads": {"type": "integer", "description": "Number of threads"},
                "status_codes": {
                    "type": "string",
                    "description": "Status codes to match (e.g. 200,301,302)",
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout per request in seconds",
                },
                "extra_args": {
                    "type": "string",
                    "description": "Additional gobuster arguments",
                },
            },
            "required": ["url"],
        },
    },
    {
        "name": "gobuster_dns",
        "description": "DNS subdomain brute-forcing",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target domain"},
                "wordlist": {"type": "string", "description": "Path to wordlist"},
                "threads": {"type": "integer", "description": "Number of threads"},
                "show_ip": {"type": "boolean", "description": "Show IP addresses"},
            },
            "required": ["domain"],
        },
    },
    {
        "name": "gobuster_vhost",
        "description": "Virtual host discovery via brute-force",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target URL"},
                "wordlist": {"type": "string", "description": "Path to wordlist"},
                "threads": {"type": "integer", "description": "Number of threads"},
            },
            "required": ["url"],
        },
    },
    {
        "name": "masscan_scan",
        "description": "High-speed port scanning (up to 10M packets/sec)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "Target IP/range (e.g. 192.168.1.0/24)",
                },
                "ports": {
                    "type": "string",
                    "description": "Port range (e.g. 0-65535 or 80,443,8080)",
                },
                "rate": {
                    "type": "integer",
                    "description": "Packets per second (default: 1000)",
                },
                "timeout": {"type": "integer"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "masscan_banner",
        "description": "Banner grabbing on discovered ports",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target IP/range"},
                "ports": {"type": "string", "description": "Ports to banner grab"},
            },
            "required": ["target", "ports"],
        },
    },
    {
        "name": "whatweb_scan",
        "description": "Web technology fingerprinting - identify CMS, frameworks, servers, plugins",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target URL or hostname"},
                "aggression": {
                    "type": "integer",
                    "description": "Aggression level 1-4 (1=stealthy, 4=heavy)",
                },
                "verbose": {"type": "boolean"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "dnsrecon_scan",
        "description": "DNS enumeration - zone transfers, records, reverse lookups",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target domain"},
                "scan_type": {
                    "type": "string",
                    "description": "Scan type: std, brt, rvl, axfr, zonewalk",
                },
                "nameserver": {"type": "string", "description": "Custom DNS server"},
            },
            "required": ["domain"],
        },
    },
    {
        "name": "dnsrecon_brute",
        "description": "DNS brute-force subdomain discovery",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target domain"},
                "wordlist": {"type": "string", "description": "Path to wordlist"},
                "threads": {"type": "integer"},
            },
            "required": ["domain"],
        },
    },
    {
        "name": "wafw00f_detect",
        "description": "Detect Web Application Firewalls (WAF) protecting a website",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target URL"},
                "findall": {
                    "type": "boolean",
                    "description": "Find ALL WAFs (not just first)",
                },
            },
            "required": ["url"],
        },
    },
    {
        "name": "fierce_scan",
        "description": "DNS reconnaissance tool - locate non-contiguous IP space and hostnames",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target domain"},
                "dns_servers": {
                    "type": "string",
                    "description": "Custom DNS servers (comma-separated)",
                },
                "subdomain_file": {
                    "type": "string",
                    "description": "Custom subdomain wordlist",
                },
            },
            "required": ["domain"],
        },
    },
    {
        "name": "theHarvester_scan",
        "description": "Gather emails, subdomains, IPs, URLs from public sources (Google, Bing, Shodan, etc.)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target domain"},
                "source": {
                    "type": "string",
                    "description": "Data source (google, bing, shodan, linkedin, etc.)",
                },
                "limit": {"type": "integer", "description": "Limit results count"},
            },
            "required": ["domain"],
        },
    },
    {
        "name": "assetfinder_enum",
        "description": "Find related domains and subdomains using various sources",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target domain"},
                "subs_only": {"type": "boolean", "description": "Only show subdomains"},
            },
            "required": ["domain"],
        },
    },
]


# ---------------------------------------------------------------------------
# Tool dispatch
# ---------------------------------------------------------------------------


async def dispatch_tool(name: str, args: Dict) -> str:
    if name == "amass_enum":
        cmd = [_find_tool("amass"), "enum", "-d", args["domain"]]
        if args.get("passive"):
            cmd.append("-passive")
        if args.get("timeout"):
            cmd.extend(["-timeout", str(args["timeout"])])
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=args.get("timeout", 10) * 60)
        return json.dumps(r, indent=2)

    elif name == "amass_intel":
        cmd = [_find_tool("amass"), "intel", "-d", args["domain"]]
        if args.get("whois"):
            cmd.append("-whois")
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "gobuster_dir":
        wl = args.get("wordlist", "/usr/share/wordlists/dirb/common.txt")
        cmd = [_find_tool("gobuster"), "dir", "-u", args["url"], "-w", wl, "--no-color"]
        if args.get("extensions"):
            cmd.extend(["-x", args["extensions"]])
        if args.get("threads"):
            cmd.extend(["-t", str(args["threads"])])
        if args.get("status_codes"):
            cmd.extend(["-s", args["status_codes"]])
        if args.get("timeout"):
            cmd.extend(["--timeout", f"{args['timeout']}s"])
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=args.get("timeout", 300))
        return json.dumps(r, indent=2)

    elif name == "gobuster_dns":
        wl = args.get(
            "wordlist", "/usr/share/wordlists/dns/subdomains-top1million-5000.txt"
        )
        cmd = [_find_tool("gobuster"), "dns", "-d", args["domain"], "-w", wl]
        if args.get("threads"):
            cmd.extend(["-t", str(args["threads"])])
        if args.get("show_ip"):
            cmd.append("-i")
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "gobuster_vhost":
        wl = args.get(
            "wordlist", "/usr/share/wordlists/dns/subdomains-top1million-5000.txt"
        )
        cmd = [_find_tool("gobuster"), "vhost", "-u", args["url"], "-w", wl]
        if args.get("threads"):
            cmd.extend(["-t", str(args["threads"])])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "masscan_scan":
        ports = args.get("ports", "1-65535")
        rate = args.get("rate", 1000)
        cmd = [
            _find_tool("masscan"),
            args["target"],
            "-p",
            ports,
            "--rate",
            str(rate),
            "--open",
        ]
        r = _run_tool(cmd, timeout=args.get("timeout", 600))
        return json.dumps(r, indent=2)

    elif name == "masscan_banner":
        cmd = [
            _find_tool("masscan"),
            args["target"],
            "-p",
            args["ports"],
            "--banners",
            "--rate",
            "500",
        ]
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "whatweb_scan":
        cmd = [_find_tool("whatweb"), args["target"], "--color=never"]
        if args.get("aggression"):
            cmd.extend(["-a", str(args["aggression"])])
        if args.get("verbose"):
            cmd.append("-v")
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "dnsrecon_scan":
        cmd = [_find_tool("dnsrecon"), "-d", args["domain"]]
        if args.get("scan_type"):
            cmd.extend(["-t", args["scan_type"]])
        if args.get("nameserver"):
            cmd.extend(["-n", args["nameserver"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "dnsrecon_brute":
        cmd = [_find_tool("dnsrecon"), "-d", args["domain"], "-t", "brt"]
        if args.get("wordlist"):
            cmd.extend(["-D", args["wordlist"]])
        if args.get("threads"):
            cmd.extend(["--threads", str(args["threads"])])
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "wafw00f_detect":
        cmd = [_find_tool("wafw00f"), args["url"]]
        if args.get("findall"):
            cmd.append("-a")
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "fierce_scan":
        cmd = [_find_tool("fierce"), "--domain", args["domain"]]
        if args.get("dns_servers"):
            cmd.extend(["--dns-servers", args["dns_servers"]])
        if args.get("subdomain_file"):
            cmd.extend(["--subdomain-file", args["subdomain_file"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "theHarvester_scan":
        src = args.get("source", "google")
        limit = args.get("limit", 500)
        cmd = [
            _find_tool("theHarvester"),
            "-d",
            args["domain"],
            "-b",
            src,
            "-l",
            str(limit),
        ]
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "assetfinder_enum":
        cmd = [_find_tool("assetfinder")]
        if args.get("subs_only"):
            cmd.append("--subs-only")
        cmd.append(args["domain"])
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
