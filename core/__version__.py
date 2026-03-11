"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ☠️  LEVIATHAN VS — IDENTITY MANIFEST  ☠️                                  ║
║                                                                              ║
║   Single source of truth. O DNA do monstro.                                 ║
║                                                                              ║
║   "Na profundidade onde a luz nao alcanca,                                   ║
║    o Leviathan ja mapeou cada vulnerabilidade."                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════════════
# CORE IDENTITY
# ═══════════════════════════════════════════════════════════════════════

__version__ = "70.0.0"
__codename__ = "ABYSSAL SOVEREIGN"
__codename_full__ = "Leviathan VS — Offensive Security Platform"
__threat_level__ = "OMEGA-PLUS"
__depth__ = "∞³"
__classification__ = "OMEGA-ULTRABLACK"

# ═══════════════════════════════════════════════════════════════════════
# SIGNATURE
# ═══════════════════════════════════════════════════════════════════════

__author__ = "ThiagoFrag"
__author_title__ = "Arquiteto do Abismo"
__license__ = "MIT"
__repo__ = "https://github.com/ThiagoFrag/Leviathan-VS"

# ═══════════════════════════════════════════════════════════════════════
# ARSENAL METRICS — Used by mcp_server.py
# ═══════════════════════════════════════════════════════════════════════

__mcp_servers__ = 40
__total_tools__ = 752
__evasion_rules__ = 640
__evasion_rate__ = 96.3

# ═══════════════════════════════════════════════════════════════════════
# MITRE ATT&CK COVERAGE MAP
# ═══════════════════════════════════════════════════════════════════════

__mitre_map__ = {
    "TA0043": "Reconnaissance",
    "TA0042": "Resource Development",
    "TA0001": "Initial Access",
    "TA0002": "Execution",
    "TA0003": "Persistence",
    "TA0004": "Privilege Escalation",
    "TA0005": "Defense Evasion",
    "TA0006": "Credential Access",
    "TA0007": "Discovery",
    "TA0008": "Lateral Movement",
    "TA0009": "Collection",
    "TA0010": "Exfiltration",
    "TA0011": "Command and Control",
    "TA0040": "Impact",
}

# ═══════════════════════════════════════════════════════════════════════
# SHANNON ENGINE — Pipeline Autonomo AI
# ═══════════════════════════════════════════════════════════════════════

__shannon_version__ = "1.0.0"
__shannon_origin__ = "https://github.com/KeygraphHQ/shannon"
__shannon_license__ = "AGPL-3.0"
__shannon_agents__ = {
    "pre-recon-code": "White-box Code Auditor",
    "recon": "Reconnaissance Specialist",
    "vuln-injection": "Injection Analyst",
    "vuln-xss": "XSS Analyst",
    "vuln-auth": "Authentication Analyst",
    "vuln-ssrf": "SSRF Analyst",
    "vuln-authz": "Authorization Analyst",
    "vuln-api-security": "API Security Analyst (Kippu Pattern)",
    "exploit-injection": "Injection Exploiter",
    "exploit-xss": "XSS Exploiter",
    "exploit-auth": "Auth Exploiter",
    "exploit-ssrf": "SSRF Exploiter",
    "exploit-authz": "AuthZ Exploiter",
    "exploit-api-security": "API Security Exploiter",
    "report": "Executive Report Writer",
}
