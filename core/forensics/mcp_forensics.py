#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP Forensics Server v1.0.0

    Digital Forensics & Incident Response MCP server.
    Integrates: volatility3, yara, binwalk, capa, foremost, bulk_extractor,
                exiftool, strings analysis, hash computation.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (14):
        - volatility_pslist: List running processes from memory dump
        - volatility_netscan: Network connections from memory dump
        - volatility_cmdline: Command line args from memory dump
        - volatility_filescan: Scan for file objects in memory dump
        - yara_scan: Scan files/dirs with YARA rules
        - yara_compile: Compile YARA rules for validation
        - binwalk_scan: Scan firmware/binary for embedded files
        - binwalk_extract: Extract embedded files from binary
        - capa_analyze: Detect capabilities in PE/ELF executables
        - foremost_carve: Carve files from disk image or raw data
        - bulk_extractor_scan: Extract emails, URLs, credit cards, etc.
        - exiftool_read: Read metadata from any file
        - exiftool_strip: Strip metadata from files
        - strings_extract: Extract readable strings from binary files

    Author: ThiagoFrag / LEVIATHAN VS
    Version: 1.0.0
    Inspired by: FuzzingLabs/mcp-security-hub forensic tooling
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
logger = logging.getLogger("leviathan-forensics-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-forensics-server"


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
        "name": "volatility_pslist",
        "description": "List running processes from a memory dump using Volatility3",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dump_file": {
                    "type": "string",
                    "description": "Path to memory dump file",
                },
                "pid": {"type": "integer", "description": "Filter by specific PID"},
            },
            "required": ["dump_file"],
        },
    },
    {
        "name": "volatility_netscan",
        "description": "List network connections and sockets from memory dump",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dump_file": {
                    "type": "string",
                    "description": "Path to memory dump file",
                },
            },
            "required": ["dump_file"],
        },
    },
    {
        "name": "volatility_cmdline",
        "description": "Show command-line arguments of processes from memory dump",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dump_file": {
                    "type": "string",
                    "description": "Path to memory dump file",
                },
                "pid": {"type": "integer", "description": "Filter by specific PID"},
            },
            "required": ["dump_file"],
        },
    },
    {
        "name": "volatility_filescan",
        "description": "Scan for file objects in memory dump (great for finding hidden/deleted files)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dump_file": {
                    "type": "string",
                    "description": "Path to memory dump file",
                },
            },
            "required": ["dump_file"],
        },
    },
    {
        "name": "yara_scan",
        "description": "Scan files or directories with YARA rules for malware detection",
        "inputSchema": {
            "type": "object",
            "properties": {
                "rules": {"type": "string", "description": "Path to YARA rules file"},
                "target": {
                    "type": "string",
                    "description": "File or directory to scan",
                },
                "recursive": {
                    "type": "boolean",
                    "description": "Scan directories recursively",
                },
            },
            "required": ["rules", "target"],
        },
    },
    {
        "name": "yara_compile",
        "description": "Compile and validate YARA rules without scanning",
        "inputSchema": {
            "type": "object",
            "properties": {
                "rules": {"type": "string", "description": "Path to YARA rules file"},
            },
            "required": ["rules"],
        },
    },
    {
        "name": "binwalk_scan",
        "description": "Scan firmware or binary for embedded file signatures",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "description": "Path to binary/firmware file",
                },
                "entropy": {"type": "boolean", "description": "Calculate entropy"},
            },
            "required": ["file"],
        },
    },
    {
        "name": "binwalk_extract",
        "description": "Extract embedded files from firmware/binary",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "description": "Path to binary/firmware file",
                },
                "output_dir": {
                    "type": "string",
                    "description": "Output directory for extracted files",
                },
            },
            "required": ["file"],
        },
    },
    {
        "name": "capa_analyze",
        "description": "Detect capabilities in PE/ELF executables (anti-debug, crypto, network, etc.)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "Path to executable"},
                "format": {
                    "type": "string",
                    "description": "Output format: default, json, vverbose",
                },
                "rules": {
                    "type": "string",
                    "description": "Path to custom capa rules directory",
                },
            },
            "required": ["file"],
        },
    },
    {
        "name": "foremost_carve",
        "description": "Carve files from disk image, memory dump, or raw data",
        "inputSchema": {
            "type": "object",
            "properties": {
                "input_file": {
                    "type": "string",
                    "description": "Path to input file (disk image, dump, etc.)",
                },
                "output_dir": {
                    "type": "string",
                    "description": "Output directory for carved files",
                },
                "types": {
                    "type": "string",
                    "description": "File types to carve (e.g. 'jpg,png,pdf,doc')",
                },
            },
            "required": ["input_file"],
        },
    },
    {
        "name": "bulk_extractor_scan",
        "description": "Extract emails, URLs, credit card numbers, phone numbers from disk images",
        "inputSchema": {
            "type": "object",
            "properties": {
                "input_file": {"type": "string", "description": "Input file to scan"},
                "output_dir": {
                    "type": "string",
                    "description": "Output directory for features",
                },
                "scanners": {
                    "type": "string",
                    "description": "Specific scanners to enable (comma-separated)",
                },
            },
            "required": ["input_file", "output_dir"],
        },
    },
    {
        "name": "exiftool_read",
        "description": "Read metadata from any file (images, PDFs, documents, videos)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "Path to file"},
                "json_output": {"type": "boolean", "description": "Output as JSON"},
            },
            "required": ["file"],
        },
    },
    {
        "name": "exiftool_strip",
        "description": "Strip all metadata from files (privacy/OPSEC)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "Path to file"},
            },
            "required": ["file"],
        },
    },
    {
        "name": "strings_extract",
        "description": "Extract readable ASCII/Unicode strings from binary files",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "Path to binary file"},
                "min_length": {
                    "type": "integer",
                    "description": "Minimum string length (default: 4)",
                },
                "encoding": {
                    "type": "string",
                    "description": "Encoding: s (7-bit), S (8-bit), l (16-bit LE), b (16-bit BE)",
                },
            },
            "required": ["file"],
        },
    },
]


# ---------------------------------------------------------------------------
# Tool dispatch
# ---------------------------------------------------------------------------


async def dispatch_tool(name: str, args: Dict) -> str:
    vol = _find_tool("vol")
    vol3 = _find_tool("vol3") if vol == "vol" else vol

    if name == "volatility_pslist":
        cmd = [vol3, "-f", args["dump_file"], "windows.pslist"]
        if args.get("pid"):
            cmd.extend(["--pid", str(args["pid"])])
        return json.dumps(_run_tool(cmd, timeout=120), indent=2)

    elif name == "volatility_netscan":
        cmd = [vol3, "-f", args["dump_file"], "windows.netscan"]
        return json.dumps(_run_tool(cmd, timeout=120), indent=2)

    elif name == "volatility_cmdline":
        cmd = [vol3, "-f", args["dump_file"], "windows.cmdline"]
        if args.get("pid"):
            cmd.extend(["--pid", str(args["pid"])])
        return json.dumps(_run_tool(cmd, timeout=120), indent=2)

    elif name == "volatility_filescan":
        cmd = [vol3, "-f", args["dump_file"], "windows.filescan"]
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    elif name == "yara_scan":
        cmd = [_find_tool("yara")]
        if args.get("recursive"):
            cmd.append("-r")
        cmd.extend([args["rules"], args["target"]])
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    elif name == "yara_compile":
        cmd = [_find_tool("yarac"), args["rules"], os.devnull]
        return json.dumps(_run_tool(cmd, timeout=30), indent=2)

    elif name == "binwalk_scan":
        cmd = [_find_tool("binwalk"), args["file"]]
        if args.get("entropy"):
            cmd.append("-E")
        return json.dumps(_run_tool(cmd, timeout=120), indent=2)

    elif name == "binwalk_extract":
        cmd = [_find_tool("binwalk"), "-e", args["file"]]
        if args.get("output_dir"):
            cmd.extend(["-C", args["output_dir"]])
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    elif name == "capa_analyze":
        cmd = [_find_tool("capa"), args["file"]]
        fmt = args.get("format", "default")
        if fmt == "json":
            cmd.append("-j")
        elif fmt == "vverbose":
            cmd.append("-vv")
        if args.get("rules"):
            cmd.extend(["-r", args["rules"]])
        return json.dumps(_run_tool(cmd, timeout=300), indent=2)

    elif name == "foremost_carve":
        cmd = [_find_tool("foremost"), "-i", args["input_file"]]
        if args.get("output_dir"):
            cmd.extend(["-o", args["output_dir"]])
        if args.get("types"):
            cmd.extend(["-t", args["types"]])
        return json.dumps(_run_tool(cmd, timeout=600), indent=2)

    elif name == "bulk_extractor_scan":
        cmd = [
            _find_tool("bulk_extractor"),
            "-o",
            args["output_dir"],
            args["input_file"],
        ]
        if args.get("scanners"):
            for s in args["scanners"].split(","):
                cmd.extend(["-e", s.strip()])
        return json.dumps(_run_tool(cmd, timeout=600), indent=2)

    elif name == "exiftool_read":
        cmd = [_find_tool("exiftool")]
        if args.get("json_output"):
            cmd.append("-json")
        cmd.append(args["file"])
        return json.dumps(_run_tool(cmd, timeout=30), indent=2)

    elif name == "exiftool_strip":
        cmd = [_find_tool("exiftool"), "-all=", args["file"]]
        return json.dumps(_run_tool(cmd, timeout=30), indent=2)

    elif name == "strings_extract":
        cmd = [_find_tool("strings")]
        ml = args.get("min_length", 4)
        cmd.extend(["-n", str(ml)])
        if args.get("encoding"):
            cmd.extend(["-e", args["encoding"]])
        cmd.append(args["file"])
        return json.dumps(_run_tool(cmd, timeout=60), indent=2)

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
