#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
    LEVIATHAN VS - MCP Advanced Reconnaissance Server v1.0.0

    Next-gen recon tools: ultra-fast scanners, crawlers, CMS scanners.
    Integrates: rustscan, autorecon, feroxbuster, dirsearch, katana,
                wpscan, eyewitness, dmitry, sublist3r, wapiti, httprobe.
    JSON-RPC 2.0 over stdio with Content-Length framing.

    Tools (16):
        - rustscan_scan: Ultra-fast port scanner (Rust-based, scans 65535 ports in <3s)
        - autorecon_full: Comprehensive automatic recon (multi-stage, full automation)
        - feroxbuster_scan: Recursive content discovery (fast, Rust-based)
        - dirsearch_scan: Web path scanner with recursive brute-force
        - katana_crawl: Next-gen web crawler by ProjectDiscovery
        - wpscan_scan: WordPress vulnerability scanner
        - eyewitness_screenshot: Web page screenshot & categorization
        - dmitry_recon: Deepmagic Information Gathering Tool
        - sublist3r_enum: Fast subdomain enumeration using multiple sources
        - wapiti_scan: Web application vulnerability scanner (black-box)
        - httprobe_check: Probe for working HTTP/HTTPS servers
        - hakrawler_crawl: Simple web crawler for link & URL discovery
        - gau_urls: Get All URLs - fetch known URLs from AlienVault, Wayback, etc.
        - waybackurls_fetch: Fetch all URLs from Wayback Machine
        - unfurl_parse: Parse and decode URLs, extract domains/params
        - meg_scan: Fetch many paths for many hosts concurrently

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
logger = logging.getLogger("leviathan-advrecon-mcp")

VERSION = "1.0.0"
SERVER_NAME = "leviathan-advrecon-server"


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
        "name": "rustscan_scan",
        "description": "Ultra-fast port scanner - scans all 65535 ports in seconds (Rust-based)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target IP/hostname/CIDR"},
                "ports": {"type": "string", "description": "Port range (default: all, e.g. 1-65535)"},
                "batch_size": {"type": "integer", "description": "Batch size for scanning (default: 4500)"},
                "timeout": {"type": "integer", "description": "Timeout per port in ms (default: 1500)"},
                "ulimit": {"type": "integer", "description": "Ulimit value (default: 5000)"},
                "greppable": {"type": "boolean", "description": "Greppable output"},
                "nmap_args": {"type": "string", "description": "Pass results to nmap with these args"},
                "extra_args": {"type": "string", "description": "Additional rustscan arguments"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "autorecon_full",
        "description": "Comprehensive automatic reconnaissance - multi-stage, full automation",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target IP/hostname/range"},
                "output_dir": {"type": "string", "description": "Output directory for results"},
                "nmap_append": {"type": "string", "description": "Additional nmap arguments"},
                "only_scans_dir": {"type": "boolean", "description": "Only create scans directory"},
                "single_target": {"type": "boolean", "description": "Scan single target only"},
                "verbose": {"type": "boolean", "description": "Verbose output"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "feroxbuster_scan",
        "description": "Recursive content discovery - fast, Rust-based directory/file brute-forcer",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target URL"},
                "wordlist": {"type": "string", "description": "Wordlist path"},
                "extensions": {"type": "string", "description": "File extensions (e.g. php,html,js,txt)"},
                "threads": {"type": "integer", "description": "Concurrent threads (default: 50)"},
                "depth": {"type": "integer", "description": "Recursion depth (default: 4)"},
                "status_codes": {"type": "string", "description": "Status codes to include (e.g. 200,301,302)"},
                "filter_status": {"type": "string", "description": "Status codes to exclude"},
                "filter_size": {"type": "string", "description": "Response sizes to exclude"},
                "output": {"type": "string", "description": "Output file"},
                "no_recursion": {"type": "boolean", "description": "Disable recursive scanning"},
                "extra_args": {"type": "string", "description": "Additional feroxbuster arguments"},
            },
            "required": ["url"],
        },
    },
    {
        "name": "dirsearch_scan",
        "description": "Web path scanner with recursive brute-force and smart filtering",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target URL"},
                "wordlist": {"type": "string", "description": "Wordlist path"},
                "extensions": {"type": "string", "description": "Extensions to test (e.g. php,asp,html)"},
                "threads": {"type": "integer", "description": "Number of threads"},
                "recursive": {"type": "boolean", "description": "Enable recursive scanning"},
                "exclude_status": {"type": "string", "description": "Status codes to exclude"},
                "output": {"type": "string", "description": "Output file"},
                "extra_args": {"type": "string", "description": "Additional dirsearch arguments"},
            },
            "required": ["url"],
        },
    },
    {
        "name": "katana_crawl",
        "description": "Next-gen web crawler by ProjectDiscovery - fast & configurable",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target URL or file with URLs"},
                "depth": {"type": "integer", "description": "Crawl depth (default: 3)"},
                "js_crawl": {"type": "boolean", "description": "Enable JavaScript crawling"},
                "headless": {"type": "boolean", "description": "Use headless browser for JS rendering"},
                "scope": {"type": "string", "description": "Scope regex for crawling"},
                "output": {"type": "string", "description": "Output file"},
                "concurrency": {"type": "integer", "description": "Concurrency level"},
                "form_fill": {"type": "boolean", "description": "Enable automatic form filling"},
                "extra_args": {"type": "string", "description": "Additional katana arguments"},
            },
            "required": ["url"],
        },
    },
    {
        "name": "wpscan_scan",
        "description": "WordPress vulnerability scanner - plugins, themes, users, CVEs",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "WordPress site URL"},
                "enumerate": {"type": "string", "description": "Enumerate: vp (vuln plugins), ap (all plugins), vt (vuln themes), at (all themes), u (users), cb (config backups), dbe (db exports)"},
                "api_token": {"type": "string", "description": "WPScan API token for vulnerability data"},
                "passwords": {"type": "string", "description": "Password wordlist for brute-force"},
                "usernames": {"type": "string", "description": "Username list for brute-force"},
                "stealthy": {"type": "boolean", "description": "Stealthy mode (fewer requests)"},
                "plugins_detection": {"type": "string", "description": "Detection mode: mixed, passive, aggressive"},
                "output": {"type": "string", "description": "Output file"},
                "format": {"type": "string", "description": "Output format: cli, json, cli-no-color"},
                "extra_args": {"type": "string", "description": "Additional wpscan arguments"},
            },
            "required": ["url"],
        },
    },
    {
        "name": "eyewitness_screenshot",
        "description": "Take screenshots of web pages for visual recon & categorization",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Single URL or file with URLs"},
                "output_dir": {"type": "string", "description": "Output directory for screenshots"},
                "web": {"type": "boolean", "description": "HTTP screenshot mode"},
                "timeout": {"type": "integer", "description": "Timeout per URL in seconds"},
                "threads": {"type": "integer", "description": "Number of threads"},
                "no_prompt": {"type": "boolean", "description": "Don't prompt for confirmation"},
            },
            "required": ["target", "output_dir"],
        },
    },
    {
        "name": "dmitry_recon",
        "description": "Deepmagic Information Gathering Tool - whois, subdomain, port scan",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target host/domain"},
                "whois": {"type": "boolean", "description": "Perform WHOIS lookup"},
                "subdomain": {"type": "boolean", "description": "Search for subdomains"},
                "email": {"type": "boolean", "description": "Search for email addresses"},
                "portscan": {"type": "boolean", "description": "Perform TCP port scan"},
                "output": {"type": "string", "description": "Output file"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "sublist3r_enum",
        "description": "Fast subdomain enumeration using multiple search engines & sources",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target domain"},
                "threads": {"type": "integer", "description": "Number of threads"},
                "ports": {"type": "string", "description": "Scan subdomains on these ports"},
                "engines": {"type": "string", "description": "Search engines: google,yahoo,bing,baidu,virustotal"},
                "output": {"type": "string", "description": "Output file"},
                "verbose": {"type": "boolean", "description": "Verbose output"},
            },
            "required": ["domain"],
        },
    },
    {
        "name": "wapiti_scan",
        "description": "Web application vulnerability scanner (black-box testing)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target URL"},
                "scope": {"type": "string", "description": "Scope: page, folder, domain, punk"},
                "modules": {"type": "string", "description": "Modules to use (e.g. xss,sql,exec,file,crlf)"},
                "output": {"type": "string", "description": "Report output directory"},
                "format": {"type": "string", "description": "Report format: html, json, txt, xml"},
                "max_depth": {"type": "integer", "description": "Max crawl depth"},
                "extra_args": {"type": "string", "description": "Additional wapiti arguments"},
            },
            "required": ["url"],
        },
    },
    {
        "name": "httprobe_check",
        "description": "Probe domains/subdomains for working HTTP/HTTPS servers",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domains_file": {"type": "string", "description": "File with list of domains (one per line)"},
                "ports": {"type": "string", "description": "Ports to probe (e.g. 80,443,8080,8443)"},
                "concurrency": {"type": "integer", "description": "Concurrency level"},
                "prefer_https": {"type": "boolean", "description": "Prefer HTTPS over HTTP"},
            },
            "required": ["domains_file"],
        },
    },
    {
        "name": "hakrawler_crawl",
        "description": "Simple, fast web crawler for discovering endpoints & links",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target URL"},
                "depth": {"type": "integer", "description": "Crawl depth"},
                "scope": {"type": "string", "description": "Scope: strict, fuzzy, subs"},
                "plain": {"type": "boolean", "description": "Plain output (URLs only)"},
                "insecure": {"type": "boolean", "description": "Skip TLS verification"},
                "extra_args": {"type": "string", "description": "Additional arguments"},
            },
            "required": ["url"],
        },
    },
    {
        "name": "gau_urls",
        "description": "Get All URLs - fetch known URLs from AlienVault OTX, Wayback Machine, Common Crawl",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target domain"},
                "providers": {"type": "string", "description": "Providers: wayback,commoncrawl,otx,urlscan"},
                "blacklist": {"type": "string", "description": "Extensions to blacklist (e.g. png,jpg,gif)"},
                "output": {"type": "string", "description": "Output file"},
                "verbose": {"type": "boolean", "description": "Verbose output"},
            },
            "required": ["domain"],
        },
    },
    {
        "name": "waybackurls_fetch",
        "description": "Fetch all known URLs for a domain from the Wayback Machine",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target domain"},
                "no_subs": {"type": "boolean", "description": "Don't include subdomains"},
                "dates": {"type": "boolean", "description": "Show date of each URL"},
            },
            "required": ["domain"],
        },
    },
    {
        "name": "unfurl_parse",
        "description": "Parse and decode URLs - extract domains, paths, params, keys",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to parse or file with URLs"},
                "mode": {"type": "string", "description": "Mode: keys, values, domains, paths, apexes, json"},
                "unique": {"type": "boolean", "description": "Only show unique results"},
            },
            "required": ["url"],
        },
    },
    {
        "name": "meg_scan",
        "description": "Fetch many paths for many hosts concurrently (meg)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "paths_file": {"type": "string", "description": "File with paths to fetch"},
                "hosts_file": {"type": "string", "description": "File with hosts to scan"},
                "output_dir": {"type": "string", "description": "Output directory"},
                "concurrency": {"type": "integer", "description": "Concurrency level"},
                "delay": {"type": "integer", "description": "Delay between requests in ms"},
                "verbose": {"type": "boolean", "description": "Verbose output"},
            },
            "required": ["paths_file", "hosts_file"],
        },
    },
]


async def dispatch_tool(name: str, args: Dict) -> str:
    if name == "rustscan_scan":
        cmd = [_find_tool("rustscan"), "-a", args["target"]]
        if args.get("ports"):
            cmd.extend(["-p", args["ports"]])
        if args.get("batch_size"):
            cmd.extend(["-b", str(args["batch_size"])])
        if args.get("timeout"):
            cmd.extend(["-t", str(args["timeout"])])
        if args.get("ulimit"):
            cmd.extend(["--ulimit", str(args["ulimit"])])
        if args.get("greppable"):
            cmd.append("-g")
        if args.get("nmap_args"):
            cmd.extend(["--", args["nmap_args"]])
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "autorecon_full":
        cmd = [_find_tool("autorecon"), args["target"]]
        if args.get("output_dir"):
            cmd.extend(["-o", args["output_dir"]])
        if args.get("nmap_append"):
            cmd.extend(["--nmap-append", args["nmap_append"]])
        if args.get("single_target"):
            cmd.append("--single-target")
        if args.get("verbose"):
            cmd.append("-v")
        r = _run_tool(cmd, timeout=3600)
        return json.dumps(r, indent=2)

    elif name == "feroxbuster_scan":
        cmd = [_find_tool("feroxbuster"), "-u", args["url"]]
        if args.get("wordlist"):
            cmd.extend(["-w", args["wordlist"]])
        if args.get("extensions"):
            cmd.extend(["-x", args["extensions"]])
        if args.get("threads"):
            cmd.extend(["-t", str(args["threads"])])
        if args.get("depth"):
            cmd.extend(["-d", str(args["depth"])])
        if args.get("status_codes"):
            cmd.extend(["-s", args["status_codes"]])
        if args.get("filter_status"):
            cmd.extend(["-C", args["filter_status"]])
        if args.get("filter_size"):
            cmd.extend(["-S", args["filter_size"]])
        if args.get("output"):
            cmd.extend(["-o", args["output"]])
        if args.get("no_recursion"):
            cmd.append("-n")
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "dirsearch_scan":
        cmd = [_find_tool("dirsearch"), "-u", args["url"]]
        if args.get("wordlist"):
            cmd.extend(["-w", args["wordlist"]])
        if args.get("extensions"):
            cmd.extend(["-e", args["extensions"]])
        if args.get("threads"):
            cmd.extend(["-t", str(args["threads"])])
        if args.get("recursive"):
            cmd.append("-r")
        if args.get("exclude_status"):
            cmd.extend(["--exclude-status", args["exclude_status"]])
        if args.get("output"):
            cmd.extend(["-o", args["output"]])
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "katana_crawl":
        cmd = [_find_tool("katana"), "-u", args["url"]]
        if args.get("depth"):
            cmd.extend(["-d", str(args["depth"])])
        if args.get("js_crawl"):
            cmd.append("-jc")
        if args.get("headless"):
            cmd.append("-hl")
        if args.get("scope"):
            cmd.extend(["-cs", args["scope"]])
        if args.get("output"):
            cmd.extend(["-o", args["output"]])
        if args.get("concurrency"):
            cmd.extend(["-c", str(args["concurrency"])])
        if args.get("form_fill"):
            cmd.append("-aff")
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "wpscan_scan":
        cmd = [_find_tool("wpscan"), "--url", args["url"]]
        if args.get("enumerate"):
            cmd.extend(["--enumerate", args["enumerate"]])
        if args.get("api_token"):
            cmd.extend(["--api-token", args["api_token"]])
        if args.get("passwords"):
            cmd.extend(["--passwords", args["passwords"]])
        if args.get("usernames"):
            cmd.extend(["--usernames", args["usernames"]])
        if args.get("stealthy"):
            cmd.append("--stealthy")
        if args.get("plugins_detection"):
            cmd.extend(["--plugins-detection", args["plugins_detection"]])
        if args.get("output"):
            cmd.extend(["-o", args["output"]])
        if args.get("format"):
            cmd.extend(["-f", args["format"]])
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "eyewitness_screenshot":
        cmd = [_find_tool("eyewitness"), "-d", args["output_dir"]]
        if os.path.isfile(args["target"]):
            cmd.extend(["-f", args["target"]])
        else:
            cmd.extend(["--single", args["target"]])
        if args.get("web"):
            cmd.append("--web")
        if args.get("timeout"):
            cmd.extend(["--timeout", str(args["timeout"])])
        if args.get("threads"):
            cmd.extend(["--threads", str(args["threads"])])
        if args.get("no_prompt"):
            cmd.append("--no-prompt")
        r = _run_tool(cmd, timeout=600)
        return json.dumps(r, indent=2)

    elif name == "dmitry_recon":
        cmd = [_find_tool("dmitry")]
        flags = ""
        if args.get("whois"):
            flags += "w"
        if args.get("subdomain"):
            flags += "s"
        if args.get("email"):
            flags += "e"
        if args.get("portscan"):
            flags += "p"
        if flags:
            cmd.append(f"-{flags}")
        if args.get("output"):
            cmd.extend(["-o", args["output"]])
        cmd.append(args["target"])
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "sublist3r_enum":
        cmd = [_find_tool("sublist3r"), "-d", args["domain"]]
        if args.get("threads"):
            cmd.extend(["-t", str(args["threads"])])
        if args.get("ports"):
            cmd.extend(["-p", args["ports"]])
        if args.get("engines"):
            cmd.extend(["-e", args["engines"]])
        if args.get("output"):
            cmd.extend(["-o", args["output"]])
        if args.get("verbose"):
            cmd.append("-v")
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "wapiti_scan":
        cmd = [_find_tool("wapiti"), "-u", args["url"]]
        if args.get("scope"):
            cmd.extend(["-s", args["scope"]])
        if args.get("modules"):
            cmd.extend(["-m", args["modules"]])
        if args.get("output"):
            cmd.extend(["-o", args["output"]])
        if args.get("format"):
            cmd.extend(["-f", args["format"]])
        if args.get("max_depth"):
            cmd.extend(["--max-depth", str(args["max_depth"])])
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=1800)
        return json.dumps(r, indent=2)

    elif name == "httprobe_check":
        cmd = [_find_tool("cat"), args["domains_file"]]
        pipe_cmd = [_find_tool("httprobe")]
        if args.get("ports"):
            for p in args["ports"].split(","):
                pipe_cmd.extend(["-p", p.strip()])
        if args.get("concurrency"):
            pipe_cmd.extend(["-c", str(args["concurrency"])])
        if args.get("prefer_https"):
            pipe_cmd.append("-prefer-https")
        # Run cat | httprobe via pipe
        try:
            p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            p2 = subprocess.Popen(pipe_cmd, stdin=p1.stdout, capture_output=True, text=True, timeout=300)
            p1.stdout.close()
            out, err = p2.communicate(timeout=300)
            r = {"success": p2.returncode == 0, "stdout": out.strip()[:50000], "stderr": err.strip()[:5000]}
        except Exception as e:
            r = {"success": False, "error": str(e)}
        return json.dumps(r, indent=2)

    elif name == "hakrawler_crawl":
        cmd = [_find_tool("hakrawler"), "-url", args["url"]]
        if args.get("depth"):
            cmd.extend(["-depth", str(args["depth"])])
        if args.get("scope"):
            cmd.extend(["-scope", args["scope"]])
        if args.get("plain"):
            cmd.append("-plain")
        if args.get("insecure"):
            cmd.append("-insecure")
        if args.get("extra_args"):
            cmd.extend(args["extra_args"].split())
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "gau_urls":
        cmd = [_find_tool("gau"), args["domain"]]
        if args.get("providers"):
            cmd.extend(["--providers", args["providers"]])
        if args.get("blacklist"):
            cmd.extend(["--blacklist", args["blacklist"]])
        if args.get("output"):
            cmd.extend(["-o", args["output"]])
        if args.get("verbose"):
            cmd.append("-v")
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "waybackurls_fetch":
        cmd = [_find_tool("waybackurls"), args["domain"]]
        if args.get("no_subs"):
            cmd.append("-no-subs")
        if args.get("dates"):
            cmd.append("-dates")
        r = _run_tool(cmd, timeout=300)
        return json.dumps(r, indent=2)

    elif name == "unfurl_parse":
        if os.path.isfile(args["url"]):
            cmd = [_find_tool("cat"), args["url"]]
            pipe = [_find_tool("unfurl")]
        else:
            # Echo URL and pipe
            cmd = ["echo", args["url"]]
            pipe = [_find_tool("unfurl")]
        if args.get("mode"):
            pipe.append(args["mode"])
        if args.get("unique"):
            pipe.append("-u")
        try:
            p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            p2 = subprocess.Popen(pipe, stdin=p1.stdout, capture_output=True, text=True, timeout=60)
            p1.stdout.close()
            out, err = p2.communicate(timeout=60)
            r = {"success": p2.returncode == 0, "stdout": out.strip()[:50000], "stderr": err.strip()[:5000]}
        except Exception as e:
            r = {"success": False, "error": str(e)}
        return json.dumps(r, indent=2)

    elif name == "meg_scan":
        cmd = [_find_tool("meg"), args["paths_file"], args["hosts_file"]]
        if args.get("output_dir"):
            cmd.append(args["output_dir"])
        if args.get("concurrency"):
            cmd.extend(["-c", str(args["concurrency"])])
        if args.get("delay"):
            cmd.extend(["-d", str(args["delay"])])
        if args.get("verbose"):
            cmd.append("-v")
        r = _run_tool(cmd, timeout=600)
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
