#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP Network Attack Server v1.0.0

    Network-level attacks: MITM, ARP poisoning, DNS spoofing, sniffing.
    Integrates: bettercap, ettercap, hping3, arp-scan, netdiscover,
                mitm6, sslscan, tcpdump, socat, snort, dnschef, sslstrip.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (16):
        - bettercap_mitm: MITM attack with ARP spoofing & packet capture
        - bettercap_sniff: Network sniffer with protocol parsing
        - bettercap_dns_spoof: DNS spoofing via bettercap
        - ettercap_mitm: ARP poisoning MITM with ettercap
        - ettercap_filter: Apply ettercap etterfilter for traffic modification
        - hping3_flood: TCP/UDP/ICMP flood testing (hping3)
        - hping3_scan: Advanced port scanning with custom packets
        - arp_scan: Fast ARP-based host discovery on local network
        - netdiscover_scan: Passive/active ARP network discovery
        - mitm6_attack: IPv6 MITM attack for WPAD/DNS takeover
        - sslscan_audit: SSL/TLS configuration audit
        - tcpdump_capture: Packet capture & filtering (tcpdump)
        - socat_relay: Network relay/proxy/forwarder (socat)
        - snort_ids: Intrusion detection with Snort IDS rules
        - dnschef_spoof: DNS proxy/spoofing server
        - sslstrip_mitm: SSL stripping MITM attack

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
logger = logging.getLogger("leviathan-netattack-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-netattack-server"


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
        "name": "bettercap_mitm",
        "description": "MITM attack with ARP spoofing, packet sniffing & injection via bettercap",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Network interface"},
                "target": {"type": "string", "description": "Target IP (omit for whole subnet)"},
                "gateway": {"type": "string", "description": "Gateway IP"},
                "caplet": {"type": "string", "description": "Bettercap caplet file or inline commands"},
                "sniffer": {"type": "boolean", "description": "Enable packet sniffer"},
                "proxy": {"type": "boolean", "description": "Enable HTTP proxy"},
                "extra_args": {"type": "string", "description": "Additional bettercap arguments"},
            },
            "required": ["interface"],
        },
    },
    {
        "name": "bettercap_sniff",
        "description": "Network traffic sniffer with protocol parsing via bettercap",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Network interface"},
                "filter": {"type": "string", "description": "BPF filter expression"},
                "output": {"type": "string", "description": "PCAP output file"},
                "duration": {"type": "integer", "description": "Capture duration in seconds"},
                "verbose": {"type": "boolean", "description": "Verbose output with packet details"},
            },
            "required": ["interface"],
        },
    },
    {
        "name": "bettercap_dns_spoof",
        "description": "DNS spoofing via bettercap - redirect domains to attacker IP",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Network interface"},
                "domain": {"type": "string", "description": "Domain to spoof (or * for all)"},
                "address": {"type": "string", "description": "IP to resolve spoofed domains to"},
                "target": {"type": "string", "description": "Target IP for ARP poisoning"},
            },
            "required": ["interface", "domain", "address"],
        },
    },
    {
        "name": "ettercap_mitm",
        "description": "ARP poisoning MITM attack with ettercap",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Network interface"},
                "target1": {"type": "string", "description": "Target 1 IP (e.g. victim)"},
                "target2": {"type": "string", "description": "Target 2 IP (e.g. gateway)"},
                "text_mode": {"type": "boolean", "description": "Text-only mode (no GUI)"},
                "filter_file": {"type": "string", "description": "Compiled etterfilter file"},
                "output_file": {"type": "string", "description": "Output pcap file"},
                "quiet": {"type": "boolean", "description": "Quiet mode"},
            },
            "required": ["interface"],
        },
    },
    {
        "name": "ettercap_filter",
        "description": "Compile and apply traffic modification filters for ettercap",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source_file": {"type": "string", "description": "Etterfilter source file (.ef)"},
                "output_file": {"type": "string", "description": "Compiled filter output (.efc)"},
            },
            "required": ["source_file"],
        },
    },
    {
        "name": "hping3_flood",
        "description": "TCP/UDP/ICMP flood testing for stress testing (hping3)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target IP address"},
                "port": {"type": "integer", "description": "Target port"},
                "flood": {"type": "boolean", "description": "Flood mode (max speed)"},
                "syn": {"type": "boolean", "description": "SYN flood"},
                "udp": {"type": "boolean", "description": "UDP mode"},
                "icmp": {"type": "boolean", "description": "ICMP mode"},
                "count": {"type": "integer", "description": "Number of packets to send"},
                "data_size": {"type": "integer", "description": "Data payload size in bytes"},
                "spoof": {"type": "string", "description": "Source IP to spoof"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "hping3_scan",
        "description": "Advanced port scanning with custom TCP/IP packets (hping3)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target IP address"},
                "scan_type": {"type": "string", "description": "Scan: SYN, ACK, FIN, XMAS, NULL, UDP"},
                "ports": {"type": "string", "description": "Port range (e.g. 1-1000 or 80,443)"},
                "count": {"type": "integer", "description": "Packets per port"},
                "interface": {"type": "string", "description": "Network interface"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "arp_scan",
        "description": "Fast ARP-based host discovery on local network",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target network (e.g. 192.168.1.0/24) or -l for local"},
                "interface": {"type": "string", "description": "Network interface"},
                "localnet": {"type": "boolean", "description": "Scan local network (auto-detect)"},
            },
            "required": [],
        },
    },
    {
        "name": "netdiscover_scan",
        "description": "Passive or active ARP network discovery (netdiscover)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "range": {"type": "string", "description": "IP range (e.g. 192.168.1.0/24)"},
                "interface": {"type": "string", "description": "Network interface"},
                "passive": {"type": "boolean", "description": "Passive mode (sniff only, no packets sent)"},
                "count": {"type": "integer", "description": "Number of ARP requests per IP"},
            },
            "required": [],
        },
    },
    {
        "name": "mitm6_attack",
        "description": "IPv6 MITM attack - WPAD and DNS takeover via mitm6",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target domain"},
                "interface": {"type": "string", "description": "Network interface"},
                "relay_target": {"type": "string", "description": "Target for NTLM relay (ntlmrelayx)"},
                "extra_args": {"type": "string", "description": "Additional mitm6 arguments"},
            },
            "required": ["domain"],
        },
    },
    {
        "name": "sslscan_audit",
        "description": "SSL/TLS vulnerability and configuration audit (sslscan)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target host:port (e.g. example.com:443)"},
                "show_certs": {"type": "boolean", "description": "Show full certificate details"},
                "no_color": {"type": "boolean", "description": "Disable colored output"},
                "xml_output": {"type": "string", "description": "XML output file path"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "tcpdump_capture",
        "description": "Network packet capture and filtering (tcpdump)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Network interface"},
                "filter": {"type": "string", "description": "BPF filter (e.g. 'port 80', 'host 10.0.0.1')"},
                "output_file": {"type": "string", "description": "Output pcap file"},
                "count": {"type": "integer", "description": "Number of packets to capture"},
                "verbose": {"type": "boolean", "description": "Verbose output (-v)"},
                "hex_dump": {"type": "boolean", "description": "Show hex dump (-X)"},
            },
            "required": ["interface"],
        },
    },
    {
        "name": "socat_relay",
        "description": "Network relay, proxy, and port forwarder (socat)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Source address spec (e.g. TCP-LISTEN:8080,fork)"},
                "dest": {"type": "string", "description": "Destination address spec (e.g. TCP:target:80)"},
                "verbose": {"type": "boolean", "description": "Verbose mode (-v)"},
            },
            "required": ["source", "dest"],
        },
    },
    {
        "name": "snort_ids",
        "description": "Intrusion detection using Snort IDS engine with custom rules",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Network interface to monitor"},
                "config": {"type": "string", "description": "Snort config file path"},
                "rules": {"type": "string", "description": "Custom rules file path"},
                "pcap": {"type": "string", "description": "PCAP file to analyze (offline mode)"},
                "log_dir": {"type": "string", "description": "Log directory"},
                "alert_mode": {"type": "string", "description": "Alert mode: fast, full, console, none"},
            },
            "required": [],
        },
    },
    {
        "name": "dnschef_spoof",
        "description": "DNS proxy and spoofing server (dnschef)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Listen interface IP"},
                "fakeip": {"type": "string", "description": "Fake IP to respond with"},
                "fakedomains": {"type": "string", "description": "Domains to spoof (comma-separated)"},
                "truedomains": {"type": "string", "description": "Domains to resolve truthfully"},
                "nameservers": {"type": "string", "description": "Upstream DNS servers"},
            },
            "required": [],
        },
    },
    {
        "name": "sslstrip_mitm",
        "description": "SSL stripping attack - downgrade HTTPS to HTTP (sslstrip)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "listen_port": {"type": "integer", "description": "Listen port (default: 10000)"},
                "favicon": {"type": "boolean", "description": "Substitute lock favicon"},
                "killsessions": {"type": "boolean", "description": "Kill existing sessions"},
                "log_file": {"type": "string", "description": "Log file path"},
            },
            "required": [],
        },
    },
]


async def dispatch_tool(name: str, args: Dict) -> str:
    if name == "bettercap_mitm":
        cmd = [_find_tool("bettercap"), "-iface", args["interface"]]
        eval_parts = ["net.probe on"]
        if args.get("target"):
            eval_parts.append(f"set arp.spoof.targets {args['target']}")
        eval_parts.append("arp.spoof on")
        if args.get("sniffer"):
            eval_parts.append("net.sniff on")
        if args.get("proxy"):
            eval_parts.append("http.proxy on")
        if args.get("caplet"):
            cmd.extend(["-caplet", args["caplet"]])
        else:
            cmd.extend(["-eval", "; ".join(eval_parts)])
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "bettercap_sniff":
        cmd = [_find_tool("bettercap"), "-iface", args["interface"]]
        eval_parts = ["net.sniff on"]
        if args.get("filter"):
            eval_parts.insert(0, f"set net.sniff.filter {args['filter']}")
        if args.get("output"):
            eval_parts.insert(0, f"set net.sniff.output {args['output']}")
        if args.get("verbose"):
            eval_parts.insert(0, "set net.sniff.verbose true")
        dur = args.get("duration", 30)
        eval_parts.append(f"sleep {dur}")
        eval_parts.append("quit")
        cmd.extend(["-eval", "; ".join(eval_parts)])
        r = _run_tool(cmd, timeout=dur + 30)
        return json.dumps(r, indent=2)

    elif name == "bettercap_dns_spoof":
        cmd = [_find_tool("bettercap"), "-iface", args["interface"]]
        eval_parts = [
            f"set dns.spoof.domains {args['domain']}",
            f"set dns.spoof.address {args['address']}",
            "dns.spoof on",
        ]
        if args.get("target"):
            eval_parts.insert(0, f"set arp.spoof.targets {args['target']}")
            eval_parts.insert(1, "arp.spoof on")
        cmd.extend(["-eval", "; ".join(eval_parts)])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "ettercap_mitm":
        cmd = [_find_tool("ettercap")]
        if args.get("text_mode", True):
            cmd.append("-T")
        if args.get("quiet"):
            cmd.append("-q")
        cmd.extend(["-i", args["interface"], "-M", "arp"])
        if args.get("target1") and args.get("target2"):
            cmd.append(f"/{args['target1']}// /{args['target2']}//")
        if args.get("filter_file"):
            cmd.extend(["-F", args["filter_file"]])
        if args.get("output_file"):
            cmd.extend(["-w", args["output_file"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "ettercap_filter":
        output = args.get("output_file", args["source_file"].replace(".ef", ".efc"))
        cmd = [_find_tool("etterfilter"), args["source_file"], "-o", output]
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "hping3_flood":
        cmd = [_find_tool("hping3"), args["target"]]
        if args.get("port"):
            cmd.extend(["-p", str(args["port"])])
        if args.get("flood"):
            cmd.append("--flood")
        if args.get("syn"):
            cmd.append("-S")
        if args.get("udp"):
            cmd.append("--udp")
        if args.get("icmp"):
            cmd.append("--icmp")
        if args.get("count"):
            cmd.extend(["-c", str(args["count"])])
        if args.get("data_size"):
            cmd.extend(["-d", str(args["data_size"])])
        if args.get("spoof"):
            cmd.extend(["-a", args["spoof"]])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "hping3_scan":
        cmd = [_find_tool("hping3"), args["target"]]
        st = args.get("scan_type", "SYN").upper()
        if st == "SYN":
            cmd.append("-S")
        elif st == "ACK":
            cmd.append("-A")
        elif st == "FIN":
            cmd.append("-F")
        elif st == "XMAS":
            cmd.extend(["-F", "-P", "-U"])
        elif st == "NULL":
            pass
        elif st == "UDP":
            cmd.append("--udp")
        if args.get("ports"):
            cmd.extend(["--scan", args["ports"]])
        if args.get("count"):
            cmd.extend(["-c", str(args["count"])])
        if args.get("interface"):
            cmd.extend(["-I", args["interface"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "arp_scan":
        cmd = [_find_tool("arp-scan")]
        if args.get("localnet"):
            cmd.append("--localnet")
        elif args.get("target"):
            cmd.append(args["target"])
        else:
            cmd.append("--localnet")
        if args.get("interface"):
            cmd.extend(["-I", args["interface"]])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "netdiscover_scan":
        cmd = [_find_tool("netdiscover")]
        if args.get("passive"):
            cmd.append("-p")
        if args.get("range"):
            cmd.extend(["-r", args["range"]])
        if args.get("interface"):
            cmd.extend(["-i", args["interface"]])
        if args.get("count"):
            cmd.extend(["-c", str(args["count"])])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "mitm6_attack":
        cmd = [_find_tool("mitm6"), "-d", args["domain"]]
        if args.get("interface"):
            cmd.extend(["-i", args["interface"]])
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "sslscan_audit":
        cmd = [_find_tool("sslscan")]
        if args.get("show_certs"):
            cmd.append("--show-certificate")
        if args.get("no_color"):
            cmd.append("--no-colour")
        if args.get("xml_output"):
            cmd.extend(["--xml", args["xml_output"]])
        cmd.append(args["target"])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "tcpdump_capture":
        cmd = [_find_tool("tcpdump"), "-i", args["interface"]]
        if args.get("filter"):
            cmd.extend(args["filter"].split())
        if args.get("output_file"):
            cmd.extend(["-w", args["output_file"]])
        if args.get("count"):
            cmd.extend(["-c", str(args["count"])])
        if args.get("verbose"):
            cmd.append("-v")
        if args.get("hex_dump"):
            cmd.append("-X")
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "socat_relay":
        cmd = [_find_tool("socat")]
        if args.get("verbose"):
            cmd.append("-v")
        cmd.extend([args["source"], args["dest"]])
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "snort_ids":
        cmd = [_find_tool("snort")]
        if args.get("pcap"):
            cmd.extend(["-r", args["pcap"]])
        elif args.get("interface"):
            cmd.extend(["-i", args["interface"]])
        if args.get("config"):
            cmd.extend(["-c", args["config"]])
        if args.get("rules"):
            cmd.extend(["--rule", args["rules"]])
        if args.get("log_dir"):
            cmd.extend(["-l", args["log_dir"]])
        if args.get("alert_mode"):
            cmd.extend(["-A", args["alert_mode"]])
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "dnschef_spoof":
        cmd = [_find_tool("dnschef")]
        if args.get("interface"):
            cmd.extend(["--interface", args["interface"]])
        if args.get("fakeip"):
            cmd.extend(["--fakeip", args["fakeip"]])
        if args.get("fakedomains"):
            cmd.extend(["--fakedomains", args["fakedomains"]])
        if args.get("truedomains"):
            cmd.extend(["--truedomains", args["truedomains"]])
        if args.get("nameservers"):
            cmd.extend(["--nameservers", args["nameservers"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "sslstrip_mitm":
        cmd = [_find_tool("sslstrip")]
        if args.get("listen_port"):
            cmd.extend(["-l", str(args["listen_port"])])
        if args.get("favicon"):
            cmd.append("-f")
        if args.get("killsessions"):
            cmd.append("-k")
        if args.get("log_file"):
            cmd.extend(["-w", args["log_file"]])
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
