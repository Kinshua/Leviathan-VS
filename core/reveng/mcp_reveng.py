#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP Reverse Engineering Server v1.0.0

    Binary analysis, disassembly, debugging, malware analysis tools.
    Integrates: objdump, readelf, ltrace, strace, dex2jar, pefile,
                oletools, upx, detect-it-easy, binwalk, yara, capa.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (16):
        - objdump_disasm: Disassemble binary with objdump
        - readelf_analyze: Analyze ELF binary headers and sections
        - ltrace_trace: Trace library calls in a process
        - strace_trace: Trace system calls in a process
        - dex2jar_convert: Convert Android DEX to JAR for analysis
        - pefile_analyze: Analyze PE (Windows EXE/DLL) files with Python pefile
        - oletools_analyze: Analyze Office documents for macros/malware (oletools)
        - upx_pack: Pack/unpack executables with UPX
        - die_detect: Detect-It-Easy - identify file type, packer, compiler, etc.
        - binwalk_extract: Binwalk firmware analysis - extract embedded files
        - yara_scan: Scan files with YARA rules for malware signatures
        - capa_analyze: Identify binary capabilities with capa (MITRE ATT&CK mapping)
        - strings_extract: Extract printable strings from binary files
        - file_identify: Identify file type and magic bytes
        - xxd_hexdump: Create hex dump of binary file
        - nm_symbols: List symbols from binary (nm)

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
import tempfile
from typing import Any, Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger("leviathan-reveng-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-reveng-server"


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
        "name": "objdump_disasm",
        "description": "Disassemble binary sections with objdump",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary": {"type": "string", "description": "Path to binary file"},
                "mode": {
                    "type": "string",
                    "description": "Mode: disasm (-d), all (-D), headers (-x), reloc (-r), symbols (-t), source (-S)",
                },
                "section": {
                    "type": "string",
                    "description": "Specific section (e.g. .text, .plt, .got)",
                },
                "start_addr": {"type": "string", "description": "Start address (hex)"},
                "stop_addr": {"type": "string", "description": "Stop address (hex)"},
                "intel": {
                    "type": "boolean",
                    "description": "Use Intel syntax instead of AT&T",
                },
            },
            "required": ["binary"],
        },
    },
    {
        "name": "readelf_analyze",
        "description": "Analyze ELF binary headers, sections, segments, symbols",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary": {"type": "string", "description": "Path to ELF binary"},
                "mode": {
                    "type": "string",
                    "description": "Mode: headers (-h), sections (-S), segments (-l), symbols (-s), dynamic (-d), relocs (-r), notes (-n), all (-a)",
                },
                "wide": {
                    "type": "boolean",
                    "description": "Wide output (don't truncate)",
                },
            },
            "required": ["binary"],
        },
    },
    {
        "name": "ltrace_trace",
        "description": "Trace library calls of a running or new process",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary": {"type": "string", "description": "Binary to trace"},
                "args": {"type": "string", "description": "Arguments for the binary"},
                "pid": {"type": "integer", "description": "PID to attach to"},
                "filter": {
                    "type": "string",
                    "description": "Library call filter pattern",
                },
                "count": {
                    "type": "boolean",
                    "description": "Count calls and report summary",
                },
                "output": {"type": "string", "description": "Output file"},
                "follow_forks": {
                    "type": "boolean",
                    "description": "Follow forked processes",
                },
            },
            "required": ["binary"],
        },
    },
    {
        "name": "strace_trace",
        "description": "Trace system calls and signals of a process",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary": {"type": "string", "description": "Binary to trace"},
                "args": {"type": "string", "description": "Arguments for the binary"},
                "pid": {"type": "integer", "description": "PID to attach to"},
                "filter": {
                    "type": "string",
                    "description": "Syscall filter (e.g. open,read,write,network)",
                },
                "count": {
                    "type": "boolean",
                    "description": "Count syscalls and report summary",
                },
                "output": {"type": "string", "description": "Output file"},
                "follow_forks": {
                    "type": "boolean",
                    "description": "Follow forked processes",
                },
                "timestamps": {"type": "boolean", "description": "Show timestamps"},
                "strings_length": {
                    "type": "integer",
                    "description": "Max string length to print",
                },
            },
            "required": ["binary"],
        },
    },
    {
        "name": "dex2jar_convert",
        "description": "Convert Android DEX files to JAR for decompilation",
        "inputSchema": {
            "type": "object",
            "properties": {
                "input_file": {
                    "type": "string",
                    "description": "Input DEX or APK file",
                },
                "output": {"type": "string", "description": "Output JAR file"},
                "force": {"type": "boolean", "description": "Force overwrite output"},
            },
            "required": ["input_file"],
        },
    },
    {
        "name": "pefile_analyze",
        "description": "Analyze Windows PE files (EXE/DLL) - imports, exports, sections, headers",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary": {"type": "string", "description": "Path to PE file"},
                "mode": {
                    "type": "string",
                    "description": "Mode: info (general), imports, exports, sections, resources, strings, all",
                },
            },
            "required": ["binary"],
        },
    },
    {
        "name": "oletools_analyze",
        "description": "Analyze Office documents for embedded macros, OLE objects, and malware indicators",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "Office document to analyze"},
                "tool": {
                    "type": "string",
                    "description": "Tool: olevba (macro extraction), oleid (indicators), rtfobj (RTF objects), oleobj (OLE objects), mraptor (macro risk)",
                },
                "decode": {
                    "type": "boolean",
                    "description": "Decode obfuscated strings",
                },
            },
            "required": ["file"],
        },
    },
    {
        "name": "upx_pack",
        "description": "Pack or unpack executables with UPX compressor",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary": {"type": "string", "description": "Path to binary file"},
                "action": {
                    "type": "string",
                    "description": "Action: pack, unpack (-d), test (-t), list (-l)",
                },
                "level": {
                    "type": "integer",
                    "description": "Compression level 1-9 (9=best, slowest)",
                },
                "output": {"type": "string", "description": "Output file"},
                "force": {"type": "boolean", "description": "Force operation"},
            },
            "required": ["binary"],
        },
    },
    {
        "name": "die_detect",
        "description": "Detect-It-Easy - identify file type, packer, compiler, linker, protection",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "File to analyze"},
                "deep_scan": {"type": "boolean", "description": "Deep scan mode"},
                "json_output": {"type": "boolean", "description": "JSON output"},
                "recursive": {
                    "type": "boolean",
                    "description": "Recursive analysis (for archives)",
                },
            },
            "required": ["file"],
        },
    },
    {
        "name": "binwalk_extract",
        "description": "Binwalk - analyze and extract embedded files from firmware/binaries",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "File to analyze"},
                "extract": {"type": "boolean", "description": "Extract embedded files"},
                "matryoshka": {
                    "type": "boolean",
                    "description": "Recursive extraction (matryoshka mode)",
                },
                "entropy": {"type": "boolean", "description": "Entropy analysis"},
                "signature": {"type": "boolean", "description": "Signature scan only"},
                "output_dir": {
                    "type": "string",
                    "description": "Output directory for extraction",
                },
                "raw": {
                    "type": "string",
                    "description": "Raw bytes search pattern (hex)",
                },
            },
            "required": ["file"],
        },
    },
    {
        "name": "yara_scan",
        "description": "Scan files/directories with YARA rules for malware detection",
        "inputSchema": {
            "type": "object",
            "properties": {
                "rules": {
                    "type": "string",
                    "description": "YARA rules file or directory",
                },
                "target": {
                    "type": "string",
                    "description": "File or directory to scan",
                },
                "recursive": {
                    "type": "boolean",
                    "description": "Scan directories recursively",
                },
                "strings": {"type": "boolean", "description": "Show matching strings"},
                "count": {"type": "boolean", "description": "Show match count only"},
                "tag": {"type": "string", "description": "Filter rules by tag"},
                "timeout": {
                    "type": "integer",
                    "description": "Scan timeout in seconds",
                },
            },
            "required": ["rules", "target"],
        },
    },
    {
        "name": "capa_analyze",
        "description": "Identify program capabilities and map to MITRE ATT&CK with capa",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "Binary file to analyze"},
                "format": {
                    "type": "string",
                    "description": "Output format: default, json, vverbose",
                },
                "rules_dir": {
                    "type": "string",
                    "description": "Custom rules directory",
                },
                "signatures": {
                    "type": "string",
                    "description": "Custom signatures path",
                },
                "tag": {
                    "type": "string",
                    "description": "Filter by tag/ATT&CK technique",
                },
            },
            "required": ["file"],
        },
    },
    {
        "name": "strings_extract",
        "description": "Extract printable strings from binary files",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "Binary file to analyze"},
                "min_length": {
                    "type": "integer",
                    "description": "Minimum string length (default: 4)",
                },
                "encoding": {
                    "type": "string",
                    "description": "Encoding: s (7-bit), S (8-bit), l (16-bit LE), b (16-bit BE), L (32-bit LE), B (32-bit BE)",
                },
                "offset": {
                    "type": "boolean",
                    "description": "Show file offset of each string",
                },
                "radix": {
                    "type": "string",
                    "description": "Offset radix: o (octal), d (decimal), x (hex)",
                },
            },
            "required": ["file"],
        },
    },
    {
        "name": "file_identify",
        "description": "Identify file type using magic bytes and signatures",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "File to identify"},
                "mime": {"type": "boolean", "description": "Output MIME type"},
                "brief": {"type": "boolean", "description": "Brief mode (no filename)"},
                "magic_file": {"type": "string", "description": "Custom magic file"},
            },
            "required": ["file"],
        },
    },
    {
        "name": "xxd_hexdump",
        "description": "Create hex dump of binary file",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "File to dump"},
                "length": {"type": "integer", "description": "Number of bytes to dump"},
                "offset": {"type": "integer", "description": "Start offset"},
                "cols": {
                    "type": "integer",
                    "description": "Columns per line (default: 16)",
                },
                "bits": {
                    "type": "boolean",
                    "description": "Show in binary instead of hex",
                },
                "include": {
                    "type": "boolean",
                    "description": "Output as C include array",
                },
                "plain": {
                    "type": "boolean",
                    "description": "Plain hex dump (no formatting)",
                },
            },
            "required": ["file"],
        },
    },
    {
        "name": "nm_symbols",
        "description": "List symbols from binary files (nm)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary": {"type": "string", "description": "Path to binary file"},
                "dynamic": {
                    "type": "boolean",
                    "description": "Show dynamic symbols only (-D)",
                },
                "defined_only": {
                    "type": "boolean",
                    "description": "Show only defined symbols",
                },
                "undefined_only": {
                    "type": "boolean",
                    "description": "Show only undefined symbols (-u)",
                },
                "demangle": {
                    "type": "boolean",
                    "description": "Demangle C++ symbol names",
                },
                "sort_by_size": {
                    "type": "boolean",
                    "description": "Sort by symbol size",
                },
            },
            "required": ["binary"],
        },
    },
]


async def dispatch_tool(name: str, args: Dict) -> str:
    if name == "objdump_disasm":
        cmd = [_find_tool("objdump")]
        mode = args.get("mode", "disasm")
        mode_map = {
            "disasm": "-d",
            "all": "-D",
            "headers": "-x",
            "reloc": "-r",
            "symbols": "-t",
            "source": "-S",
        }
        cmd.append(mode_map.get(mode, "-d"))
        if args.get("intel"):
            cmd.extend(["-M", "intel"])
        if args.get("section"):
            cmd.extend(["-j", args["section"]])
        if args.get("start_addr"):
            cmd.extend(["--start-address", args["start_addr"]])
        if args.get("stop_addr"):
            cmd.extend(["--stop-address", args["stop_addr"]])
        cmd.append(args["binary"])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "readelf_analyze":
        cmd = [_find_tool("readelf")]
        mode = args.get("mode", "all")
        mode_map = {
            "headers": "-h",
            "sections": "-S",
            "segments": "-l",
            "symbols": "-s",
            "dynamic": "-d",
            "relocs": "-r",
            "notes": "-n",
            "all": "-a",
        }
        cmd.append(mode_map.get(mode, "-a"))
        if args.get("wide"):
            cmd.append("-W")
        cmd.append(args["binary"])
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "ltrace_trace":
        cmd = [_find_tool("ltrace")]
        if args.get("pid"):
            cmd.extend(["-p", str(args["pid"])])
        else:
            cmd.append(args["binary"])
            if args.get("args"):
                cmd.extend(args["args"].split())
        if args.get("filter"):
            cmd.extend(["-e", args["filter"]])
        if args.get("count"):
            cmd.append("-c")
        if args.get("output"):
            cmd.extend(["-o", args["output"]])
        if args.get("follow_forks"):
            cmd.append("-f")
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "strace_trace":
        cmd = [_find_tool("strace")]
        if args.get("pid"):
            cmd.extend(["-p", str(args["pid"])])
        if args.get("filter"):
            cmd.extend(["-e", f"trace={args['filter']}"])
        if args.get("count"):
            cmd.append("-c")
        if args.get("output"):
            cmd.extend(["-o", args["output"]])
        if args.get("follow_forks"):
            cmd.append("-f")
        if args.get("timestamps"):
            cmd.append("-t")
        if args.get("strings_length"):
            cmd.extend(["-s", str(args["strings_length"])])
        if not args.get("pid"):
            cmd.append(args["binary"])
            if args.get("args"):
                cmd.extend(args["args"].split())
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "dex2jar_convert":
        cmd = [_find_tool("d2j-dex2jar"), args["input_file"]]
        if args.get("output"):
            cmd.extend(["-o", args["output"]])
        if args.get("force"):
            cmd.append("--force")
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "pefile_analyze":
        mode = args.get("mode", "info")
        script = f"""
import pefile, json, sys
try:
    pe = pefile.PE(r'{args["binary"]}')
    result = {{}}
    if '{mode}' in ('info', 'all'):
        result['machine'] = hex(pe.FILE_HEADER.Machine)
        result['timestamp'] = pe.FILE_HEADER.TimeDateStamp
        result['subsystem'] = pe.OPTIONAL_HEADER.Subsystem
        result['dll_characteristics'] = hex(pe.OPTIONAL_HEADER.DllCharacteristics)
        result['entry_point'] = hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
        result['image_base'] = hex(pe.OPTIONAL_HEADER.ImageBase)
        aslr = bool(pe.OPTIONAL_HEADER.DllCharacteristics & 0x0040)
        dep = bool(pe.OPTIONAL_HEADER.DllCharacteristics & 0x0100)
        result['ASLR'] = aslr
        result['DEP'] = dep
    if '{mode}' in ('sections', 'all'):
        result['sections'] = [{{
            'name': s.Name.decode('utf-8','ignore').strip('\\x00'),
            'virtual_addr': hex(s.VirtualAddress),
            'virtual_size': s.Misc_VirtualSize,
            'raw_size': s.SizeOfRawData,
            'entropy': round(s.get_entropy(), 2),
            'characteristics': hex(s.Characteristics),
        }} for s in pe.sections]
    if '{mode}' in ('imports', 'all'):
        imports = []
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                dll = entry.dll.decode('utf-8','ignore')
                funcs = [i.name.decode('utf-8','ignore') if i.name else f'ord({{i.ordinal}})' for i in entry.imports[:50]]
                imports.append({{'dll': dll, 'functions': funcs, 'count': len(entry.imports)}})
        result['imports'] = imports
    if '{mode}' in ('exports', 'all'):
        exports = []
        if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
            for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols[:100]:
                exports.append({{'name': exp.name.decode('utf-8','ignore') if exp.name else '', 'ordinal': exp.ordinal, 'address': hex(exp.address)}})
        result['exports'] = exports
    if '{mode}' in ('strings', 'all'):
        result['strings_count'] = len(pe.get_strings())
    print(json.dumps(result, indent=2))
except Exception as e:
    print(json.dumps({{'error': str(e)}}))
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(script)
            f.flush()
            r = _run_tool([sys.executable, f.name], timeout=60)
            os.unlink(f.name)
        return json.dumps(r, indent=2)

    elif name == "oletools_analyze":
        tool = args.get("tool", "olevba")
        tool_map = {
            "olevba": "olevba",
            "oleid": "oleid",
            "rtfobj": "rtfobj",
            "oleobj": "oleobj",
            "mraptor": "mraptor",
        }
        cmd = [_find_tool(tool_map.get(tool, "olevba")), args["file"]]
        if tool == "olevba" and args.get("decode"):
            cmd.append("--decode")
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "upx_pack":
        cmd = [_find_tool("upx")]
        action = args.get("action", "pack")
        if action == "unpack":
            cmd.append("-d")
        elif action == "test":
            cmd.append("-t")
        elif action == "list":
            cmd.append("-l")
        if action == "pack" and args.get("level"):
            cmd.append(f"-{args['level']}")
        if args.get("output"):
            cmd.extend(["-o", args["output"]])
        if args.get("force"):
            cmd.append("-f")
        cmd.append(args["binary"])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "die_detect":
        cmd = [_find_tool("diec"), args["file"]]
        if args.get("deep_scan"):
            cmd.append("--deepscan")
        if args.get("json_output"):
            cmd.append("--json")
        if args.get("recursive"):
            cmd.append("-r")
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "binwalk_extract":
        cmd = [_find_tool("binwalk")]
        if args.get("extract"):
            cmd.append("-e")
        if args.get("matryoshka"):
            cmd.append("-Me")
        if args.get("entropy"):
            cmd.append("-E")
        if args.get("signature"):
            cmd.append("-B")
        if args.get("output_dir"):
            cmd.extend(["-C", args["output_dir"]])
        if args.get("raw"):
            cmd.extend(["-R", args["raw"]])
        cmd.append(args["file"])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "yara_scan":
        cmd = [_find_tool("yara")]
        if args.get("recursive"):
            cmd.append("-r")
        if args.get("strings"):
            cmd.append("-s")
        if args.get("count"):
            cmd.append("-c")
        if args.get("tag"):
            cmd.extend(["-t", args["tag"]])
        if args.get("timeout"):
            cmd.extend(["-a", str(args["timeout"])])
        cmd.extend([args["rules"], args["target"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "capa_analyze":
        cmd = [_find_tool("capa"), args["file"]]
        if args.get("format") == "json":
            cmd.append("-j")
        elif args.get("format") == "vverbose":
            cmd.append("-vv")
        if args.get("rules_dir"):
            cmd.extend(["-r", args["rules_dir"]])
        if args.get("signatures"):
            cmd.extend(["-s", args["signatures"]])
        if args.get("tag"):
            cmd.extend(["-t", args["tag"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "strings_extract":
        cmd = [_find_tool("strings")]
        if args.get("min_length"):
            cmd.extend(["-n", str(args["min_length"])])
        if args.get("encoding"):
            cmd.extend(["-e", args["encoding"]])
        if args.get("offset"):
            cmd.append("-t")
            cmd.append(args.get("radix", "x"))
        cmd.append(args["file"])
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "file_identify":
        cmd = [_find_tool("file")]
        if args.get("mime"):
            cmd.append("--mime")
        if args.get("brief"):
            cmd.append("-b")
        if args.get("magic_file"):
            cmd.extend(["-m", args["magic_file"]])
        cmd.append(args["file"])
        r = _run_tool(cmd, timeout=30)
        return json.dumps(r, indent=2)

    elif name == "xxd_hexdump":
        cmd = [_find_tool("xxd")]
        if args.get("length"):
            cmd.extend(["-l", str(args["length"])])
        if args.get("offset"):
            cmd.extend(["-s", str(args["offset"])])
        if args.get("cols"):
            cmd.extend(["-c", str(args["cols"])])
        if args.get("bits"):
            cmd.append("-b")
        if args.get("include"):
            cmd.append("-i")
        if args.get("plain"):
            cmd.append("-p")
        cmd.append(args["file"])
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "nm_symbols":
        cmd = [_find_tool("nm")]
        if args.get("dynamic"):
            cmd.append("-D")
        if args.get("defined_only"):
            cmd.append("--defined-only")
        if args.get("undefined_only"):
            cmd.append("-u")
        if args.get("demangle"):
            cmd.append("-C")
        if args.get("sort_by_size"):
            cmd.append("--size-sort")
        cmd.append(args["binary"])
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    return json.dumps({"error": f"Unknown tool: {name}"})


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
        try:
            result_text = await dispatch_tool(
                params.get("name", ""), params.get("arguments", {})
            )
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
