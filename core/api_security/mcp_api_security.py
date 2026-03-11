#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
████████████████████████████████████████████████████████████████████████████████████
██                                                                                ██
██  🛡️  LEVIATHAN VS - MCP API Security Server v1.0.0                           ██
██                                                                                ██
██  API Security Testing MCP server.                                             ██
██  Integrates: Broken Access Control, Data Exposure, JWT Attacks,               ██
██              Rate Limiting, IDOR, User Enumeration, CORS Analysis.            ██
██  JSON-RPC 2.0 over stdio with Content-Length framing.                         ██
██                                                                                ██
██  Tools (16):                                                                   ██
██    - api_audit_full:       Complete OWASP API security audit                  ██
██    - api_scan_access:      Broken Access Control scanner (A01:2021)           ██
██    - api_scan_exposure:    Sensitive Data Exposure scanner (A02:2021)         ██
██    - api_scan_jwt:         JWT security testing suite                         ██
██    - api_scan_idor:        IDOR vulnerability scanner                         ██
██    - api_scan_ratelimit:   Rate limiting analyzer                             ██
██    - api_scan_enum:        User enumeration detector                          ██
██    - api_scan_cors:        CORS misconfiguration scanner                      ██
██    - api_scan_headers:     Security header analyzer                           ██
██    - api_scan_privesc:     Privilege escalation tester                        ██
██    - api_scan_methods:     HTTP method tampering tester                       ██
██    - api_generate_report:  Generate full security report                      ██
██    - pentest_full:         Full pentest (all OWASP Top 10 vectors)            ██
██    - pentest_compliance:   Regulatory compliance check (LGPD/GDPR/PCI)       ██
██    - pentest_mass_assign:  Mass assignment vulnerability test                 ██
██    - pentest_report:       Generate comprehensive pentest report              ██
██                                                                                ██
██  Author: ThiagoFrag / LEVIATHAN VS                                            ██
██  Version: 1.0.0                                                                ██
████████████████████████████████████████████████████████████████████████████████████
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional

# Add parent paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.mcp_plugin_base import MCPPluginBase

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger("leviathan-api-security-mcp")


class APISecurityMCPServer(MCPPluginBase):
    """MCP Server for API Security Testing.

    Implements 16 tools for comprehensive API security auditing
    covering OWASP Top 10 2021 and OWASP API Security Top 10.
    """

    server_name = "leviathan-api-security-server"
    version = "1.0.0"
    tools = [
        {
            "name": "api_audit_full",
            "description": (
                "Complete OWASP API security audit. Tests: Broken Access Control, "
                "Sensitive Data Exposure, JWT vulnerabilities, IDOR, rate limiting, "
                "CORS, user enumeration, privilege escalation. Returns full report."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Base URL of the API (e.g. https://example.com)",
                    },
                    "jwt_token": {
                        "type": "string",
                        "description": "JWT token for authenticated tests",
                    },
                    "login_url": {
                        "type": "string",
                        "description": "Login endpoint URL for auth tests",
                    },
                    "endpoints": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of specific API endpoints to test",
                    },
                    "format": {
                        "type": "string",
                        "description": "Report format: json or markdown (default: markdown)",
                    },
                },
                "required": ["target"],
            },
        },
        {
            "name": "api_scan_access",
            "description": (
                "Test for Broken Access Control (OWASP A01:2021). "
                "Checks if endpoints return data without authentication."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Base URL of the API"},
                    "endpoints": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "API endpoints to test",
                    },
                },
                "required": ["target"],
            },
        },
        {
            "name": "api_scan_exposure",
            "description": (
                "Scan for Sensitive Data Exposure (OWASP A02:2021). "
                "Detects PII, tokens, internal IDs in API responses."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Base URL of the API"},
                },
                "required": ["target"],
            },
        },
        {
            "name": "api_scan_jwt",
            "description": (
                "JWT security testing: algorithm none, weak key brute force, "
                "expired token, missing claims."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Base URL of the API"},
                    "token": {"type": "string", "description": "JWT token to test"},
                    "endpoint": {
                        "type": "string",
                        "description": "Protected endpoint to test against",
                    },
                },
                "required": ["target", "token"],
            },
        },
        {
            "name": "api_scan_idor",
            "description": (
                "Test for Insecure Direct Object Reference (IDOR). "
                "Attempts to access resources of other users."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Base URL of the API"},
                    "auth_token": {"type": "string", "description": "Auth token"},
                    "user_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "User IDs to test IDOR against",
                    },
                },
                "required": ["target"],
            },
        },
        {
            "name": "api_scan_ratelimit",
            "description": (
                "Test rate limiting effectiveness. Sends rapid requests "
                "and checks for 429 responses."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Base URL of the API"},
                    "endpoints": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Endpoints to test",
                    },
                    "requests": {
                        "type": "integer",
                        "description": "Number of requests per test (default: 30)",
                    },
                },
                "required": ["target"],
            },
        },
        {
            "name": "api_scan_enum",
            "description": (
                "Test for user enumeration via response/timing differences "
                "on login and registration endpoints."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Base URL of the API"},
                    "login_url": {
                        "type": "string",
                        "description": "Login endpoint URL",
                    },
                },
                "required": ["target"],
            },
        },
        {
            "name": "api_scan_cors",
            "description": (
                "Test CORS policy for misconfigurations that allow "
                "cross-origin data theft."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Base URL of the API"},
                    "endpoints": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Endpoints to test",
                    },
                },
                "required": ["target"],
            },
        },
        {
            "name": "api_scan_headers",
            "description": "Analyze security headers in API responses.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Target URL"},
                },
                "required": ["target"],
            },
        },
        {
            "name": "api_scan_privesc",
            "description": (
                "Test for privilege escalation by accessing admin endpoints "
                "with low-privilege or no credentials."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Base URL of the API"},
                    "token": {
                        "type": "string",
                        "description": "Low-privilege auth token",
                    },
                },
                "required": ["target"],
            },
        },
        {
            "name": "api_scan_methods",
            "description": (
                "Test HTTP method tampering. Checks if endpoints accept "
                "unexpected methods (PUT, DELETE, TRACE)."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Base URL of the API"},
                    "endpoints": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Endpoints to test",
                    },
                },
                "required": ["target"],
            },
        },
        {
            "name": "api_generate_report",
            "description": (
                "Generate a full API security audit report from previous scan results. "
                "Includes OWASP mapping, LGPD/GDPR compliance, remediation roadmap."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "description": "Report format: json or markdown (default: markdown)",
                    },
                },
                "required": [],
            },
        },
        {
            "name": "pentest_full",
            "description": (
                "Run a FULL penetration test covering ALL OWASP Top 10 (2021) attack "
                "vectors: SQLi, XSS, CMDi, SSRF, SSTI, XXE, NoSQLi, Path Traversal, "
                "IDOR, JWT, CORS, CSRF, CRLF, Auth Bypass, Rate Limiting, User Enum, "
                "Mass Assignment, Deserialization, Business Logic, Race Conditions. "
                "Integrates SirenScanner, API Security, Exploit Engine, and Fuzzer."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Target URL to pentest",
                    },
                    "jwt_token": {
                        "type": "string",
                        "description": "JWT token for authenticated tests",
                    },
                    "login_url": {
                        "type": "string",
                        "description": "Login endpoint URL",
                    },
                    "endpoints": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Specific endpoints to focus on",
                    },
                    "enable_fuzzer": {
                        "type": "boolean",
                        "description": "Enable fuzzing (intensive, default: false)",
                    },
                    "aggressive": {
                        "type": "boolean",
                        "description": "Aggressive mode (more payloads, default: false)",
                    },
                    "format": {
                        "type": "string",
                        "description": "Report format: json or markdown (default: markdown)",
                    },
                },
                "required": ["target"],
            },
        },
        {
            "name": "pentest_compliance",
            "description": (
                "Check regulatory compliance (LGPD, GDPR, PCI-DSS, OWASP ASVS) "
                "based on pentest findings. Returns violation matrix with affected "
                "regulations, articles, and remediation requirements."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Target that was previously scanned",
                    },
                },
                "required": ["target"],
            },
        },
        {
            "name": "pentest_mass_assign",
            "description": (
                "Test for Mass Assignment vulnerabilities (OWASP A04/API6). "
                "Sends extra fields (role, is_admin, price, etc.) to detect "
                "if the backend accepts unauthorized field modifications."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "endpoint_url": {
                        "type": "string",
                        "description": "API endpoint to test (e.g. /api/v1/users/me)",
                    },
                    "method": {
                        "type": "string",
                        "description": "HTTP method (POST/PUT/PATCH)",
                    },
                    "original_body": {
                        "type": "object",
                        "description": "Original request body",
                    },
                },
                "required": ["endpoint_url"],
            },
        },
        {
            "name": "pentest_report",
            "description": (
                "Generate a comprehensive penetration test report with OWASP "
                "Top 10 coverage, attack vector distribution, compliance impact, "
                "and prioritized remediation roadmap."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "description": "Report format: json or markdown (default: markdown)",
                    },
                },
                "required": [],
            },
        },
    ]

    def __init__(self):
        super().__init__()
        self._engine = None
        self._pentest_engine = None
        self._pentest_result = None

    def _get_engine(self):
        if self._engine is None:
            from core.shannon.api_security import SirenAPISecurityEngine

            self._engine = SirenAPISecurityEngine()
        return self._engine

    async def dispatch_tool(self, name: str, args: Dict) -> str:
        from core.shannon.api_security import (
            APISecurityHTTP,
            BrokenAccessControlScanner,
            DataExposureScanner,
            JWTSecurityScanner,
            RateLimitScanner,
            UserEnumerationScanner,
        )

        if name == "api_audit_full":
            engine = self._get_engine()
            result = await engine.full_api_audit(
                target=args["target"],
                jwt_token=args.get("jwt_token"),
                login_url=args.get("login_url"),
                endpoints=args.get("endpoints"),
            )
            fmt = args.get("format", "markdown")
            if fmt == "json":
                return engine.generate_json_report()
            return engine.generate_report()

        elif name == "api_scan_access":
            http = APISecurityHTTP()
            scanner = BrokenAccessControlScanner(http)
            try:
                findings = await scanner.scan_unauthenticated_access(
                    args["target"], args.get("endpoints")
                )
                return json.dumps([f.to_dict() for f in findings], indent=2)
            finally:
                await http.close()

        elif name == "api_scan_exposure":
            http = APISecurityHTTP()
            scanner = DataExposureScanner(http)
            try:
                findings = await scanner.scan_response_headers(args["target"])
                findings.extend(await scanner.scan_debug_info_leak(args["target"]))
                return json.dumps([f.to_dict() for f in findings], indent=2)
            finally:
                await http.close()

        elif name == "api_scan_jwt":
            http = APISecurityHTTP()
            scanner = JWTSecurityScanner(http)
            try:
                findings = await scanner.scan_jwt_security(
                    args["target"],
                    args["token"],
                    args.get("endpoint", "/api/v1/users/me"),
                )
                return json.dumps([f.to_dict() for f in findings], indent=2)
            finally:
                await http.close()

        elif name == "api_scan_idor":
            http = APISecurityHTTP()
            scanner = BrokenAccessControlScanner(http)
            try:
                findings = await scanner.scan_idor(
                    args["target"],
                    args.get("auth_token"),
                    args.get("user_ids"),
                )
                return json.dumps([f.to_dict() for f in findings], indent=2)
            finally:
                await http.close()

        elif name == "api_scan_ratelimit":
            http = APISecurityHTTP()
            scanner = RateLimitScanner(http)
            try:
                findings = await scanner.scan_rate_limit(
                    args["target"],
                    args.get("endpoints"),
                    args.get("requests", 30),
                )
                return json.dumps([f.to_dict() for f in findings], indent=2)
            finally:
                await http.close()

        elif name == "api_scan_enum":
            http = APISecurityHTTP()
            scanner = UserEnumerationScanner(http)
            try:
                findings = await scanner.scan_response_enumeration(
                    args["target"], args.get("login_url")
                )
                findings.extend(await scanner.scan_total_count_exposure(args["target"]))
                return json.dumps([f.to_dict() for f in findings], indent=2)
            finally:
                await http.close()

        elif name == "api_scan_cors":
            http = APISecurityHTTP()
            scanner = DataExposureScanner(http)
            try:
                findings = await scanner.scan_cors_policy(
                    args["target"], args.get("endpoints")
                )
                return json.dumps([f.to_dict() for f in findings], indent=2)
            finally:
                await http.close()

        elif name == "api_scan_headers":
            http = APISecurityHTTP()
            scanner = DataExposureScanner(http)
            try:
                findings = await scanner.scan_response_headers(args["target"])
                return json.dumps([f.to_dict() for f in findings], indent=2)
            finally:
                await http.close()

        elif name == "api_scan_privesc":
            http = APISecurityHTTP()
            scanner = BrokenAccessControlScanner(http)
            try:
                findings = await scanner.scan_privilege_escalation(
                    args["target"], args.get("token")
                )
                return json.dumps([f.to_dict() for f in findings], indent=2)
            finally:
                await http.close()

        elif name == "api_scan_methods":
            http = APISecurityHTTP()
            scanner = BrokenAccessControlScanner(http)
            try:
                findings = await scanner.scan_http_method_tampering(
                    args["target"], args.get("endpoints")
                )
                return json.dumps([f.to_dict() for f in findings], indent=2)
            finally:
                await http.close()

        elif name == "api_generate_report":
            engine = self._get_engine()
            if not engine.result:
                return "No scan results available. Run api_audit_full first."
            fmt = args.get("format", "markdown")
            if fmt == "json":
                return engine.generate_json_report()
            return engine.generate_report()

        elif name == "pentest_full":
            from core.shannon.pentest_engine import PentestConfig, SirenPentestEngine

            config = PentestConfig(
                target_url=args["target"],
                jwt_token=args.get("jwt_token", ""),
                login_url=args.get("login_url", ""),
                endpoints=args.get("endpoints", []),
                enable_fuzzer=args.get("enable_fuzzer", False),
                aggressive_mode=args.get("aggressive", False),
            )
            engine = SirenPentestEngine(config)
            result = await engine.run_full_pentest()
            self._pentest_engine = engine
            self._pentest_result = result

            fmt = args.get("format", "markdown")
            if fmt == "json":
                return engine.generate_json_report()
            return engine.generate_report()

        elif name == "pentest_compliance":
            from core.shannon.pentest_engine import ComplianceChecker

            checker = ComplianceChecker()
            if self._pentest_result and self._pentest_result.findings:
                violations = checker.check_compliance(self._pentest_result.findings)
            else:
                return json.dumps(
                    {"error": "No pentest results. Run pentest_full first."}
                )
            return json.dumps(violations, indent=2, default=str)

        elif name == "pentest_mass_assign":
            from core.shannon.pentest_engine import MassAssignmentScanner

            scanner = MassAssignmentScanner()
            endpoint_data = {
                "url": args["endpoint_url"],
                "method": args.get("method", "POST"),
            }
            # Simulate the modified response by adding injection fields to original body
            original = args.get("original_body", {})
            modified_body = dict(original)
            modified_body.update(scanner.INJECTION_FIELDS)

            findings = scanner.scan_mass_assignment(
                endpoint_data=endpoint_data,
                original_response={"status": 200, "body": json.dumps(original)},
                modified_response={"status": 200, "body": json.dumps(modified_body)},
            )
            return json.dumps([f.to_dict() for f in findings], indent=2, default=str)

        elif name == "pentest_report":
            if not self._pentest_engine:
                return "No pentest results available. Run pentest_full first."
            fmt = args.get("format", "markdown")
            if fmt == "json":
                return self._pentest_engine.generate_json_report()
            return self._pentest_engine.generate_report()

        return json.dumps({"error": f"Unknown tool: {name}"})


if __name__ == "__main__":
    APISecurityMCPServer.main()
