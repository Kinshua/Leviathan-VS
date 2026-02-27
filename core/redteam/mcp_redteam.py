#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP Red Team / C2 Server v1.0.0

    Command & Control frameworks, payload generation, EDR evasion.
    Integrates: sliver, mythic, empire, havoc, covenant, armitage,
                macro_pack, donut, scarecrow, shellter, veil, nim payloads.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (16):
        - sliver_c2: Sliver C2 framework - implant generation & management
        - sliver_listener: Start Sliver listener (mTLS, HTTP, HTTPS, DNS)
        - mythic_agent: Mythic C2 agent generation (various languages)
        - mythic_task: Send task to Mythic agent
        - empire_listener: PowerShell Empire listener management
        - empire_stager: Empire stager generation
        - empire_module: Run Empire post-exploitation module
        - havoc_demon: Havoc C2 Demon payload generation
        - covenant_grunt: Covenant C2 Grunt generation
        - armitage_launch: Launch Armitage (MSF GUI for team ops)
        - macro_pack_generate: Generate weaponized Office macros
        - donut_shellcode: Convert .NET assemblies to position-independent shellcode
        - scarecrow_payload: EDR bypass payload with ScareCrow
        - shellter_inject: Inject payload into PE files
        - veil_generate: Veil-Evasion payload generation (AV bypass)
        - nim_payload: Compile Nim-based evasion payloads

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
logger = logging.getLogger("leviathan-redteam-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-redteam-server"


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
        "name": "sliver_c2",
        "description": "Sliver C2 - generate implants (beacon/session) for various OSes",
        "inputSchema": {
            "type": "object",
            "properties": {
                "implant_type": {"type": "string", "description": "Type: beacon or session"},
                "os": {"type": "string", "description": "Target OS: windows, linux, macos"},
                "arch": {"type": "string", "description": "Architecture: amd64, 386, arm64"},
                "format": {"type": "string", "description": "Format: exe, shared, shellcode, service"},
                "c2_url": {"type": "string", "description": "C2 callback URL (e.g. mtls://10.0.0.1:8888)"},
                "name": {"type": "string", "description": "Implant name"},
                "output": {"type": "string", "description": "Output file path"},
                "obfuscate": {"type": "boolean", "description": "Enable code obfuscation"},
                "skip_symbols": {"type": "boolean", "description": "Skip symbol obfuscation"},
                "evasion": {"type": "boolean", "description": "Enable evasion features"},
                "extra_args": {"type": "string", "description": "Additional sliver arguments"},
            },
            "required": ["c2_url"],
        },
    },
    {
        "name": "sliver_listener",
        "description": "Start Sliver C2 listener (mTLS, HTTP, HTTPS, DNS, WireGuard)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "protocol": {"type": "string", "description": "Protocol: mtls, http, https, dns, wg"},
                "host": {"type": "string", "description": "Listen host (default: 0.0.0.0)"},
                "port": {"type": "integer", "description": "Listen port"},
                "domain": {"type": "string", "description": "Domain for DNS/HTTP(S) listeners"},
                "website": {"type": "string", "description": "Website name for HTTP(S) listeners"},
                "persistent": {"type": "boolean", "description": "Persistent listener (survives restart)"},
            },
            "required": ["protocol"],
        },
    },
    {
        "name": "mythic_agent",
        "description": "Mythic C2 - generate agents (Apollo, Medusa, Poseidon, Athena, etc.)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "agent_type": {"type": "string", "description": "Agent: apollo (C#), poseidon (Go), medusa (Python), athena (.NET), merlin (Go)"},
                "c2_profile": {"type": "string", "description": "C2 profile: http, websocket, smb, tcp"},
                "callback_host": {"type": "string", "description": "Callback host URL"},
                "callback_port": {"type": "integer", "description": "Callback port"},
                "output": {"type": "string", "description": "Output file path"},
                "encrypted_key": {"type": "string", "description": "Encryption key"},
            },
            "required": ["agent_type", "callback_host"],
        },
    },
    {
        "name": "mythic_task",
        "description": "Send task to active Mythic C2 agent",
        "inputSchema": {
            "type": "object",
            "properties": {
                "agent_id": {"type": "string", "description": "Target agent callback ID"},
                "command": {"type": "string", "description": "Command to execute on agent"},
                "params": {"type": "string", "description": "Command parameters (JSON string)"},
                "api_url": {"type": "string", "description": "Mythic API URL"},
                "api_token": {"type": "string", "description": "Mythic API token"},
            },
            "required": ["agent_id", "command"],
        },
    },
    {
        "name": "empire_listener",
        "description": "PowerShell Empire - create/manage listeners",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action: create, list, kill"},
                "listener_type": {"type": "string", "description": "Type: http, http_hop, redirector, dbx, onedrive"},
                "name": {"type": "string", "description": "Listener name"},
                "host": {"type": "string", "description": "Listen host"},
                "port": {"type": "integer", "description": "Listen port"},
                "api_url": {"type": "string", "description": "Empire REST API URL"},
                "api_token": {"type": "string", "description": "Empire API token"},
            },
            "required": ["action"],
        },
    },
    {
        "name": "empire_stager",
        "description": "Generate PowerShell Empire stager payloads",
        "inputSchema": {
            "type": "object",
            "properties": {
                "stager_type": {"type": "string", "description": "Type: multi_launcher, multi_bash, windows_dll, windows_hta, windows_macro, osx_applescript"},
                "listener": {"type": "string", "description": "Listener name to use"},
                "output": {"type": "string", "description": "Output file path"},
                "obfuscate": {"type": "boolean", "description": "Enable obfuscation"},
                "language": {"type": "string", "description": "Language: powershell, python, csharp"},
            },
            "required": ["stager_type", "listener"],
        },
    },
    {
        "name": "empire_module",
        "description": "Run Empire post-exploitation module on active agent",
        "inputSchema": {
            "type": "object",
            "properties": {
                "module": {"type": "string", "description": "Module path (e.g. powershell/situational_awareness/network/arpscan)"},
                "agent": {"type": "string", "description": "Target agent name/ID"},
                "options": {"type": "string", "description": "Module options as key=value pairs (semicolon-separated)"},
            },
            "required": ["module", "agent"],
        },
    },
    {
        "name": "havoc_demon",
        "description": "Havoc C2 - generate Demon payload (advanced evasion)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "listener": {"type": "string", "description": "Listener name/URL"},
                "arch": {"type": "string", "description": "Architecture: x64, x86"},
                "format": {"type": "string", "description": "Format: exe, dll, shellcode, raw"},
                "sleep": {"type": "integer", "description": "Sleep interval in seconds"},
                "jitter": {"type": "integer", "description": "Jitter percentage (0-100)"},
                "indirect_syscall": {"type": "boolean", "description": "Use indirect syscalls"},
                "stack_spoof": {"type": "boolean", "description": "Enable stack spoofing"},
                "sleep_technique": {"type": "string", "description": "Sleep technique: WaitForSingleObject, Ekko, Zilean"},
                "injection": {"type": "string", "description": "Injection technique: spawn, inject, fork_run"},
                "output": {"type": "string", "description": "Output file path"},
            },
            "required": ["listener"],
        },
    },
    {
        "name": "covenant_grunt",
        "description": "Covenant C2 - generate Grunt (.NET implant)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "listener": {"type": "string", "description": "Covenant listener name"},
                "implant_template": {"type": "string", "description": "Template: GruntHTTP, GruntSMB, GruntBridge"},
                "dotnet_version": {"type": "string", "description": ".NET version: Net40, Net35, NetCore31"},
                "output_type": {"type": "string", "description": "Output: exe, dll, service"},
                "delay": {"type": "integer", "description": "Callback delay in seconds"},
                "jitter": {"type": "integer", "description": "Jitter percentage"},
                "api_url": {"type": "string", "description": "Covenant API URL"},
                "api_token": {"type": "string", "description": "Covenant API token"},
            },
            "required": ["listener", "implant_template"],
        },
    },
    {
        "name": "armitage_launch",
        "description": "Launch Armitage (Metasploit team collaboration GUI)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "rpc_host": {"type": "string", "description": "MSFRPCD host (default: 127.0.0.1)"},
                "rpc_port": {"type": "integer", "description": "MSFRPCD port (default: 55553)"},
                "rpc_user": {"type": "string", "description": "RPC username"},
                "rpc_pass": {"type": "string", "description": "RPC password"},
            },
            "required": [],
        },
    },
    {
        "name": "macro_pack_generate",
        "description": "Generate weaponized Office macros with macro_pack",
        "inputSchema": {
            "type": "object",
            "properties": {
                "payload_type": {"type": "string", "description": "Type: DROPPER, EMBED_EXE, METERPRETER, WEBMETER, CMD, POWERSHELL"},
                "input_file": {"type": "string", "description": "Input file (payload/shellcode)"},
                "output": {"type": "string", "description": "Output file (.doc, .xls, .ppt, .vba, .hta)"},
                "obfuscate": {"type": "boolean", "description": "Obfuscate macro code"},
                "bypass": {"type": "boolean", "description": "Include AMSI/ETW bypass"},
                "template": {"type": "string", "description": "Office template to use"},
            },
            "required": ["payload_type", "output"],
        },
    },
    {
        "name": "donut_shellcode",
        "description": "Convert .NET/PE/DLL to position-independent shellcode (Donut)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "input_file": {"type": "string", "description": "Input .NET assembly, PE, or DLL"},
                "output": {"type": "string", "description": "Output shellcode file"},
                "arch": {"type": "string", "description": "Architecture: 1 (x86), 2 (amd64), 3 (both)"},
                "class_name": {"type": "string", "description": ".NET class name"},
                "method": {"type": "string", "description": ".NET method name"},
                "args": {"type": "string", "description": "Arguments to pass"},
                "entropy": {"type": "string", "description": "Entropy level: 1 (none), 2 (random names), 3 (random+encrypt)"},
                "bypass": {"type": "string", "description": "AMSI/WLDP bypass: 1 (none), 2 (abort), 3 (patch)"},
                "compress": {"type": "string", "description": "Compression: 1 (none), 2 (aPLib), 3 (LZNT1), 4 (Xpress)"},
            },
            "required": ["input_file"],
        },
    },
    {
        "name": "scarecrow_payload",
        "description": "ScareCrow - EDR bypass payload loader generation",
        "inputSchema": {
            "type": "object",
            "properties": {
                "input_file": {"type": "string", "description": "Input shellcode/payload file"},
                "loader": {"type": "string", "description": "Loader: binary, dll, control, excel, msiexec, wscript"},
                "domain": {"type": "string", "description": "Domain for signed loader certificate"},
                "injection": {"type": "string", "description": "Injection: self, remote, function-stomping"},
                "output": {"type": "string", "description": "Output file"},
                "etw": {"type": "boolean", "description": "Enable ETW patching"},
                "sandbox": {"type": "boolean", "description": "Enable sandbox evasion checks"},
            },
            "required": ["input_file"],
        },
    },
    {
        "name": "shellter_inject",
        "description": "Shellter - dynamic shellcode injection into PE files",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pe_file": {"type": "string", "description": "Target PE file to inject into"},
                "payload": {"type": "string", "description": "Payload: custom, meterpreter_reverse_tcp, shell_reverse_tcp"},
                "shellcode_file": {"type": "string", "description": "Custom shellcode file (if payload=custom)"},
                "lhost": {"type": "string", "description": "LHOST for Metasploit payloads"},
                "lport": {"type": "integer", "description": "LPORT for Metasploit payloads"},
                "stealth": {"type": "boolean", "description": "Stealth mode (preserve original functionality)"},
                "auto": {"type": "boolean", "description": "Automatic mode"},
            },
            "required": ["pe_file"],
        },
    },
    {
        "name": "veil_generate",
        "description": "Veil-Evasion - generate AV-evasion payloads",
        "inputSchema": {
            "type": "object",
            "properties": {
                "payload": {"type": "string", "description": "Payload module (e.g. python/meterpreter/rev_tcp, cs/meterpreter/rev_tcp)"},
                "lhost": {"type": "string", "description": "Local host"},
                "lport": {"type": "integer", "description": "Local port"},
                "output": {"type": "string", "description": "Output file"},
                "extra_options": {"type": "string", "description": "Extra options (key=value semicolon-separated)"},
            },
            "required": ["payload"],
        },
    },
    {
        "name": "nim_payload",
        "description": "Compile Nim-based evasion payloads (OffensiveNim patterns)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Path to Nim source file"},
                "output": {"type": "string", "description": "Output binary path"},
                "target_os": {"type": "string", "description": "Target OS: windows, linux"},
                "arch": {"type": "string", "description": "Architecture: amd64, i386"},
                "release": {"type": "boolean", "description": "Build release mode (optimized)"},
                "strip": {"type": "boolean", "description": "Strip symbols"},
                "extra_args": {"type": "string", "description": "Additional nim compile flags"},
            },
            "required": ["source"],
        },
    },
]


async def dispatch_tool(name: str, args: Dict) -> str:
    if name == "sliver_c2":
        cmd = [_find_tool("sliver-client"), "generate"]
        imp = args.get("implant_type", "beacon")
        if imp == "beacon":
            cmd.append("beacon")
        cmd.extend(["--os", args.get("os", "windows")])
        cmd.extend(["--arch", args.get("arch", "amd64")])
        if args.get("format"):
            cmd.extend(["--format", args["format"]])
        c2 = args["c2_url"]
        if c2.startswith("mtls://"):
            cmd.extend(["--mtls", c2.replace("mtls://", "")])
        elif c2.startswith("https://"):
            cmd.extend(["--https", c2.replace("https://", "")])
        elif c2.startswith("http://"):
            cmd.extend(["--http", c2.replace("http://", "")])
        elif c2.startswith("dns://"):
            cmd.extend(["--dns", c2.replace("dns://", "")])
        if args.get("name"):
            cmd.extend(["--name", args["name"]])
        if args.get("output"):
            cmd.extend(["--save", args["output"]])
        if args.get("obfuscate"):
            cmd.append("--debug")  # Actually --obfuscate not yet in CLI
        if args.get("skip_symbols"):
            cmd.append("--skip-symbols")
        if args.get("evasion"):
            cmd.append("--evasion")
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "sliver_listener":
        proto = args["protocol"]
        cmd = [_find_tool("sliver-client"), proto]
        if args.get("host"):
            cmd.extend(["--lhost", args["host"]])
        if args.get("port"):
            cmd.extend(["--lport", str(args["port"])])
        if args.get("domain"):
            cmd.extend(["--domain", args["domain"]])
        if args.get("website"):
            cmd.extend(["--website", args["website"]])
        if args.get("persistent"):
            cmd.append("--persistent")
        r = _run_tool(cmd, timeout=30)
        return json.dumps(r, indent=2)

    elif name == "mythic_agent":
        # Mythic uses its web API — we use mythic-cli or curl
        cmd = [_find_tool("mythic-cli"), "payload", "create"]
        cmd.extend(["--payload-type", args["agent_type"]])
        cmd.extend(["--callback-host", args["callback_host"]])
        if args.get("callback_port"):
            cmd.extend(["--callback-port", str(args["callback_port"])])
        if args.get("c2_profile"):
            cmd.extend(["--c2-profile", args["c2_profile"]])
        if args.get("output"):
            cmd.extend(["--output", args["output"]])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "mythic_task":
        import urllib.request
        api_url = args.get("api_url", "https://127.0.0.1:7443")
        token = args.get("api_token", "")
        data = json.dumps({
            "action": "create_task",
            "callback_id": args["agent_id"],
            "command": args["command"],
            "params": args.get("params", ""),
        }).encode()
        req = urllib.request.Request(
            f"{api_url}/api/v1.4/tasks",
            data=data,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        )
        try:
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            resp = urllib.request.urlopen(req, timeout=30, context=ctx)
            result = json.loads(resp.read().decode())
            return json.dumps({"success": True, "result": result}, indent=2)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    elif name == "empire_listener":
        action = args["action"]
        if action == "list":
            api_url = args.get("api_url", "https://127.0.0.1:1337")
            token = args.get("api_token", "")
            import urllib.request, ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            req = urllib.request.Request(f"{api_url}/api/v2/listeners", headers={"Authorization": f"Bearer {token}"})
            try:
                resp = urllib.request.urlopen(req, timeout=30, context=ctx)
                return json.dumps({"success": True, "listeners": json.loads(resp.read().decode())}, indent=2)
            except Exception as e:
                return json.dumps({"success": False, "error": str(e)})
        # For create/kill, use powershell-empire CLI
        cmd = [_find_tool("powershell-empire"), "client"]
        r = _run_tool(cmd, timeout=30)
        return json.dumps(r, indent=2)

    elif name == "empire_stager":
        api_url = args.get("api_url", "https://127.0.0.1:1337")
        data = {
            "StagerName": args["stager_type"],
            "Listener": args["listener"],
        }
        if args.get("language"):
            data["Language"] = args["language"]
        if args.get("obfuscate"):
            data["Obfuscate"] = True
        return json.dumps({"info": "Use Empire REST API to create stagers", "payload": data}, indent=2)

    elif name == "empire_module":
        data = {
            "module": args["module"],
            "agent": args["agent"],
        }
        if args.get("options"):
            opts = {}
            for kv in args["options"].split(";"):
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    opts[k.strip()] = v.strip()
            data["options"] = opts
        return json.dumps({"info": "Use Empire REST API", "payload": data}, indent=2)

    elif name == "havoc_demon":
        cmd = [_find_tool("havoc"), "payload", "generate"]
        cmd.extend(["--listener", args["listener"]])
        cmd.extend(["--arch", args.get("arch", "x64")])
        if args.get("format"):
            cmd.extend(["--format", args["format"]])
        if args.get("sleep"):
            cmd.extend(["--sleep", str(args["sleep"])])
        if args.get("jitter"):
            cmd.extend(["--jitter", str(args["jitter"])])
        if args.get("indirect_syscall"):
            cmd.append("--indirect-syscall")
        if args.get("stack_spoof"):
            cmd.append("--stack-spoof")
        if args.get("sleep_technique"):
            cmd.extend(["--sleep-technique", args["sleep_technique"]])
        if args.get("injection"):
            cmd.extend(["--injection", args["injection"]])
        if args.get("output"):
            cmd.extend(["--output", args["output"]])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "covenant_grunt":
        api_url = args.get("api_url", "https://127.0.0.1:7443")
        token = args.get("api_token", "")
        data = {
            "ListenerName": args["listener"],
            "ImplantTemplate": args["implant_template"],
        }
        if args.get("dotnet_version"):
            data["DotNetVersion"] = args["dotnet_version"]
        if args.get("output_type"):
            data["OutputType"] = args["output_type"]
        if args.get("delay"):
            data["Delay"] = args["delay"]
        if args.get("jitter"):
            data["JitterPercent"] = args["jitter"]
        return json.dumps({"info": "Use Covenant API to generate Grunt", "payload": data}, indent=2)

    elif name == "armitage_launch":
        cmd = [_find_tool("armitage")]
        host = args.get("rpc_host", "127.0.0.1")
        port = args.get("rpc_port", 55553)
        user = args.get("rpc_user", "msf")
        pwd = args.get("rpc_pass", "msf")
        cmd.extend(["-h", host, "-p", str(port), "-u", user, "-P", pwd])
        r = _run_tool(cmd, timeout=30)
        return json.dumps(r, indent=2)

    elif name == "macro_pack_generate":
        cmd = [_find_tool("macro_pack"), "-t", args["payload_type"]]
        if args.get("input_file"):
            cmd.extend(["-f", args["input_file"]])
        cmd.extend(["-o", args["output"]])
        if args.get("obfuscate"):
            cmd.append("--obfuscate")
        if args.get("bypass"):
            cmd.append("--bypass")
        if args.get("template"):
            cmd.extend(["--template", args["template"]])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "donut_shellcode":
        cmd = [_find_tool("donut"), args["input_file"]]
        if args.get("output"):
            cmd.extend(["-o", args["output"]])
        if args.get("arch"):
            cmd.extend(["-a", args["arch"]])
        if args.get("class_name"):
            cmd.extend(["-c", args["class_name"]])
        if args.get("method"):
            cmd.extend(["-m", args["method"]])
        if args.get("args"):
            cmd.extend(["-p", args["args"]])
        if args.get("entropy"):
            cmd.extend(["-e", args["entropy"]])
        if args.get("bypass"):
            cmd.extend(["-b", args["bypass"]])
        if args.get("compress"):
            cmd.extend(["-z", args["compress"]])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "scarecrow_payload":
        cmd = [_find_tool("ScareCrow"), "-I", args["input_file"]]
        if args.get("loader"):
            cmd.extend(["-Loader", args["loader"]])
        if args.get("domain"):
            cmd.extend(["-domain", args["domain"]])
        if args.get("injection"):
            cmd.extend(["-injection", args["injection"]])
        if args.get("output"):
            cmd.extend(["-O", args["output"]])
        if args.get("etw"):
            cmd.append("-etw")
        if args.get("sandbox"):
            cmd.append("-sandbox")
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "shellter_inject":
        cmd = [_find_tool("shellter")]
        if args.get("auto"):
            cmd.extend(["-a"])
        cmd.extend(["-f", args["pe_file"]])
        if args.get("payload") and args["payload"] != "custom":
            cmd.extend(["-p", args["payload"]])
        if args.get("shellcode_file"):
            cmd.extend(["-s", args["shellcode_file"]])
        if args.get("lhost"):
            cmd.extend(["--lhost", args["lhost"]])
        if args.get("lport"):
            cmd.extend(["--lport", str(args["lport"])])
        if args.get("stealth"):
            cmd.append("--stealth")
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "veil_generate":
        cmd = [_find_tool("veil"), "-t", "Evasion", "-p", args["payload"]]
        if args.get("lhost"):
            cmd.extend(["--ip", args["lhost"]])
        if args.get("lport"):
            cmd.extend(["--port", str(args["lport"])])
        if args.get("output"):
            cmd.extend(["-o", args["output"]])
        if args.get("extra_options"):
            for opt in args["extra_options"].split(";"):
                if "=" in opt:
                    cmd.extend(["--", opt.strip()])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "nim_payload":
        cmd = [_find_tool("nim"), "c"]
        if args.get("release"):
            cmd.append("-d:release")
        if args.get("strip"):
            cmd.append("--passL:-s")
        if args.get("target_os") == "windows":
            cmd.extend(["--os:windows", "-d:mingw"])
        elif args.get("target_os") == "linux":
            cmd.append("--os:linux")
        if args.get("arch") == "i386":
            cmd.append("--cpu:i386")
        elif args.get("arch") == "amd64":
            cmd.append("--cpu:amd64")
        if args.get("output"):
            cmd.extend(["-o:" + args["output"]])
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        cmd.append(args["source"])
        r = _run_tool(cmd, timeout=300)
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
