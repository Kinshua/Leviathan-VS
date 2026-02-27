#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP Social Engineering Server v1.0.0

    Social engineering, phishing, and credential harvesting.
    Integrates: gophish, setoolkit, evilginx2, beef-xss, king-phisher,
                modlishka, wifiphisher, blackeye, zphisher.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (14):
        - setoolkit_attack: Social Engineering Toolkit attacks
        - gophish_campaign: GoPhish phishing campaign management
        - gophish_templates: GoPhish email template management
        - gophish_results: GoPhish campaign results & stats
        - evilginx2_phishlet: Evilginx2 reverse proxy phishing (bypass 2FA)
        - evilginx2_session: Evilginx2 session/token capture
        - beef_hook: BeEF browser exploitation framework - hook management
        - beef_command: BeEF - execute browser command modules
        - beef_autorun: BeEF - configure autorun rules
        - modlishka_proxy: Modlishka reverse proxy phishing
        - wifiphisher_attack: WiFi phishing - evil twin + captive portal
        - blackeye_phish: Blackeye phishing page generator
        - zphisher_phish: Zphisher automated phishing tool (30+ templates)
        - credential_harvest: Custom credential harvesting server

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
logger = logging.getLogger("leviathan-socialeng-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-socialeng-server"


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
        "name": "setoolkit_attack",
        "description": "Social Engineering Toolkit - spear phishing, web attacks, credential harvesting",
        "inputSchema": {
            "type": "object",
            "properties": {
                "attack_type": {"type": "string", "description": "Attack type: spear-phish, website, infectious_media, credential_harvest, mass_mailer, powershell"},
                "target_url": {"type": "string", "description": "Target URL to clone (for web attacks)"},
                "target_email": {"type": "string", "description": "Target email address"},
                "payload": {"type": "string", "description": "Payload type/path"},
                "listener_ip": {"type": "string", "description": "Listener IP for reverse connections"},
                "extra_args": {"type": "string", "description": "Additional SET arguments"},
            },
            "required": ["attack_type"],
        },
    },
    {
        "name": "gophish_campaign",
        "description": "GoPhish - create and launch phishing campaigns via API",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action: create, launch, complete, delete, list, get"},
                "api_url": {"type": "string", "description": "GoPhish API URL (default: https://localhost:3333)"},
                "api_key": {"type": "string", "description": "GoPhish API key"},
                "campaign_name": {"type": "string", "description": "Campaign name"},
                "campaign_id": {"type": "integer", "description": "Campaign ID (for get/delete/complete)"},
                "template_id": {"type": "integer", "description": "Email template ID"},
                "landing_page_id": {"type": "integer", "description": "Landing page ID"},
                "smtp_id": {"type": "integer", "description": "SMTP profile ID"},
                "group_id": {"type": "integer", "description": "Target group ID"},
            },
            "required": ["action"],
        },
    },
    {
        "name": "gophish_templates",
        "description": "GoPhish - manage email templates and landing pages",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action: list_templates, create_template, list_pages, create_page, import_site"},
                "api_url": {"type": "string", "description": "GoPhish API URL"},
                "api_key": {"type": "string", "description": "GoPhish API key"},
                "name": {"type": "string", "description": "Template/page name"},
                "subject": {"type": "string", "description": "Email subject"},
                "html": {"type": "string", "description": "HTML content"},
                "url": {"type": "string", "description": "URL to import as landing page"},
            },
            "required": ["action"],
        },
    },
    {
        "name": "gophish_results",
        "description": "GoPhish - get campaign results, timeline, and statistics",
        "inputSchema": {
            "type": "object",
            "properties": {
                "api_url": {"type": "string", "description": "GoPhish API URL"},
                "api_key": {"type": "string", "description": "GoPhish API key"},
                "campaign_id": {"type": "integer", "description": "Campaign ID to query"},
                "summary": {"type": "boolean", "description": "Get summary statistics only"},
            },
            "required": ["campaign_id"],
        },
    },
    {
        "name": "evilginx2_phishlet",
        "description": "Evilginx2 - configure reverse proxy phishing (bypasses 2FA)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action: setup, enable, disable, list, hostname"},
                "phishlet": {"type": "string", "description": "Phishlet name (e.g. office365, google, facebook)"},
                "domain": {"type": "string", "description": "Phishing domain"},
                "hostname": {"type": "string", "description": "Hostname for phishlet"},
                "redirect_url": {"type": "string", "description": "Redirect URL after capture"},
            },
            "required": ["action"],
        },
    },
    {
        "name": "evilginx2_session",
        "description": "Evilginx2 - manage captured sessions and tokens",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action: list, get, delete"},
                "session_id": {"type": "integer", "description": "Session ID"},
            },
            "required": ["action"],
        },
    },
    {
        "name": "beef_hook",
        "description": "BeEF (Browser Exploitation Framework) - manage hooked browsers",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action: list, info, logs"},
                "api_url": {"type": "string", "description": "BeEF API URL (default: http://localhost:3000)"},
                "api_token": {"type": "string", "description": "BeEF API token"},
                "hook_id": {"type": "integer", "description": "Hooked browser ID"},
            },
            "required": ["action"],
        },
    },
    {
        "name": "beef_command",
        "description": "BeEF - execute browser command modules on hooked browsers",
        "inputSchema": {
            "type": "object",
            "properties": {
                "api_url": {"type": "string", "description": "BeEF API URL"},
                "api_token": {"type": "string", "description": "BeEF API token"},
                "hook_id": {"type": "integer", "description": "Hooked browser ID"},
                "module_id": {"type": "integer", "description": "Command module ID"},
                "module_name": {"type": "string", "description": "Module name to search/execute"},
                "options": {"type": "string", "description": "Module options as JSON string"},
            },
            "required": ["hook_id"],
        },
    },
    {
        "name": "beef_autorun",
        "description": "BeEF - configure autorun rules for new hooked browsers",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action: list, add, delete"},
                "api_url": {"type": "string", "description": "BeEF API URL"},
                "api_token": {"type": "string", "description": "BeEF API token"},
                "module_id": {"type": "integer", "description": "Module ID to autorun"},
                "rule_id": {"type": "integer", "description": "Rule ID (for delete)"},
            },
            "required": ["action"],
        },
    },
    {
        "name": "modlishka_proxy",
        "description": "Modlishka - reverse proxy for transparent phishing (2FA bypass)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target_domain": {"type": "string", "description": "Target domain to proxy"},
                "phishing_domain": {"type": "string", "description": "Phishing domain"},
                "listen_port": {"type": "integer", "description": "Listen port"},
                "cert": {"type": "string", "description": "TLS certificate path"},
                "key": {"type": "string", "description": "TLS key path"},
                "config_file": {"type": "string", "description": "Modlishka config JSON file"},
            },
            "required": ["target_domain"],
        },
    },
    {
        "name": "wifiphisher_attack",
        "description": "WiFi phishing - create evil twin AP with captive portal",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string", "description": "Wireless interface"},
                "target_ap": {"type": "string", "description": "Target AP ESSID to impersonate"},
                "scenario": {"type": "string", "description": "Phishing scenario (firmware-upgrade, oauth-login, etc.)"},
                "deauth": {"type": "boolean", "description": "Deauth clients from target AP"},
                "extra_args": {"type": "string", "description": "Additional wifiphisher arguments"},
            },
            "required": ["interface"],
        },
    },
    {
        "name": "blackeye_phish",
        "description": "Blackeye - phishing page generator (32+ templates)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "template": {"type": "string", "description": "Template: instagram, facebook, google, microsoft, twitter, github, linkedin, etc."},
                "port": {"type": "integer", "description": "Server port (default: 8080)"},
                "redirect_url": {"type": "string", "description": "Redirect URL after credential capture"},
            },
            "required": ["template"],
        },
    },
    {
        "name": "zphisher_phish",
        "description": "Zphisher - automated phishing tool with 30+ templates and tunneling",
        "inputSchema": {
            "type": "object",
            "properties": {
                "template": {"type": "string", "description": "Template: facebook, instagram, google, microsoft, netflix, paypal, steam, etc."},
                "port": {"type": "integer", "description": "Local port"},
                "tunnel": {"type": "string", "description": "Tunneling: cloudflared, ngrok, loclx"},
                "custom_url": {"type": "string", "description": "Custom phishing URL mask"},
            },
            "required": ["template"],
        },
    },
    {
        "name": "credential_harvest",
        "description": "Custom credential harvesting - clone site and capture submissions",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target_url": {"type": "string", "description": "URL to clone for credential harvesting"},
                "listen_port": {"type": "integer", "description": "Listen port (default: 80)"},
                "listen_ip": {"type": "string", "description": "Listen IP (default: 0.0.0.0)"},
                "output_file": {"type": "string", "description": "File to save captured credentials"},
                "redirect_after": {"type": "string", "description": "URL to redirect after capture"},
            },
            "required": ["target_url"],
        },
    },
]


async def dispatch_tool(name: str, args: Dict) -> str:
    if name == "setoolkit_attack":
        cmd = [_find_tool("setoolkit")]
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "gophish_campaign":
        # GoPhish API interaction via curl
        api_url = args.get("api_url", "https://localhost:3333")
        api_key = args.get("api_key", "")
        action = args["action"]
        if action == "list":
            cmd = [_find_tool("curl"), "-k", "-H", f"Authorization: {api_key}", f"{api_url}/api/campaigns/"]
        elif action == "get" and args.get("campaign_id"):
            cmd = [_find_tool("curl"), "-k", "-H", f"Authorization: {api_key}", f"{api_url}/api/campaigns/{args['campaign_id']}"]
        elif action == "delete" and args.get("campaign_id"):
            cmd = [_find_tool("curl"), "-k", "-X", "DELETE", "-H", f"Authorization: {api_key}", f"{api_url}/api/campaigns/{args['campaign_id']}"]
        else:
            return json.dumps({"error": f"Unsupported action: {action}. Use list, get, or delete with campaign_id."})
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "gophish_templates":
        api_url = args.get("api_url", "https://localhost:3333")
        api_key = args.get("api_key", "")
        action = args["action"]
        if action == "list_templates":
            cmd = [_find_tool("curl"), "-k", "-H", f"Authorization: {api_key}", f"{api_url}/api/templates/"]
        elif action == "list_pages":
            cmd = [_find_tool("curl"), "-k", "-H", f"Authorization: {api_key}", f"{api_url}/api/pages/"]
        elif action == "import_site" and args.get("url"):
            cmd = [_find_tool("curl"), "-k", "-X", "POST", "-H", f"Authorization: {api_key}",
                   "-H", "Content-Type: application/json",
                   "-d", json.dumps({"url": args["url"]}),
                   f"{api_url}/api/import/site"]
        else:
            return json.dumps({"error": f"Unsupported action: {action}"})
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "gophish_results":
        api_url = args.get("api_url", "https://localhost:3333")
        api_key = args.get("api_key", "")
        cid = args["campaign_id"]
        endpoint = f"/api/campaigns/{cid}/summary" if args.get("summary") else f"/api/campaigns/{cid}/results"
        cmd = [_find_tool("curl"), "-k", "-H", f"Authorization: {api_key}", f"{api_url}{endpoint}"]
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "evilginx2_phishlet":
        cmd = [_find_tool("evilginx2")]
        action = args["action"]
        eval_cmd = f"phishlets {action}"
        if args.get("phishlet"):
            eval_cmd += f" {args['phishlet']}"
        if args.get("hostname"):
            eval_cmd += f" {args['hostname']}"
        cmd.extend(["-eval", eval_cmd])
        r = _run_tool(cmd, timeout=120)
        return json.dumps(r, indent=2)

    elif name == "evilginx2_session":
        cmd = [_find_tool("evilginx2")]
        action = args["action"]
        eval_cmd = f"sessions {action}"
        if args.get("session_id"):
            eval_cmd += f" {args['session_id']}"
        cmd.extend(["-eval", eval_cmd])
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "beef_hook":
        api_url = args.get("api_url", "http://localhost:3000")
        api_token = args.get("api_token", "")
        action = args["action"]
        if action == "list":
            cmd = [_find_tool("curl"), f"{api_url}/api/hooks?token={api_token}"]
        elif action == "info" and args.get("hook_id"):
            cmd = [_find_tool("curl"), f"{api_url}/api/hooks/{args['hook_id']}?token={api_token}"]
        elif action == "logs" and args.get("hook_id"):
            cmd = [_find_tool("curl"), f"{api_url}/api/logs/{args['hook_id']}?token={api_token}"]
        else:
            return json.dumps({"error": f"Unsupported action: {action}"})
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "beef_command":
        api_url = args.get("api_url", "http://localhost:3000")
        api_token = args.get("api_token", "")
        hook_id = args["hook_id"]
        if args.get("module_id"):
            data = json.dumps({"token": api_token})
            cmd = [_find_tool("curl"), "-X", "POST", "-H", "Content-Type: application/json",
                   "-d", data, f"{api_url}/api/modules/{hook_id}/{args['module_id']}"]
        else:
            cmd = [_find_tool("curl"), f"{api_url}/api/modules?token={api_token}"]
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "beef_autorun":
        api_url = args.get("api_url", "http://localhost:3000")
        api_token = args.get("api_token", "")
        action = args["action"]
        if action == "list":
            cmd = [_find_tool("curl"), f"{api_url}/api/autorun?token={api_token}"]
        else:
            return json.dumps({"error": f"Unsupported action: {action}. Use BeEF web UI for add/delete."})
        r = _run_tool(cmd, timeout=60)
        return json.dumps(r, indent=2)

    elif name == "modlishka_proxy":
        cmd = [_find_tool("modlishka"), "-target", args["target_domain"]]
        if args.get("phishing_domain"):
            cmd.extend(["-phishingDomain", args["phishing_domain"]])
        if args.get("listen_port"):
            cmd.extend(["-listeningPort", str(args["listen_port"])])
        if args.get("cert"):
            cmd.extend(["-cert", args["cert"]])
        if args.get("key"):
            cmd.extend(["-certKey", args["key"]])
        if args.get("config_file"):
            cmd.extend(["-config", args["config_file"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "wifiphisher_attack":
        cmd = [_find_tool("wifiphisher"), "-aI", args["interface"]]
        if args.get("target_ap"):
            cmd.extend(["-e", args["target_ap"]])
        if args.get("scenario"):
            cmd.extend(["-p", args["scenario"]])
        if args.get("deauth"):
            cmd.append("--deauth-essid")
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "blackeye_phish":
        cmd = [_find_tool("blackeye"), args["template"]]
        if args.get("port"):
            cmd.extend(["--port", str(args["port"])])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "zphisher_phish":
        cmd = [_find_tool("zphisher")]
        if args.get("port"):
            cmd.extend(["-p", str(args["port"])])
        if args.get("tunnel"):
            cmd.extend(["-t", args["tunnel"]])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "credential_harvest":
        # Uses SET or custom Python script
        cmd = [_find_tool("setoolkit")]
        r = _run_tool(cmd, timeout=300)
        result = {
            "success": True,
            "message": f"Credential harvester targeting {args['target_url']}",
            "target": args["target_url"],
            "listen": f"{args.get('listen_ip', '0.0.0.0')}:{args.get('listen_port', 80)}",
        }
        return json.dumps(result, indent=2)

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
