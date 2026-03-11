# LEVIATHAN VS — Briefing Operacional

## O QUE É

**Leviathan VS** é uma plataforma de segurança ofensiva completa para VS Code. Integra 36+ MCP servers com 700+ ferramentas organizadas em 13 domínios de ataque, cobrindo os 14 táticas MITRE ATT&CK.

O motor de inteligência autônoma (**Shannon Engine**, em `core/shannon/`) fornece inferência Bayesiana, genética de vulnerabilidades, síntese de exploit chains via A*, simulação de personas de ataque, e auto-evolução por ELO.

> **Nota**: O projeto SIREN (Shannon Intelligence Recon & Exploitation Nexus) agora é um repositório separado em `github.com/Kinshua/Siren`. O Shannon Engine permanece no Leviathan como módulo interno.

---

## ARQUITETURA

### MCP Servers (36 módulos)

| Categoria | MCPs |
|---|---|
| Mobile & Instrumentação | adb, frida_mcp, objection, jadx, androguard, apktool |
| Emuladores Android | ldplayer, nox, memu, bluestacks |
| WebApp Security | webapp, burpsuite, nuclei |
| Recon & OSINT | recon, adv_recon, osint |
| Network | netattack, scapy, mitmproxy, wireless |
| Reverse Engineering | ghidra, r2, reveng, stego, forensics |
| Cloud | cloud |
| Active Directory | active_directory |
| Red Team & C2 | redteam |
| Exploitation | exploit, exploit_dev |
| Credentials | hashcat, wordlist |
| Social Engineering | social_eng |
| Wireshark | wireshark |

### Shannon Engine (core/shannon/) — 6 Tiers

```
TIER 0 — CORTEX (Cérebro Cognitivo)
  bayesian_engine.py    — Inferência probabilística Bayesiana
  vuln_dna.py           — Genética de vulnerabilidades, genoma 128-dim
  exploit_synthesis.py  — Síntese de exploit chains via A*
  attack_persona.py     — Simulação de 8+ tipos de atacante
  knowledge_graph.py    — Grafo de conhecimento persistente

TIER 1 — ARSENAL (Armas Especializadas)
  protocol_dissector.py, supply_chain.py, container_security.py,
  graphql_engine.py, websocket_engine.py

TIER 2 — INTELLIGENCE (Inteligência Analítica)
  attack_narrative.py, defensive_mirror.py, osint_correlator.py,
  deep_fingerprint.py, cve_predictor.py

TIER 3 — AUTOMATION (Campanhas & Monitoração)
  campaign_manager.py, continuous_monitor.py, result_correlator.py

TIER 4 — OUTPUT (Compliance & Remediação)
  compliance_mapper.py, risk_scorer.py, remediation_generator.py

TIER 5 — META (Auto-Evolução)
  self_evolution.py, strategy_db.py, performance_profiler.py
```

### Infraestrutura

- `cli.py` — Interface de comandos (translate, http, doctor, pentest, auth, crypto, api-audit, workspace)
- `mcp_server.py` — Servidor JSON-RPC 2.0 (MCP protocol)
- `mcp_launcher.py` — Seletor interativo de MCPs
- `mcp_plugin_base.py` — Classe base abstrata para plugins
- `doctor.py` — Diagnóstico de ferramentas e ambiente
- `colors.py` — Engine visual (gradientes, animações, banners)
- `config.json` — Base de regras do KRAKEN ENGINE (640+ regras de evasão semântica)

---

## CONVENÇÕES DE CÓDIGO

```python
# Imports canônicos
from __future__ import annotations
import json, logging, threading, time, hashlib, uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional

# Logger
logger = logging.getLogger("siren.<tier>.<module>")

# Dataclasses com to_dict()
@dataclass
class MyData:
    field: str = ""
    def to_dict(self) -> Dict[str, Any]:
        return {"field": self.field}

# Thread safety com RLock
class MyEngine:
    def __init__(self) -> None:
        self._lock = threading.RLock()

# MCP plugins herdam de MCPPluginBase
# Shannon engine: zero deps externas (stdlib only)
# Naming: Siren{Capability} para classes do Shannon
```

## COMO VALIDAR

```bash
# Verificar imports
python -c "from core.shannon import *"

# Doctor
python core/doctor.py

# MCP server
python core/mcp_server.py
```

## CONTEXTO

- Desenvolvedor: ThiagoFrag (GitHub: Kinshua)
- Idioma: código em inglês, docs em português
- Filosofia: "O abismo não responde. Ele executa."
- SIREN: projeto separado em github.com/Kinshua/Siren
