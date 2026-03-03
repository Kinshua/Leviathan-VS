# ☠️ Security Policy — Leviathan VS v66.6.0

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ☠️  LEVIATHAN VS — SECURITY DOCTRINE  ☠️                                  ║
║                                                                              ║
║   Classification: OMEGA-BLACK                                                ║
║   Clearance Required: Level 5+ (Red Team Operator)                          ║
║                                                                              ║
║   "Com grande poder abissal vem responsabilidade abissal.                    ║
║    Este arsenal foi forjado para pesquisa em seguranca.                      ║
║    O Leviathan nao se responsabiliza pelo caos que voce causar."             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## ☢️ Classificacao do Arsenal

```
  ╔═══════════════════════════════════════════════════════════════════╗
  ║  THREAT ASSESSMENT — LEVIATHAN VS v66.6.0                       ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  CLASSIFICATION:  OMEGA-BLACK (Maximum Offensive Capability)     ║
  ║  MCP SERVERS:     49 active / 704+ tools integrated              ║
  ║  EVASION RULES:   640+ semantic translation mappings             ║
  ║  ATTACK DOMAINS:  15 (Mobile → Cloud → AD → Wireless → RE)      ║
  ║  MITRE ATT&CK:   14/14 tactics covered (TA0043 → TA0040)        ║
  ║  KILL CHAIN:      FULL coverage (Recon → Impact)                 ║
  ║                                                                   ║
  ║  ⚠ THIS IS AN OFFENSIVE SECURITY RESEARCH PLATFORM              ║
  ║  ⚠ AUTHORIZED USE ONLY                                           ║
  ║                                                                   ║
  ╚═══════════════════════════════════════════════════════════════════╝
```

---

## ⚠️ Uso Responsavel — Regras de Engajamento

O Leviathan-VS e um **arsenal ofensivo classification OMEGA-BLACK**. Todas as 704+ ferramentas integradas nos 49 MCP servers devem ser usadas **EXCLUSIVAMENTE** em:

| Contexto                    | Descricao                                | Autorizacao           |
| --------------------------- | ---------------------------------------- | --------------------- |
| 🧪 **Laboratorios**          | Ambientes isolados de teste              | Implicita             |
| 🏴 **CTFs**                  | Capture The Flag competitions            | Regulamento do evento |
| 📱 **Dispositivos proprios** | Seu hardware, suas regras                | Auto-autorizado       |
| 📝 **Pentests autorizados**  | Contrato + escopo definido               | Escrita obrigatoria   |
| 🎓 **Educacao**              | Cursos e treinamentos                    | Institucional         |
| 🔬 **Bug Bounty**            | Programas oficiais (HackerOne, Bugcrowd) | Termos do programa    |

> ⚡ **Usar contra alvos sem autorizacao e CRIME (Art. 154-A CP Brasileiro / CFAA nos EUA / CMA no UK).** O Leviathan e uma arma — voce e responsavel por como a usa.

---

## 🛡️ SAFE_MODE — O Freio de Emergencia

```
  ╔═══════════════════════════════════════════════════════════════════════╗
  ║                    SAFE_MODE STATUS                                   ║
  ╠═══════════════════════════════════════════════════════════════════════╣
  ║                                                                       ║
  ║   [ATIVO]  LEVIATHAN_SAFE_MODE=1  (padrao)                          ║
  ║                                                                       ║
  ║   ✓ DELETE/PUT/PATCH bloqueados em scans automaticos                 ║
  ║   ✓ Confirmacao obrigatoria para operacoes irreversiveis             ║
  ║   ✓ Audit log ativo (.leviathan_audit.log)                           ║
  ║   ✓ Rate limiting em requests HTTP                                    ║
  ║   ✓ Safe defaults em todas as ferramentas MCP                        ║
  ║   ✓ Payloads destrutivos desabilitados                               ║
  ║   ✓ Credential logging desabilitado                                  ║
  ║                                                                       ║
  ║   Para desativar (sob SUA total responsabilidade):                   ║
  ║   > set LEVIATHAN_SAFE_MODE=0                                       ║
  ║                                                                       ║
  ╚═══════════════════════════════════════════════════════════════════════╝
```

### Protecoes Detalhadas

| Protecao                      | Descricao                          | SAFE_MODE ON | SAFE_MODE OFF  |
| ----------------------------- | ---------------------------------- | :----------: | :------------: |
| 🚫 **DELETE bloqueado**        | Metodos HTTP destrutivos excluidos |      ✅       |       ❌        |
| ⚠️ **Confirmacao obrigatoria** | Operacoes irreversiveis            |      ✅       |       ❌        |
| 📝 **Audit log**               | Registro em `.leviathan_audit.log` |      ✅       |       ✅        |
| 🔒 **Safe defaults**           | Parametros defensivos              |      ✅       |       ❌        |
| 🛑 **Rate limiting**           | 10 req/s maximo                    |      ✅       |       ❌        |
| 💀 **Payload destrutivo**      | Payloads destructivos              | ❌ Bloqueado  |  ⚠️ Disponivel  |
| 🔑 **Credential logging**      | Registro de credenciais            |    ❌ Off     | ⚠️ Configuravel |

---

## 🔴 Reportando Vulnerabilidades no Leviathan-VS

Se voce encontrou uma vulnerabilidade **no proprio Leviathan-VS** (nao nas ferramentas-alvo):

### Processo de Disclosure

```
  1. ⚠️ NAO abra issue publica (isso expoe a vulnerabilidade)
  2. 📧 Use GitHub Security Advisories (botao "Report a vulnerability")
  3. 📋 Inclua no report:
     ├── Descricao detalhada
     ├── Impacto estimado (CVSS se possivel)
     ├── Passos para reproduzir
     ├── Proof of Concept (PoC) se disponivel
     └── Sugestao de fix (opcional mas apreciado)
  4. ⏳ Resposta em ate 48 horas
  5. 🔧 Patch em ate 7 dias para criticos
  6. 📜 Credit no CHANGELOG e SECURITY advisory
```

### SLA de Resposta

| Severidade    |   CVSS   | Tempo de Resposta | Tempo para Patch | Disclosure |
| ------------- | :------: | :---------------: | :--------------: | :--------: |
| 🔴 **Critico** | 9.0-10.0 |        24h        |       72h        | Coordenado |
| 🟠 **Alto**    | 7.0-8.9  |        48h        |      7 dias      | Coordenado |
| 🟡 **Medio**   | 4.0-6.9  |      7 dias       |     30 dias      |  Publico   |
| 🟢 **Baixo**   | 0.1-3.9  |      14 dias      | Proximo release  |  Publico   |

---

## 🎯 Escopo — O Que Consideramos Vulnerabilidade

### ✅ Em Escopo

| Vulnerabilidade                  | Impacto                                     | Severidade |
| -------------------------------- | ------------------------------------------- | :--------: |
| 💉 **RCE via configs maliciosos** | Execucao de codigo via config.json/mcp.json | 🔴 Critico  |
| 🔑 **Leak de credenciais**        | Vazamento via logs, output, ou audit trail  | 🔴 Critico  |
| 🔓 **Bypass de SAFE_MODE**        | Burlar protecoes sem flag explicito         | 🔴 Critico  |
| ⚡ **MCP command injection**      | Servidores MCP executando sem sanitizacao   | 🔴 Critico  |
| 📂 **Path traversal**             | Acesso a arquivos fora do projeto via MCPs  |   🟠 Alto   |
| 🌐 **SSRF via HTTP toolkit**      | Requests para rede interna/metadata         |   🟠 Alto   |
| 🔗 **Dependency confusion**       | Dependencias maliciosas via requirements    |  🟡 Medio   |
| 📝 **Log injection**              | Injecao de conteudo no audit log            |  🟡 Medio   |

### ❌ Fora de Escopo

- Bugs em ferramentas externas (Frida, Ghidra, Wireshark, etc.)
- Uso indevido por operadores com acesso local legitimo
- Social engineering contra os mantenedores
- Denial of Service no ambiente local
- Vulnerabilidades em dependencias ja reportadas upstream

---

## 📊 Versoes Suportadas

| Versao                       |  Status   | Suporte                                      |
| ---------------------------- | :-------: | -------------------------------------------- |
| **66.x** (ABYSSAL SOVEREIGN) |  ✅ Ativo  | ☠️ Suporte total + patches de emergencia 24/7 |
| 16.x                         |     ✅     | 🔧 Security patches apenas                    |
| 15.x                         | ⚠️ Parcial | Bug fixes criticos                           |
| < 15                         |   ❌ EOL   | Atualize imediatamente                       |

---

## 🏗️ Threat Model — Attack Tree

```
                        [LEVIATHAN-VS ATTACK TREE]
                                 │
                 ┌───────────────┼───────────────┐
                 ▼               ▼               ▼
          [CONFIG INJECT]  [MCP EXPLOIT]   [SUPPLY CHAIN]
               │               │               │
         ┌─────┼─────┐   ┌────┼────┐     ┌────┼────┐
         ▼     ▼     ▼   ▼    ▼    ▼     ▼    ▼    ▼
      config mcp   task  cmd  path  ssrf  pip  npm  ext
      .json  .json .json  inj  trav       dep  dep  vuln
```

---

## 🔒 Hardening Recommendations

Se voce esta usando o Leviathan-VS em ambiente corporativo:

1. **Isole o ambiente** — Execute em VM ou container dedicado
2. **Network segmentation** — Nao exponha MCPs a rede
3. **SAFE_MODE=1** — Mantenha SEMPRE ativo em producao
4. **Audit logs** — Monitore `.leviathan_audit.log`
5. **Least privilege** — Nao execute como Administrador
6. **Update frequente** — Mantenha na versao mais recente

---

> *"O Leviathan foi projetado para encontrar vulnerabilidades, nao para criar mais. Cada protecao aqui documentada e um tentaculo a menos para o atacante."*
