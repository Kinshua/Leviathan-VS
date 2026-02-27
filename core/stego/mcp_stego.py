#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP Steganography Server v1.0.0

    Steganography detection, embedding & extraction.
    Integrates: steghide, stegosuite, zsteg, openstego, outguess,
                stegsolve, snow, stegseek, stegcracker, exiftool.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (14):
        - steghide_embed: Embed secret data into image/audio (steghide)
        - steghide_extract: Extract hidden data from stego file
        - steghide_info: Get info about stego file capacity/embedded data
        - zsteg_detect: Detect LSB steganography in PNG/BMP files
        - zsteg_extract: Extract specific payload from PNG/BMP
        - openstego_embed: Embed data using OpenStego (supports watermarking)
        - openstego_extract: Extract hidden data with OpenStego
        - outguess_embed: Embed data using OutGuess (JPEG steganography)
        - outguess_extract: Extract data embedded with OutGuess
        - snow_embed: Whitespace steganography - hide data in text files
        - snow_extract: Extract whitespace-hidden data from text
        - stegseek_crack: Crack steghide passphrases using wordlists (fast)
        - stegcracker_crack: Brute-force steghide passwords
        - exiftool_stego: Analyze/manipulate metadata for hidden data

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
logger = logging.getLogger("leviathan-stego-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-stego-server"


def _find_tool(name: str) -> str:
    p = shutil.which(name)
    return p if p else name


def _run_tool(cmd: List[str], timeout: int = 300) -> Dict:
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace",
        )
        return {
            "success": proc.returncode == 0,
            "stdout": proc.stdout.strip()[:50000],
            "stderr": proc.stderr.strip()[:5000],
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"Timeout after {timeout}s"}
    except FileNotFoundError:
        return {"success": False, "error": f"Tool not found: {cmd[0]}. Install it first."}
    except Exception as e:
        return {"success": False, "error": str(e)}


TOOLS = [
    {
        "name": "steghide_embed",
        "description": "Embed secret data into JPEG/BMP/WAV/AU cover file (steghide)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cover_file": {"type": "string", "description": "Cover file (JPEG/BMP/WAV/AU)"},
                "embed_file": {"type": "string", "description": "File to embed/hide"},
                "output_file": {"type": "string", "description": "Output stego file"},
                "passphrase": {"type": "string", "description": "Passphrase for encryption"},
                "compression": {"type": "integer", "description": "Compression level 1-9"},
                "force": {"type": "boolean", "description": "Overwrite existing output"},
            },
            "required": ["cover_file", "embed_file"],
        },
    },
    {
        "name": "steghide_extract",
        "description": "Extract hidden data from steghide stego file",
        "inputSchema": {
            "type": "object",
            "properties": {
                "stego_file": {"type": "string", "description": "Stego file to extract from"},
                "passphrase": {"type": "string", "description": "Passphrase (empty for no password)"},
                "output_file": {"type": "string", "description": "Output extracted file"},
                "force": {"type": "boolean", "description": "Overwrite existing output"},
            },
            "required": ["stego_file"],
        },
    },
    {
        "name": "steghide_info",
        "description": "Show info about stego file capacity and embedded data",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "File to analyze"},
                "passphrase": {"type": "string", "description": "Passphrase to check"},
            },
            "required": ["file"],
        },
    },
    {
        "name": "zsteg_detect",
        "description": "Detect LSB steganography & hidden data in PNG/BMP files",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "PNG or BMP image file"},
                "all": {"type": "boolean", "description": "Try all known methods"},
                "bits": {"type": "string", "description": "Bits to analyze (e.g. 1,2,3)"},
                "order": {"type": "string", "description": "Bit order: auto, msb, lsb"},
            },
            "required": ["file"],
        },
    },
    {
        "name": "zsteg_extract",
        "description": "Extract specific payload from PNG/BMP using zsteg",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "PNG or BMP image file"},
                "channel": {"type": "string", "description": "Channel spec (e.g. b1,lsb,xy or r2,msb,yx)"},
                "output_file": {"type": "string", "description": "Output file for extracted data"},
            },
            "required": ["file", "channel"],
        },
    },
    {
        "name": "openstego_embed",
        "description": "Embed data using OpenStego (supports watermarking & data hiding)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "message_file": {"type": "string", "description": "File to hide"},
                "cover_file": {"type": "string", "description": "Cover image file"},
                "output_file": {"type": "string", "description": "Output stego image"},
                "password": {"type": "string", "description": "Encryption password"},
                "algorithm": {"type": "string", "description": "Stego algorithm to use"},
            },
            "required": ["message_file", "cover_file", "output_file"],
        },
    },
    {
        "name": "openstego_extract",
        "description": "Extract hidden data from OpenStego stego image",
        "inputSchema": {
            "type": "object",
            "properties": {
                "stego_file": {"type": "string", "description": "Stego image file"},
                "output_dir": {"type": "string", "description": "Output directory for extracted data"},
                "password": {"type": "string", "description": "Decryption password"},
            },
            "required": ["stego_file", "output_dir"],
        },
    },
    {
        "name": "outguess_embed",
        "description": "Hide data in JPEG images using OutGuess steganography",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data_file": {"type": "string", "description": "File containing data to hide"},
                "cover_file": {"type": "string", "description": "Cover JPEG image"},
                "output_file": {"type": "string", "description": "Output stego JPEG"},
                "key": {"type": "string", "description": "Encryption key"},
            },
            "required": ["data_file", "cover_file", "output_file"],
        },
    },
    {
        "name": "outguess_extract",
        "description": "Extract data hidden with OutGuess from JPEG",
        "inputSchema": {
            "type": "object",
            "properties": {
                "stego_file": {"type": "string", "description": "Stego JPEG file"},
                "output_file": {"type": "string", "description": "Output file for extracted data"},
                "key": {"type": "string", "description": "Decryption key"},
            },
            "required": ["stego_file", "output_file"],
        },
    },
    {
        "name": "snow_embed",
        "description": "Whitespace steganography - hide data in trailing spaces/tabs of text",
        "inputSchema": {
            "type": "object",
            "properties": {
                "message": {"type": "string", "description": "Message to hide"},
                "cover_file": {"type": "string", "description": "Cover text file"},
                "output_file": {"type": "string", "description": "Output stego text file"},
                "password": {"type": "string", "description": "Encryption password"},
            },
            "required": ["message", "cover_file", "output_file"],
        },
    },
    {
        "name": "snow_extract",
        "description": "Extract whitespace-hidden data from text file (SNOW)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "stego_file": {"type": "string", "description": "Stego text file"},
                "password": {"type": "string", "description": "Decryption password"},
            },
            "required": ["stego_file"],
        },
    },
    {
        "name": "stegseek_crack",
        "description": "Fast steghide passphrase cracker using wordlists (stegseek)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "stego_file": {"type": "string", "description": "Steghide stego file to crack"},
                "wordlist": {"type": "string", "description": "Wordlist path (default: rockyou.txt)"},
                "output_file": {"type": "string", "description": "Output extracted file"},
                "threads": {"type": "integer", "description": "Number of threads"},
            },
            "required": ["stego_file"],
        },
    },
    {
        "name": "stegcracker_crack",
        "description": "Brute-force steghide passwords with wordlist (stegcracker)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "stego_file": {"type": "string", "description": "Steghide stego file"},
                "wordlist": {"type": "string", "description": "Wordlist path"},
                "threads": {"type": "integer", "description": "Number of threads"},
                "output_file": {"type": "string", "description": "Output file"},
            },
            "required": ["stego_file"],
        },
    },
    {
        "name": "exiftool_stego",
        "description": "Analyze/manipulate file metadata for hidden data (exiftool)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "File to analyze"},
                "write_tag": {"type": "string", "description": "Tag to write (e.g. -Comment=hidden_data)"},
                "extract_all": {"type": "boolean", "description": "Extract all metadata"},
                "verbose": {"type": "boolean", "description": "Verbose hex dump output"},
            },
            "required": ["file"],
        },
    },
]


async def dispatch_tool(name: str, args: Dict) -> str:
    if name == "steghide_embed":
        cmd = [_find_tool("steghide"), "embed", "-cf", args["cover_file"], "-ef", args["embed_file"]]
        if args.get("output_file"):
            cmd.extend(["-sf", args["output_file"]])
        if args.get("passphrase"):
            cmd.extend(["-p", args["passphrase"]])
        else:
            cmd.extend(["-p", ""])
        if args.get("compression"):
            cmd.extend(["-z", str(args["compression"])])
        if args.get("force"):
            cmd.append("-f")
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "steghide_extract":
        cmd = [_find_tool("steghide"), "extract", "-sf", args["stego_file"]]
        if args.get("passphrase") is not None:
            cmd.extend(["-p", args.get("passphrase", "")])
        else:
            cmd.extend(["-p", ""])
        if args.get("output_file"):
            cmd.extend(["-xf", args["output_file"]])
        if args.get("force"):
            cmd.append("-f")
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "steghide_info":
        cmd = [_find_tool("steghide"), "info", args["file"]]
        if args.get("passphrase"):
            cmd.extend(["-p", args["passphrase"]])
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "zsteg_detect":
        cmd = [_find_tool("zsteg"), args["file"]]
        if args.get("all"):
            cmd.append("-a")
        if args.get("bits"):
            cmd.extend(["-b", args["bits"]])
        if args.get("order"):
            cmd.extend(["-o", args["order"]])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "zsteg_extract":
        cmd = [_find_tool("zsteg"), args["file"], "-E", args["channel"]]
        if args.get("output_file"):
            # Redirect handled by capturing stdout
            pass
        r = _run_tool(cmd, timeout=120)
        if args.get("output_file") and r.get("success"):
            with open(args["output_file"], "w", encoding="utf-8") as f:
                f.write(r.get("stdout", ""))
            r["saved_to"] = args["output_file"]
        return json.dumps(r, indent=2)

    elif name == "openstego_embed":
        cmd = [_find_tool("openstego"), "embed", "-mf", args["message_file"],
               "-cf", args["cover_file"], "-sf", args["output_file"]]
        if args.get("password"):
            cmd.extend(["-p", args["password"]])
        if args.get("algorithm"):
            cmd.extend(["-a", args["algorithm"]])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "openstego_extract":
        cmd = [_find_tool("openstego"), "extract", "-sf", args["stego_file"],
               "-xd", args["output_dir"]]
        if args.get("password"):
            cmd.extend(["-p", args["password"]])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "outguess_embed":
        cmd = [_find_tool("outguess")]
        if args.get("key"):
            cmd.extend(["-k", args["key"]])
        cmd.extend(["-d", args["data_file"], args["cover_file"], args["output_file"]])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "outguess_extract":
        cmd = [_find_tool("outguess"), "-r"]
        if args.get("key"):
            cmd.extend(["-k", args["key"]])
        cmd.extend([args["stego_file"], args["output_file"]])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "snow_embed":
        cmd = [_find_tool("snow"), "-m", args["message"]]
        if args.get("password"):
            cmd.extend(["-p", args["password"]])
        cmd.extend([args["cover_file"], args["output_file"]])
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "snow_extract":
        cmd = [_find_tool("snow")]
        if args.get("password"):
            cmd.extend(["-p", args["password"]])
        cmd.append(args["stego_file"])
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "stegseek_crack":
        cmd = [_find_tool("stegseek"), args["stego_file"]]
        if args.get("wordlist"):
            cmd.append(args["wordlist"])
        if args.get("output_file"):
            cmd.extend(["-xf", args["output_file"]])
        if args.get("threads"):
            cmd.extend(["-t", str(args["threads"])])
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "stegcracker_crack":
        cmd = [_find_tool("stegcracker"), args["stego_file"]]
        if args.get("wordlist"):
            cmd.append(args["wordlist"])
        if args.get("threads"):
            cmd.extend(["-t", str(args["threads"])])
        if args.get("output_file"):
            cmd.extend(["-o", args["output_file"]])
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "exiftool_stego":
        cmd = [_find_tool("exiftool")]
        if args.get("extract_all"):
            cmd.append("-a")
        if args.get("verbose"):
            cmd.append("-v2")
        if args.get("write_tag"):
            cmd.append(args["write_tag"])
        cmd.append(args["file"])
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
