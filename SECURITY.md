# ☠️ Security Policy — Leviathan VS

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   "Com grande poder abissal vem grande responsabilidade abissal."    ║
║                                                                      ║
║   Este arsenal foi forjado para pesquisa em seguranca.               ║
║   O Leviathan nao se responsabiliza pelo caos que voce causar.       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

## ⚠️ Uso Responsavel

O Leviathan-VS e um **arsenal ofensivo nivel militar**. Todas as 704+ ferramentas integradas devem ser usadas **EXCLUSIVAMENTE** em:

- 🧪 **Laboratorios** — ambientes controlados
- 🏴 **CTFs** — Capture The Flag competitions
- 📱 **Dispositivos proprios** — seu hardware, suas regras
- 📝 **Autorizacao explicita** — permissao por escrito do proprietario

> **Usar contra alvos sem autorizacao e crime.** O Leviathan e uma arma — use com responsabilidade.

## 🛡️ SAFE_MODE — O Freio de Emergencia

**SAFE_MODE** esta ativado por padrao (`LEVIATHAN_SAFE_MODE=1`) e:

| Protecao                      | Descricao                                               |
| ----------------------------- | ------------------------------------------------------- |
| 🚫 **DELETE bloqueado**        | Metodos HTTP destrutivos excluidos de scans automaticos |
| ⚠️ **Confirmacao obrigatoria** | Operacoes irreversiveis requerem confirmacao            |
| 📝 **Audit log**               | Todas as acoes registradas em `.leviathan_audit.log`    |
| 🔒 **Safe defaults**           | Parametros defensivos em todas as ferramentas           |

Para desativar (sob sua total responsabilidade — voce foi avisado):
```bash
set LEVIATHAN_SAFE_MODE=0
```

## 🔴 Reportando Vulnerabilidades

Se voce encontrou uma vulnerabilidade **no Leviathan-VS** (nao nas ferramentas alvo):

1. **NAO abra issue publica** — isso expoe a vuln
2. 📧 Envie email para o maintainer ou use **GitHub Security Advisories**
3. 📋 Inclua: descricao, impacto, passos para reproduzir, PoC
4. ⏳ Aguarde resposta em ate **72 horas**

## 🎯 Escopo — O Que Consideramos Vulnerabilidade

### ✅ Em Escopo

| Vuln                             | Impacto                               |
| -------------------------------- | ------------------------------------- |
| 💉 **RCE via configs maliciosos** | Execucao de codigo arbitrario         |
| 🔑 **Leak de credenciais**        | Vazamento via logs ou output          |
| 🔓 **Bypass de SAFE_MODE**        | Sem flag explicito                    |
| ⚡ **MCP command injection**      | Servidores executando sem sanitizacao |
| 📂 **Path traversal**             | Acesso a arquivos fora do projeto     |

### ❌ Fora de Escopo

- Bugs em ferramentas externas (Frida, Ghidra, etc.)
- Uso indevido por operadores com acesso local
- Social engineering contra os mantenedores

## 📊 Versoes Suportadas

| Versao         | Suportada | Nivel de Suporte                        |
| -------------- | --------- | --------------------------------------- |
| 66.x (ABYSSAL) | ✅ Sim     | ☠️ Suporte total + patches de emergencia |
| 16.x           | ✅ Sim     | 🔧 Security patches apenas               |
| 15.x           | ⚠️ Parcial | Bug fixes criticos                      |
| < 15           | ❌ Nao     | Atualize imediatamente                  |
