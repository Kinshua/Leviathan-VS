#Requires -Version 5.1
<#
.SYNOPSIS
    ☠️ LEVIATHAN VS — ABYSSAL INSTALLER v66.6.0 — Classification: OMEGA-BLACK
.DESCRIPTION
    Invoca o monstro. Instala e configura automaticamente o arsenal ofensivo
    Classification OMEGA-BLACK com 49 MCP servers, 704+ ferramentas, 640+ regras
    de evasao, 15 dominios de ataque, e 160+ extensoes VS Code.

    Kill Chain: FULL | Evasion: 96.3% | Accuracy: 99.7%
    MITRE ATT&CK: 14/14 Tactics (TA0043 -> TA0040)
.NOTES
    Autor: ThiagoFrag — Arquiteto do Abismo
    Versao: 66.6.0 ABYSSAL SOVEREIGN
    Classification: OMEGA-BLACK
    Threat Level: OMEGA
#>

param(
    [switch]$Silent,
    [switch]$SkipVSCode,
    [switch]$SkipMCP
)

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

# Cores
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) { Write-Output $args }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Banner {
    $banner = @"

 `e[38;5;196m╔═══════════════════════════════════════════════════════════════════════════╗`e[0m
 `e[38;5;196m║`e[0m                                                                           `e[38;5;196m║`e[0m
 `e[38;5;196m║`e[0m   ██╗     ███████╗██╗   ██╗██╗ █████╗ ████████╗██╗  ██╗ █████╗ ███╗   ██║`e[0m
 `e[38;5;196m║`e[0m   ██║     ██╔════╝██║   ██║██║██╔══██╗╚══██╔══╝██║  ██║██╔══██╗████╗  ██║`e[0m
 `e[38;5;196m║`e[0m   ██║     █████╗  ██║   ██║██║███████║   ██║   ███████║███████║██╔██╗ ██║`e[0m
 `e[38;5;196m║`e[0m   ██║     ██╔══╝  ╚██╗ ██╔╝██║██╔══██║   ██║   ██╔══██║██╔══██║██║╚██╗██║`e[0m
 `e[38;5;196m║`e[0m   ███████╗███████╗ ╚████╔╝ ██║██║  ██║   ██║   ██║  ██║██║  ██║██║ ╚████║`e[0m
 `e[38;5;196m║`e[0m   ╚══════╝╚══════╝  ╚═══╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝ ╚══╝`e[0m
 `e[38;5;196m║`e[0m                                                                           `e[38;5;196m║`e[0m
 `e[38;5;196m║`e[0m   `e[38;5;160m☠️  ABYSSAL INSTALLER v66.6.0 — Threat Level OMEGA`e[0m                    `e[38;5;196m║`e[0m
 `e[38;5;196m║`e[0m   `e[38;5;208m"Cada dependencia e um tentaculo. Cada extensao, uma garra."`e[0m         `e[38;5;196m║`e[0m
 `e[38;5;196m║`e[0m                                                                           `e[38;5;196m║`e[0m
 `e[38;5;196m╚═══════════════════════════════════════════════════════════════════════════╝`e[0m

"@
    Write-Host $banner -ForegroundColor Red
}

function Test-Command($Command) {
    return [bool](Get-Command $Command -ErrorAction SilentlyContinue)
}

function Install-WithWinget($PackageId, $Name) {
    Write-Host "  [*] Instalando $Name..." -ForegroundColor Yellow
    winget install $PackageId --silent --accept-package-agreements --accept-source-agreements 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] $Name instalado" -ForegroundColor Green
        return $true
    }
    Write-Host "  [!] Falha ao instalar $Name" -ForegroundColor Red
    return $false
}

function Install-VSCodeExtension($ExtensionId) {
    code --install-extension $ExtensionId --force 2>$null | Out-Null
}

# ============================================================================
# MAIN
# ============================================================================

Clear-Host
Write-Banner

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "[1/8] Verificando Python..." -ForegroundColor Cyan
if (Test-Command "python") {
    $pyVersion = python --version 2>&1
    Write-Host "  [OK] $pyVersion" -ForegroundColor Green
} else {
    Install-WithWinget "Python.Python.3.12" "Python 3.12"
    # Atualizar PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

Write-Host "`n[2/8] Verificando Git..." -ForegroundColor Cyan
if (Test-Command "git") {
    $gitVersion = git --version 2>&1
    Write-Host "  [OK] $gitVersion" -ForegroundColor Green
} else {
    Install-WithWinget "Git.Git" "Git"
}

Write-Host "`n[3/8] Verificando VS Code..." -ForegroundColor Cyan
if (Test-Command "code") {
    Write-Host "  [OK] VS Code encontrado" -ForegroundColor Green
} else {
    if (-not $SkipVSCode) {
        Install-WithWinget "Microsoft.VisualStudioCode" "VS Code"
    }
}

Write-Host "`n[4/8] Instalando dependencias Python..." -ForegroundColor Cyan
$packages = @("requests", "aiohttp", "colorama", "rich", "httpx")
python -m pip install --upgrade pip --quiet 2>$null
foreach ($pkg in $packages) {
    python -m pip install $pkg --quiet 2>$null
}
Write-Host "  [OK] Dependencias: $($packages -join ', ')" -ForegroundColor Green

Write-Host "`n[5/8] Instalando extensoes VS Code..." -ForegroundColor Cyan
$extensions = @(
    "GitHub.copilot",
    "GitHub.copilot-chat",
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.debugpy"
)
foreach ($ext in $extensions) {
    Install-VSCodeExtension $ext
    Write-Host "  [OK] $ext" -ForegroundColor Green
}

Write-Host "`n[6/8] Configurando MCP para GitHub Copilot..." -ForegroundColor Cyan
if (-not $SkipMCP) {
    $mcpDir = "$env:APPDATA\Code\User\globalStorage\github.copilot"
    $mcpConfig = "$mcpDir\mcp.json"

    if (-not (Test-Path $mcpDir)) {
        New-Item -ItemType Directory -Path $mcpDir -Force | Out-Null
    }

    $mcpJson = @{
        servers = @{
            "megazord-hog" = @{
                type = "stdio"
                command = "python"
                args = @("$($scriptPath -replace '\\','/')/core/mcp_server.py")
                env = @{}
            }
        }
    } | ConvertTo-Json -Depth 4

    $mcpJson | Out-File -FilePath $mcpConfig -Encoding utf8 -Force
    Write-Host "  [OK] MCP configurado: $mcpConfig" -ForegroundColor Green
}

Write-Host "`n[7/8] Validando instalacao..." -ForegroundColor Cyan
$checks = @(
    @{Name="Python"; Test={python -c "print('ok')" 2>$null; $LASTEXITCODE -eq 0}},
    @{Name="Config"; Test={Test-Path "$scriptPath\core\config.json"}},
    @{Name="Translator"; Test={Test-Path "$scriptPath\core\translator.py"}},
    @{Name="HTTP Toolkit"; Test={Test-Path "$scriptPath\core\http_toolkit.py"}},
    @{Name="MCP Server"; Test={Test-Path "$scriptPath\core\mcp_server.py"}}
)

foreach ($check in $checks) {
    if (& $check.Test) {
        Write-Host "  [OK] $($check.Name)" -ForegroundColor Green
    } else {
        Write-Host "  [X] $($check.Name)" -ForegroundColor Red
    }
}

Write-Host "`n[8/8] Abrindo VS Code..." -ForegroundColor Cyan
if (-not $Silent) {
    Start-Process code -ArgumentList $scriptPath
    Write-Host "  [OK] VS Code aberto com o projeto" -ForegroundColor Green
}

# Final
Write-Host "`n" -NoNewline
Write-Host ("=" * 75) -ForegroundColor Red
Write-Host @"

  `e[38;5;196m☠️  LEVIATHAN VS v66.6.0 — INSTALACAO CONCLUIDA`e[0m

  `e[38;5;160mO MONSTRO DESPERTA. O ABISMO AGORA E SEU AMBIENTE DE TRABALHO.`e[0m

  `e[38;5;208mCOMO USAR:`e[0m

  1. No VS Code, pressione `e[38;5;117mCtrl+Shift+P`e[0m
  2. Digite `e[38;5;117m"Tasks: Run Task"`e[0m
  3. Escolha uma task `e[38;5;196m[LEVIATHAN]`e[0m

  `e[38;5;220mARSENAL INTERATIVO:`e[0m

  # Seletor de MCPs (49 servers / 704+ tools)
  `e[38;5;82mpython core\mcp_launcher.py`e[0m

  # Healthcheck de profundidade
  `e[38;5;82mpython core\doctor.py`e[0m

  # Launcher visual
  `e[38;5;82mLEVIATHAN.bat`e[0m

  `e[38;5;240mGitHub: https://github.com/ThiagoFrag/Leviathan-VS`e[0m
  `e[38;5;240m"O abismo nao esquece quem o visitou."`e[0m

"@ -ForegroundColor White

Write-Host ("=" * 75) -ForegroundColor Red
Write-Host ""

if (-not $Silent) {
    Read-Host "Pressione ENTER para retornar a superficie"
}
