#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP Wordlist & Password Server v1.0.0

    Wordlist generation, password cracking, hash identification.
    Integrates: cewl, crunch, cupp, hash-identifier, ophcrack, patator,
                mentalist, kwprocessor, john, hashid, princeprocessor.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (16):
        - cewl_generate: Generate custom wordlist from website content
        - crunch_generate: Generate wordlists with pattern-based rules
        - cupp_generate: Common User Passwords Profiler (social profiling)
        - hash_identifier: Identify hash types from hash strings
        - hashid_identify: Advanced hash identification (600+ hash types)
        - ophcrack_crack: Rainbow table password cracking (Windows LM/NTLM)
        - patator_brute: Multi-purpose brute-forcer (SSH, FTP, HTTP, SQL, etc.)
        - mentalist_generate: GUI/CLI wordlist generator with rules & chains
        - kwprocessor_generate: Keyboard walk pattern generator
        - princeprocessor_generate: PRINCE algorithm wordlist processor
        - john_crack: John the Ripper password cracker
        - john_show: Show cracked passwords from John pot file
        - john_rules: Apply John wordlist rules
        - wordlistctl_fetch: Download and manage wordlists
        - username_anarchy: Generate username permutations
        - rsmangler_mangle: Mangle/permute words for password lists

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
logger = logging.getLogger("leviathan-wordlist-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-wordlist-server"


def _find_tool(name: str) -> str:
    p = shutil.which(name)
    return p if p else name


def _run_tool(cmd: List[str], timeout: int = 600) -> Dict:
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
        "name": "cewl_generate",
        "description": "Generate custom wordlist by spidering a website and extracting words",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target URL to spider"},
                "depth": {"type": "integer", "description": "Spider depth (default: 2)"},
                "min_length": {"type": "integer", "description": "Minimum word length (default: 3)"},
                "max_length": {"type": "integer", "description": "Maximum word length"},
                "with_numbers": {"type": "boolean", "description": "Include words with numbers"},
                "email": {"type": "boolean", "description": "Also extract email addresses"},
                "meta": {"type": "boolean", "description": "Include metadata words"},
                "output": {"type": "string", "description": "Output file"},
                "count": {"type": "boolean", "description": "Show word count next to words"},
                "lowercase": {"type": "boolean", "description": "Convert all to lowercase"},
                "extra_args": {"type": "string", "description": "Additional cewl arguments"},
            },
            "required": ["url"],
        },
    },
    {
        "name": "crunch_generate",
        "description": "Generate wordlists with specific patterns, charsets, and length ranges",
        "inputSchema": {
            "type": "object",
            "properties": {
                "min_length": {"type": "integer", "description": "Minimum word length"},
                "max_length": {"type": "integer", "description": "Maximum word length"},
                "charset": {"type": "string", "description": "Character set (e.g. abcdef0123456789, or mixalpha-numeric)"},
                "pattern": {"type": "string", "description": "Pattern: @ (lowercase), , (uppercase), % (numeric), ^ (special)"},
                "output": {"type": "string", "description": "Output file"},
                "start_string": {"type": "string", "description": "Start from this string"},
                "count": {"type": "integer", "description": "Maximum number of words"},
                "compress": {"type": "boolean", "description": "Compress output with gzip"},
            },
            "required": ["min_length", "max_length"],
        },
    },
    {
        "name": "cupp_generate",
        "description": "Common User Passwords Profiler - generate targeted wordlist from personal info",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interactive": {"type": "boolean", "description": "Interactive mode (prompts for info)"},
                "name": {"type": "string", "description": "Target's first name"},
                "surname": {"type": "string", "description": "Target's surname"},
                "nickname": {"type": "string", "description": "Target's nickname"},
                "birthdate": {"type": "string", "description": "Target's birthdate (DDMMYYYY)"},
                "partner_name": {"type": "string", "description": "Partner's name"},
                "partner_birthdate": {"type": "string", "description": "Partner's birthdate"},
                "pet_name": {"type": "string", "description": "Pet's name"},
                "company": {"type": "string", "description": "Company name"},
                "keywords": {"type": "string", "description": "Additional keywords (comma-separated)"},
                "output": {"type": "string", "description": "Output file"},
                "leet": {"type": "boolean", "description": "Add leet speak variations"},
            },
            "required": [],
        },
    },
    {
        "name": "hash_identifier",
        "description": "Identify hash type from a hash string",
        "inputSchema": {
            "type": "object",
            "properties": {
                "hash": {"type": "string", "description": "Hash string to identify"},
            },
            "required": ["hash"],
        },
    },
    {
        "name": "hashid_identify",
        "description": "Advanced hash identification supporting 600+ hash types with hashcat/john modes",
        "inputSchema": {
            "type": "object",
            "properties": {
                "hash": {"type": "string", "description": "Hash string or file with hashes"},
                "extended": {"type": "boolean", "description": "Show extended info (hashcat/john modes)"},
                "mode": {"type": "string", "description": "Show specific: hashcat (-m) or john (-j) modes"},
            },
            "required": ["hash"],
        },
    },
    {
        "name": "ophcrack_crack",
        "description": "Rainbow table password cracking for Windows LM/NTLM hashes",
        "inputSchema": {
            "type": "object",
            "properties": {
                "hash_file": {"type": "string", "description": "File with hashes (pwdump format)"},
                "tables_dir": {"type": "string", "description": "Directory with rainbow tables"},
                "table_type": {"type": "string", "description": "Table type: xp_free, xp_special, vista_free, etc."},
                "output": {"type": "string", "description": "Output file"},
                "num_threads": {"type": "integer", "description": "Number of threads"},
            },
            "required": ["hash_file"],
        },
    },
    {
        "name": "patator_brute",
        "description": "Multi-purpose brute-forcer supporting SSH, FTP, HTTP, SMTP, SQL, LDAP, etc.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "module": {"type": "string", "description": "Module: ssh_login, ftp_login, http_fuzz, smtp_login, mysql_login, ldap_login, rdp_login, smb_login, vnc_login"},
                "host": {"type": "string", "description": "Target host"},
                "port": {"type": "integer", "description": "Target port"},
                "user_file": {"type": "string", "description": "Username wordlist file"},
                "pass_file": {"type": "string", "description": "Password wordlist file"},
                "user": {"type": "string", "description": "Single username"},
                "threads": {"type": "integer", "description": "Number of threads (default: 10)"},
                "extra_args": {"type": "string", "description": "Additional module-specific arguments"},
            },
            "required": ["module", "host"],
        },
    },
    {
        "name": "mentalist_generate",
        "description": "Mentalist wordlist generator with chain rules and transformations",
        "inputSchema": {
            "type": "object",
            "properties": {
                "base_words": {"type": "string", "description": "Base wordlist file"},
                "rules": {"type": "string", "description": "Rules to apply: append_num, prepend_special, capitalize, leet, reverse"},
                "append": {"type": "string", "description": "String to append to each word"},
                "prepend": {"type": "string", "description": "String to prepend to each word"},
                "case": {"type": "string", "description": "Case: upper, lower, capitalize, toggle"},
                "output": {"type": "string", "description": "Output file"},
            },
            "required": ["base_words", "output"],
        },
    },
    {
        "name": "kwprocessor_generate",
        "description": "Keyboard walk pattern generator (kwprocessor)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "basechars": {"type": "string", "description": "Base characters file"},
                "keywalk_south": {"type": "integer", "description": "Max steps south (default: 1)"},
                "keywalk_north": {"type": "integer", "description": "Max steps north"},
                "keywalk_west": {"type": "integer", "description": "Max steps west"},
                "keywalk_east": {"type": "integer", "description": "Max steps east"},
                "output_length": {"type": "integer", "description": "Output word length"},
                "output": {"type": "string", "description": "Output file"},
                "keyboard": {"type": "string", "description": "Keyboard layout: en, de, fr, ru"},
            },
            "required": [],
        },
    },
    {
        "name": "princeprocessor_generate",
        "description": "PRINCE algorithm - password generation by combining dictionary words",
        "inputSchema": {
            "type": "object",
            "properties": {
                "wordlist": {"type": "string", "description": "Input wordlist file"},
                "min_length": {"type": "integer", "description": "Minimum output length"},
                "max_length": {"type": "integer", "description": "Maximum output length"},
                "min_elem": {"type": "integer", "description": "Minimum number of combined elements"},
                "max_elem": {"type": "integer", "description": "Maximum number of combined elements"},
                "output": {"type": "string", "description": "Output file"},
            },
            "required": ["wordlist"],
        },
    },
    {
        "name": "john_crack",
        "description": "John the Ripper password cracker",
        "inputSchema": {
            "type": "object",
            "properties": {
                "hash_file": {"type": "string", "description": "File with hashes to crack"},
                "format": {"type": "string", "description": "Hash format (e.g. raw-md5, raw-sha256, ntlm, bcrypt, zip)"},
                "wordlist": {"type": "string", "description": "Wordlist file for dictionary attack"},
                "rules": {"type": "string", "description": "Wordlist rules (e.g. All, Jumbo, best64)"},
                "incremental": {"type": "string", "description": "Incremental mode charset"},
                "mask": {"type": "string", "description": "Mask for mask attack (e.g. ?u?l?l?l?d?d?d?d)"},
                "fork": {"type": "integer", "description": "Number of processes to fork"},
                "session": {"type": "string", "description": "Session name"},
                "restore": {"type": "string", "description": "Restore session name"},
            },
            "required": ["hash_file"],
        },
    },
    {
        "name": "john_show",
        "description": "Show cracked passwords from John the Ripper pot file",
        "inputSchema": {
            "type": "object",
            "properties": {
                "hash_file": {"type": "string", "description": "Original hash file"},
                "format": {"type": "string", "description": "Hash format"},
                "pot": {"type": "string", "description": "Custom pot file path"},
            },
            "required": ["hash_file"],
        },
    },
    {
        "name": "john_rules",
        "description": "Process wordlist with John the Ripper rules (mangling)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "wordlist": {"type": "string", "description": "Input wordlist"},
                "rules": {"type": "string", "description": "Rule set: All, best64, Jumbo, d3ad0ne, T0XlC"},
                "output": {"type": "string", "description": "Output file (stdout if not specified)"},
            },
            "required": ["wordlist", "rules"],
        },
    },
    {
        "name": "wordlistctl_fetch",
        "description": "Download and manage wordlists from public repositories",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action: fetch, search, list"},
                "name": {"type": "string", "description": "Wordlist name to fetch/search"},
                "category": {"type": "string", "description": "Category: usernames, passwords, discovery, fuzzing, misc"},
                "output_dir": {"type": "string", "description": "Output directory"},
                "decompress": {"type": "boolean", "description": "Decompress after downloading"},
            },
            "required": ["action"],
        },
    },
    {
        "name": "username_anarchy",
        "description": "Generate username permutations from names (e.g. john.smith → jsmith, smithj, etc.)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Full name (e.g. 'John Smith')"},
                "input_file": {"type": "string", "description": "File with names (one per line)"},
                "format": {"type": "string", "description": "Custom format string"},
                "select": {"type": "string", "description": "Select specific plugins (comma-separated)"},
                "output": {"type": "string", "description": "Output file"},
            },
            "required": [],
        },
    },
    {
        "name": "rsmangler_mangle",
        "description": "Mangle and permute words for targeted password list generation",
        "inputSchema": {
            "type": "object",
            "properties": {
                "input_file": {"type": "string", "description": "Input wordlist file"},
                "min_length": {"type": "integer", "description": "Minimum output length"},
                "max_length": {"type": "integer", "description": "Maximum output length"},
                "leet": {"type": "boolean", "description": "Add leet speak permutations"},
                "double": {"type": "boolean", "description": "Double each word"},
                "reverse": {"type": "boolean", "description": "Add reversed words"},
                "capital": {"type": "boolean", "description": "Capitalize permutations"},
                "output": {"type": "string", "description": "Output file"},
            },
            "required": ["input_file"],
        },
    },
]


async def dispatch_tool(name: str, args: Dict) -> str:
    if name == "cewl_generate":
        cmd = [_find_tool("cewl"), args["url"]]
        if args.get("depth"):
            cmd.extend(["-d", str(args["depth"])])
        if args.get("min_length"):
            cmd.extend(["-m", str(args["min_length"])])
        if args.get("max_length"):
            cmd.extend(["--max_word_length", str(args["max_length"])])
        if args.get("with_numbers"):
            cmd.append("--with-numbers")
        if args.get("email"):
            cmd.append("-e")
        if args.get("meta"):
            cmd.append("-a")
        if args.get("output"):
            cmd.extend(["-w", args["output"]])
        if args.get("count"):
            cmd.append("-c")
        if args.get("lowercase"):
            cmd.append("--lowercase")
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "crunch_generate":
        cmd = [_find_tool("crunch"), str(args["min_length"]), str(args["max_length"])]
        if args.get("charset"):
            cmd.append(args["charset"])
        if args.get("pattern"):
            cmd.extend(["-t", args["pattern"]])
        if args.get("output"):
            cmd.extend(["-o", args["output"]])
        if args.get("start_string"):
            cmd.extend(["-s", args["start_string"]])
        if args.get("count"):
            cmd.extend(["-c", str(args["count"])])
        if args.get("compress"):
            cmd.append("-z gzip")
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "cupp_generate":
        if args.get("interactive"):
            cmd = [_find_tool("cupp"), "-i"]
            r = _run_tool(cmd, timeout=60)
            return json.dumps(r, indent=2)
        # Non-interactive: create a config and run
        script = "from cupp import *\nimport sys\n"
        fields = {
            "name": args.get("name", ""),
            "surname": args.get("surname", ""),
            "nick": args.get("nickname", ""),
            "birthdate": args.get("birthdate", ""),
            "partner": args.get("partner_name", ""),
            "partner_bd": args.get("partner_birthdate", ""),
            "pet": args.get("pet_name", ""),
            "company": args.get("company", ""),
            "keywords": args.get("keywords", "").split(",") if args.get("keywords") else [],
            "leet": args.get("leet", False),
        }
        cmd = [_find_tool("cupp"), "-i"]  # Would need stdin, fallback
        r = {"info": "Use CUPP interactively or provide profile data", "profile": fields}
        return json.dumps(r, indent=2)

    elif name == "hash_identifier":
        cmd = [_find_tool("hash-identifier")]
        try:
            proc = subprocess.run(
                cmd, input=args["hash"] + "\n\n", capture_output=True,
                text=True, timeout=30, encoding="utf-8", errors="replace",
            )
            return json.dumps({
                "success": True,
                "stdout": proc.stdout.strip()[:50000],
                "stderr": proc.stderr.strip()[:5000],
            }, indent=2)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    elif name == "hashid_identify":
        cmd = [_find_tool("hashid")]
        if args.get("extended"):
            cmd.append("-e")
        if args.get("mode") == "hashcat":
            cmd.append("-m")
        elif args.get("mode") == "john":
            cmd.append("-j")
        if os.path.isfile(args["hash"]):
            cmd.extend(["-f", args["hash"]])
        else:
            cmd.append(args["hash"])
        r = _run_tool(cmd, timeout=30)
        return json.dumps(r, indent=2)

    elif name == "ophcrack_crack":
        cmd = [_find_tool("ophcrack"), "-g", "-d", args.get("tables_dir", "/usr/share/ophcrack/tables")]
        cmd.extend(["-f", args["hash_file"]])
        if args.get("table_type"):
            cmd.extend(["-t", args["table_type"]])
        if args.get("output"):
            cmd.extend(["-o", args["output"]])
        if args.get("num_threads"):
            cmd.extend(["-n", str(args["num_threads"])])
        r = _run_tool(cmd, timeout=3600)
        return json.dumps(r, indent=2)

    elif name == "patator_brute":
        cmd = [_find_tool("patator"), args["module"]]
        cmd.append(f"host={args['host']}")
        if args.get("port"):
            cmd.append(f"port={args['port']}")
        if args.get("user_file"):
            cmd.append(f"user=FILE0")
            cmd.append(f"0={args['user_file']}")
        elif args.get("user"):
            cmd.append(f"user={args['user']}")
        if args.get("pass_file"):
            idx = "1" if args.get("user_file") else "0"
            cmd.append(f"password=FILE{idx}")
            cmd.append(f"{idx}={args['pass_file']}")
        if args.get("threads"):
            cmd.extend(["--threads", str(args["threads"])])
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=1800)
        return json.dumps(r, indent=2)

    elif name == "mentalist_generate":
        # Mentalist is mainly GUI, we use a simplified CLI approach
        cmd = [_find_tool("mentalist"), "--base", args["base_words"], "-o", args["output"]]
        if args.get("append"):
            cmd.extend(["--append", args["append"]])
        if args.get("prepend"):
            cmd.extend(["--prepend", args["prepend"]])
        if args.get("case"):
            cmd.extend(["--case", args["case"]])
        if args.get("rules"):
            cmd.extend(["--rules", args["rules"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "kwprocessor_generate":
        cmd = [_find_tool("kwp")]
        if args.get("basechars"):
            cmd.append(args["basechars"])
        if args.get("keywalk_south"):
            cmd.extend(["-s", str(args["keywalk_south"])])
        if args.get("keywalk_west"):
            cmd.extend(["-w", str(args["keywalk_west"])])
        if args.get("keywalk_east"):
            cmd.extend(["-e", str(args["keywalk_east"])])
        if args.get("keywalk_north"):
            cmd.extend(["-n", str(args["keywalk_north"])])
        if args.get("keyboard"):
            cmd.extend(["-z", args["keyboard"]])
        if args.get("output_length"):
            cmd.extend(["-l", str(args["output_length"])])
        r = _run_tool(cmd, timeout=300)
        if args.get("output") and r.get("success"):
            with open(args["output"], "w") as f:
                f.write(r.get("stdout", ""))
        return json.dumps(r, indent=2)

    elif name == "princeprocessor_generate":
        cmd = [_find_tool("pp64.bin"), args["wordlist"]]
        if args.get("min_length"):
            cmd.extend(["--pw-min", str(args["min_length"])])
        if args.get("max_length"):
            cmd.extend(["--pw-max", str(args["max_length"])])
        if args.get("min_elem"):
            cmd.extend(["--elem-cnt-min", str(args["min_elem"])])
        if args.get("max_elem"):
            cmd.extend(["--elem-cnt-max", str(args["max_elem"])])
        r = _run_tool(cmd, timeout=300)
        if args.get("output") and r.get("success"):
            with open(args["output"], "w") as f:
                f.write(r.get("stdout", ""))
        return json.dumps(r, indent=2)

    elif name == "john_crack":
        cmd = [_find_tool("john")]
        if args.get("format"):
            cmd.extend(["--format=" + args["format"]])
        if args.get("wordlist"):
            cmd.extend(["--wordlist=" + args["wordlist"]])
        if args.get("rules"):
            cmd.extend(["--rules=" + args["rules"]])
        if args.get("incremental"):
            cmd.extend(["--incremental=" + args["incremental"]])
        if args.get("mask"):
            cmd.extend(["--mask=" + args["mask"]])
        if args.get("fork"):
            cmd.extend(["--fork=" + str(args["fork"])])
        if args.get("session"):
            cmd.extend(["--session=" + args["session"]])
        if args.get("restore"):
            cmd.extend(["--restore=" + args["restore"]])
        else:
            cmd.append(args["hash_file"])
        r = _run_tool(cmd, timeout=3600)
        return json.dumps(r, indent=2)

    elif name == "john_show":
        cmd = [_find_tool("john"), "--show", args["hash_file"]]
        if args.get("format"):
            cmd.extend(["--format=" + args["format"]])
        if args.get("pot"):
            cmd.extend(["--pot=" + args["pot"]])
        r = _run_tool(cmd, timeout=30)
        return json.dumps(r, indent=2)

    elif name == "john_rules":
        cmd = [_find_tool("john"), "--wordlist=" + args["wordlist"],
               "--rules=" + args["rules"], "--stdout"]
        r = _run_tool(cmd, timeout=300)
        if args.get("output") and r.get("success"):
            with open(args["output"], "w") as f:
                f.write(r.get("stdout", ""))
        return json.dumps(r, indent=2)

    elif name == "wordlistctl_fetch":
        cmd = [_find_tool("wordlistctl")]
        action = args["action"]
        if action == "fetch":
            cmd.extend(["fetch", args.get("name", "")])
            if args.get("output_dir"):
                cmd.extend(["-d", args["output_dir"]])
            if args.get("decompress"):
                cmd.append("-x")
        elif action == "search":
            cmd.extend(["search", args.get("name", "")])
        elif action == "list":
            cmd.append("list")
            if args.get("category"):
                cmd.append(args["category"])
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "username_anarchy":
        cmd = [_find_tool("username-anarchy")]
        if args.get("name"):
            cmd.append(args["name"])
        if args.get("input_file"):
            cmd.extend(["-i", args["input_file"]])
        if args.get("format"):
            cmd.extend(["--format", args["format"]])
        if args.get("select"):
            cmd.extend(["--select-format", args["select"]])
        r = _run_tool(cmd, timeout=60)
        if args.get("output") and r.get("success"):
            with open(args["output"], "w") as f:
                f.write(r.get("stdout", ""))
        return json.dumps(r, indent=2)

    elif name == "rsmangler_mangle":
        cmd = [_find_tool("rsmangler"), "-f", args["input_file"]]
        if args.get("min_length"):
            cmd.extend(["--min", str(args["min_length"])])
        if args.get("max_length"):
            cmd.extend(["--max", str(args["max_length"])])
        if args.get("leet"):
            cmd.append("-l")
        if args.get("double"):
            cmd.append("-d")
        if args.get("reverse"):
            cmd.append("-r")
        if args.get("capital"):
            cmd.append("-c")
        r = _run_tool(cmd, timeout=300)
        if args.get("output") and r.get("success"):
            with open(args["output"], "w") as f:
                f.write(r.get("stdout", ""))
        return json.dumps(r, indent=2)

    return json.dumps({"error": f"Unknown tool: {name}"})


async def handle_message(msg: Dict) -> Optional[Dict]:
    method = msg.get("method", "")
    mid = msg.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": SERVER_NAME, "version": VERSION},
        }}
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = msg.get("params", {})
        try:
            result_text = await dispatch_tool(params.get("name", ""), params.get("arguments", {}))
        except Exception as exc:
            result_text = json.dumps({"error": str(exc)})
        return {"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": result_text}]}}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"Method not found: {method}"}}


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
