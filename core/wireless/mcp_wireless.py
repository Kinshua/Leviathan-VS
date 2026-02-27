#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP Wireless & RF Security Server v1.0.0

    Wireless network hacking, WiFi cracking, Bluetooth & RF attacks.
    Integrates: aircrack-ng suite, bettercap, wifite, reaver, kismet,
                wifipumpkin3, airgeddon, bully, wash, cowpatty.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (16):
        - airmon_start: Enable monitor mode on wireless interface
        - airmon_stop: Disable monitor mode
        - airodump_scan: Capture WiFi networks & clients
        - aireplay_deauth: Deauthentication attack on target AP/client
        - aircrack_wpa: Crack WPA/WPA2 handshake with wordlist
        - aircrack_wep: Crack WEP key from captured IVs
        - wifite_auto: Automated WiFi auditing (WPA/WPS/WEP)
        - reaver_wps: WPS PIN brute-force attack
        - wash_scan: Scan for WPS-enabled access points
        - bully_wps: WPS brute-force (alternative to reaver)
        - bettercap_wifi: WiFi recon & deauth via bettercap
        - bettercap_ble: Bluetooth Low Energy scanning & attacks
        - kismet_scan: Passive WiFi/BT/RF monitoring
        - cowpatty_crack: WPA-PSK cracking with rainbow tables
        - wifipumpkin3_rogueap: Rogue AP / Evil Twin attack framework
        - airgeddon_menu: Interactive wireless audit framework

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
logger = logging.getLogger("leviathan-wireless-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-wireless-server"


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
        return {"success": False, "error": f"Tool not found: {cmd[0]}. Install it first."}
    except Exception as e:
        return {"success": False, "error": str(e)}


TOOLS = [
    {
        "name": "airmon_start",
        "description": "Enable monitor mode on a wireless interface (airmon-ng start)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Wireless interface (e.g. wlan0)"},
                "channel": {"type": "integer", "description": "Lock to specific channel"},
            },
            "required": ["interface"],
        },
    },
    {
        "name": "airmon_stop",
        "description": "Disable monitor mode on wireless interface (airmon-ng stop)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Monitor interface (e.g. wlan0mon)"},
            },
            "required": ["interface"],
        },
    },
    {
        "name": "airodump_scan",
        "description": "Scan & capture WiFi networks, clients, handshakes (airodump-ng)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Monitor interface"},
                "bssid": {"type": "string", "description": "Filter by AP BSSID"},
                "channel": {"type": "integer", "description": "Lock to channel"},
                "output_prefix": {"type": "string", "description": "Output file prefix"},
                "duration": {"type": "integer", "description": "Capture duration in seconds (default: 30)"},
                "band": {"type": "string", "description": "Band: a, b, g (default: bg)"},
            },
            "required": ["interface"],
        },
    },
    {
        "name": "aireplay_deauth",
        "description": "Send deauthentication packets to disconnect clients from AP",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Monitor interface"},
                "bssid": {"type": "string", "description": "Target AP BSSID"},
                "client": {"type": "string", "description": "Target client MAC (omit for broadcast)"},
                "count": {"type": "integer", "description": "Number of deauth packets (0=infinite, default: 10)"},
            },
            "required": ["interface", "bssid"],
        },
    },
    {
        "name": "aircrack_wpa",
        "description": "Crack WPA/WPA2 handshake using wordlist attack",
        "inputSchema": {
            "type": "object",
            "properties": {
                "capture_file": {"type": "string", "description": "Path to .cap file with handshake"},
                "wordlist": {"type": "string", "description": "Path to wordlist file"},
                "bssid": {"type": "string", "description": "Target BSSID"},
                "essid": {"type": "string", "description": "Target ESSID/network name"},
            },
            "required": ["capture_file", "wordlist"],
        },
    },
    {
        "name": "aircrack_wep",
        "description": "Crack WEP key from captured IVs",
        "inputSchema": {
            "type": "object",
            "properties": {
                "capture_file": {"type": "string", "description": "Path to .cap/.ivs file"},
                "bssid": {"type": "string", "description": "Target BSSID"},
                "key_length": {"type": "integer", "description": "Key length: 64 or 128 bits"},
            },
            "required": ["capture_file"],
        },
    },
    {
        "name": "wifite_auto",
        "description": "Automated WiFi auditing - cracks WPA/WPS/WEP automatically",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Wireless interface"},
                "target_bssid": {"type": "string", "description": "Target specific BSSID"},
                "kill_conflicting": {"type": "boolean", "description": "Kill conflicting processes"},
                "wpa_only": {"type": "boolean", "description": "Only attack WPA networks"},
                "wps_only": {"type": "boolean", "description": "Only attack WPS networks"},
                "wordlist": {"type": "string", "description": "Custom wordlist path"},
                "extra_args": {"type": "string", "description": "Additional wifite arguments"},
            },
            "required": [],
        },
    },
    {
        "name": "reaver_wps",
        "description": "WPS PIN brute-force attack against WPS-enabled routers",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Monitor interface"},
                "bssid": {"type": "string", "description": "Target AP BSSID"},
                "channel": {"type": "integer", "description": "AP channel"},
                "pixie_dust": {"type": "boolean", "description": "Use Pixie Dust attack (faster)"},
                "delay": {"type": "integer", "description": "Delay between PIN attempts (seconds)"},
                "verbose": {"type": "boolean", "description": "Verbose output"},
            },
            "required": ["interface", "bssid"],
        },
    },
    {
        "name": "wash_scan",
        "description": "Scan for WPS-enabled access points (wash)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Monitor interface"},
                "channel": {"type": "integer", "description": "Specific channel to scan"},
                "duration": {"type": "integer", "description": "Scan duration in seconds (default: 15)"},
            },
            "required": ["interface"],
        },
    },
    {
        "name": "bully_wps",
        "description": "WPS brute-force attack (alternative to Reaver, often more reliable)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Monitor interface"},
                "bssid": {"type": "string", "description": "Target AP BSSID"},
                "channel": {"type": "integer", "description": "AP channel"},
                "pixie_dust": {"type": "boolean", "description": "Use Pixie Dust attack"},
                "force": {"type": "boolean", "description": "Force attack even if AP is locked"},
            },
            "required": ["interface", "bssid"],
        },
    },
    {
        "name": "bettercap_wifi",
        "description": "WiFi reconnaissance & deauth attacks via bettercap",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Wireless interface"},
                "command": {"type": "string", "description": "Bettercap caplet or command string"},
                "recon": {"type": "boolean", "description": "Run wifi.recon (discover networks)"},
                "deauth": {"type": "string", "description": "BSSID to deauth"},
                "extra_args": {"type": "string", "description": "Additional bettercap arguments"},
            },
            "required": ["interface"],
        },
    },
    {
        "name": "bettercap_ble",
        "description": "Bluetooth Low Energy scanning & enumeration via bettercap",
        "inputSchema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "BLE command (ble.recon, ble.enum, etc.)"},
                "target": {"type": "string", "description": "Target BLE device MAC address"},
                "duration": {"type": "integer", "description": "Scan duration in seconds"},
            },
            "required": [],
        },
    },
    {
        "name": "kismet_scan",
        "description": "Passive wireless monitoring - WiFi, Bluetooth, RF (kismet)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Capture source (e.g. wlan0)"},
                "log_prefix": {"type": "string", "description": "Log file prefix"},
                "filter": {"type": "string", "description": "Device filter expression"},
                "duration": {"type": "integer", "description": "Capture duration in seconds"},
            },
            "required": ["source"],
        },
    },
    {
        "name": "cowpatty_crack",
        "description": "WPA-PSK cracking using precomputed PMK rainbow tables (cowpatty)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "capture_file": {"type": "string", "description": "Path to .cap file"},
                "wordlist": {"type": "string", "description": "Wordlist or PMK hash file"},
                "essid": {"type": "string", "description": "Target ESSID"},
                "use_hash": {"type": "boolean", "description": "Use pre-computed PMK hashes"},
            },
            "required": ["capture_file", "essid"],
        },
    },
    {
        "name": "wifipumpkin3_rogueap",
        "description": "Rogue AP / Evil Twin attack framework (wifipumpkin3)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Wireless interface for AP"},
                "ssid": {"type": "string", "description": "Fake AP SSID to broadcast"},
                "channel": {"type": "integer", "description": "WiFi channel"},
                "proxy": {"type": "string", "description": "Proxy plugin (captiveflask, beef, etc.)"},
                "extra_args": {"type": "string", "description": "Additional arguments"},
            },
            "required": ["interface", "ssid"],
        },
    },
    {
        "name": "airgeddon_menu",
        "description": "Interactive wireless audit framework with automated attacks",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Wireless interface"},
                "script": {"type": "string", "description": "Airgeddon script/command to execute"},
                "extra_args": {"type": "string", "description": "Additional arguments"},
            },
            "required": ["interface"],
        },
    },
]


async def dispatch_tool(name: str, args: Dict) -> str:
    if name == "airmon_start":
        cmd = [_find_tool("airmon-ng"), "start", args["interface"]]
        if args.get("channel"):
            cmd.append(str(args["channel"]))
        r = _run_tool(cmd, timeout=30)
        return json.dumps(r, indent=2)

    elif name == "airmon_stop":
        cmd = [_find_tool("airmon-ng"), "stop", args["interface"]]
        r = _run_tool(cmd, timeout=30)
        return json.dumps(r, indent=2)

    elif name == "airodump_scan":
        cmd = [_find_tool("airodump-ng"), args["interface"]]
        if args.get("bssid"):
            cmd.extend(["--bssid", args["bssid"]])
        if args.get("channel"):
            cmd.extend(["-c", str(args["channel"])])
        if args.get("output_prefix"):
            cmd.extend(["-w", args["output_prefix"]])
        if args.get("band"):
            cmd.extend(["--band", args["band"]])
        duration = args.get("duration", 30)
        r = _run_tool(cmd, timeout=duration + 10)
        return json.dumps(r, indent=2)

    elif name == "aireplay_deauth":
        count = args.get("count", 10)
        cmd = [_find_tool("aireplay-ng"), "--deauth", str(count), "-a", args["bssid"]]
        if args.get("client"):
            cmd.extend(["-c", args["client"]])
        cmd.append(args["interface"])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "aircrack_wpa":
        cmd = [_find_tool("aircrack-ng"), "-w", args["wordlist"], args["capture_file"]]
        if args.get("bssid"):
            cmd.extend(["-b", args["bssid"]])
        if args.get("essid"):
            cmd.extend(["-e", args["essid"]])
        r = _run_tool(cmd, timeout=3600)
        return json.dumps(r, indent=2)

    elif name == "aircrack_wep":
        cmd = [_find_tool("aircrack-ng"), args["capture_file"]]
        if args.get("bssid"):
            cmd.extend(["-b", args["bssid"]])
        if args.get("key_length"):
            cmd.extend(["-n", str(args["key_length"])])
        r = _run_tool(cmd, timeout=1800)
        return json.dumps(r, indent=2)

    elif name == "wifite_auto":
        cmd = [_find_tool("wifite")]
        if args.get("interface"):
            cmd.extend(["-i", args["interface"]])
        if args.get("target_bssid"):
            cmd.extend(["--bssid", args["target_bssid"]])
        if args.get("kill_conflicting"):
            cmd.append("--kill")
        if args.get("wpa_only"):
            cmd.append("--wpa")
        if args.get("wps_only"):
            cmd.append("--wps")
        if args.get("wordlist"):
            cmd.extend(["--dict", args["wordlist"]])
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=3600)
        return json.dumps(r, indent=2)

    elif name == "reaver_wps":
        cmd = [_find_tool("reaver"), "-i", args["interface"], "-b", args["bssid"]]
        if args.get("channel"):
            cmd.extend(["-c", str(args["channel"])])
        if args.get("pixie_dust"):
            cmd.extend(["-K", "1"])
        if args.get("delay"):
            cmd.extend(["-d", str(args["delay"])])
        if args.get("verbose"):
            cmd.append("-vv")
        r = _run_tool(cmd, timeout=3600)
        return json.dumps(r, indent=2)

    elif name == "wash_scan":
        cmd = [_find_tool("wash"), "-i", args["interface"]]
        if args.get("channel"):
            cmd.extend(["-c", str(args["channel"])])
        duration = args.get("duration", 15)
        r = _run_tool(cmd, timeout=duration + 10)
        return json.dumps(r, indent=2)

    elif name == "bully_wps":
        cmd = [_find_tool("bully"), args["interface"], "-b", args["bssid"]]
        if args.get("channel"):
            cmd.extend(["-c", str(args["channel"])])
        if args.get("pixie_dust"):
            cmd.extend(["-d"])
        if args.get("force"):
            cmd.append("-F")
        r = _run_tool(cmd, timeout=3600)
        return json.dumps(r, indent=2)

    elif name == "bettercap_wifi":
        cmd = [_find_tool("bettercap"), "-iface", args["interface"]]
        if args.get("command"):
            cmd.extend(["-eval", args["command"]])
        elif args.get("recon"):
            cmd.extend(["-eval", "wifi.recon on; sleep 10; wifi.show; quit"])
        elif args.get("deauth"):
            cmd.extend(["-eval", f"wifi.recon on; sleep 3; wifi.deauth {args['deauth']}; quit"])
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "bettercap_ble":
        cmd = [_find_tool("bettercap")]
        if args.get("command"):
            cmd.extend(["-eval", args["command"]])
        elif args.get("target"):
            cmd.extend(["-eval", f"ble.recon on; sleep 5; ble.enum {args['target']}; quit"])
        else:
            dur = args.get("duration", 10)
            cmd.extend(["-eval", f"ble.recon on; sleep {dur}; ble.show; quit"])
        r = _run_tool(cmd, timeout=args.get("duration", 30) + 15)
        return json.dumps(r, indent=2)

    elif name == "kismet_scan":
        cmd = [_find_tool("kismet"), "-c", args["source"], "--no-ncurses"]
        if args.get("log_prefix"):
            cmd.extend(["--log-prefix", args["log_prefix"]])
        if args.get("filter"):
            cmd.extend(["--filter", args["filter"]])
        duration = args.get("duration", 30)
        r = _run_tool(cmd, timeout=duration + 15)
        return json.dumps(r, indent=2)

    elif name == "cowpatty_crack":
        cmd = [_find_tool("cowpatty"), "-r", args["capture_file"], "-s", args["essid"]]
        if args.get("use_hash") and args.get("wordlist"):
            cmd.extend(["-d", args["wordlist"]])
        elif args.get("wordlist"):
            cmd.extend(["-f", args["wordlist"]])
        r = _run_tool(cmd, timeout=3600)
        return json.dumps(r, indent=2)

    elif name == "wifipumpkin3_rogueap":
        cmd = [_find_tool("wifipumpkin3"), "--interface", args["interface"], "--ssid", args["ssid"]]
        if args.get("channel"):
            cmd.extend(["--channel", str(args["channel"])])
        if args.get("proxy"):
            cmd.extend(["--proxy", args["proxy"]])
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "airgeddon_menu":
        cmd = [_find_tool("airgeddon")]
        if args.get("script"):
            cmd.extend(args["script"].split())
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
