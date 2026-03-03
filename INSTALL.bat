@echo off
chcp 65001 >nul
title ☠️ LEVIATHAN VS — ABYSSAL INSTALLER v66.6.0 — Classification: OMEGA-BLACK
color 0C

echo.
echo [38;5;196m╔═══════════════════════════════════════════════════════════════════════════╗[0m
echo [38;5;196m║[0m                                                                           [38;5;196m║[0m
echo [38;5;196m║[0m   [38;5;196m██╗     ███████╗██╗   ██╗██╗ █████╗ ████████╗██╗  ██╗ █████╗ ███╗   ██║[0m
echo [38;5;196m║[0m   [38;5;196m██║     ██╔════╝██║   ██║██║██╔══██╗╚══██╔══╝██║  ██║██╔══██╗████╗  ██║[0m
echo [38;5;196m║[0m   [38;5;196m██║     █████╗  ██║   ██║██║███████║   ██║   ███████║███████║██╔██╗ ██║[0m
echo [38;5;196m║[0m   [38;5;196m██║     ██╔══╝  ╚██╗ ██╔╝██║██╔══██║   ██║   ██╔══██║██╔══██║██║╚██╗██║[0m
echo [38;5;196m║[0m   [38;5;196m███████╗███████╗ ╚████╔╝ ██║██║  ██║   ██║   ██║  ██║██║  ██║██║ ╚████║[0m
echo [38;5;196m║[0m   [38;5;196m╚══════╝╚══════╝  ╚═══╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝ ╚══╝[0m
echo [38;5;196m║[0m                                                                           [38;5;196m║[0m
echo [38;5;196m║[0m   [38;5;160m☠️  ABYSSAL INSTALLER v66.6.0 — Classification: OMEGA-BLACK[0m           [38;5;196m║[0m
echo [38;5;196m║[0m   [38;5;208m"Cada dependencia instalada e um tentaculo a mais no monstro."[0m       [38;5;196m║[0m
echo [38;5;196m║[0m                                                                           [38;5;196m║[0m
echo [38;5;196m║[0m   [38;5;82m49 MCPs[0m [38;5;117m704+ Tools[0m [38;5;220m640+ Rules[0m [38;5;141m160+ Ext[0m [38;5;196m15 Domains[0m [38;5;213m14 Tactics[0m   [38;5;196m║[0m
echo [38;5;196m║[0m                                                                           [38;5;196m║[0m
echo [38;5;196m╚═══════════════════════════════════════════════════════════════════════════╝[0m
echo.

:: Verificar se está rodando como admin
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Executando com privilegios de administrador
) else (
    echo [!] Recomendado: Execute como Administrador para instalacao completa
)

echo.
echo [1/8] Verificando Python...
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo [X] Python nao encontrado! Instalando via winget...
    winget install Python.Python.3.12 --silent --accept-package-agreements
    if %errorLevel% neq 0 (
        echo [ERRO] Falha ao instalar Python. Instale manualmente: https://python.org
        pause
        exit /b 1
    )
) else (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo [OK] %%i encontrado
)

echo.
echo [2/8] Verificando Git...
where git >nul 2>&1
if %errorLevel% neq 0 (
    echo [X] Git nao encontrado! Instalando via winget...
    winget install Git.Git --silent --accept-package-agreements
) else (
    for /f "tokens=*" %%i in ('git --version 2^>^&1') do echo [OK] %%i encontrado
)

echo.
echo [3/8] Verificando VS Code...
where code >nul 2>&1
if %errorLevel% neq 0 (
    echo [X] VS Code nao encontrado! Instalando via winget...
    winget install Microsoft.VisualStudioCode --silent --accept-package-agreements
) else (
    echo [OK] VS Code encontrado
)

echo.
echo [4/8] Instalando dependencias Python...
python -m pip install --upgrade pip --quiet
python -m pip install requests aiohttp colorama rich --quiet
echo [OK] Dependencias instaladas

echo.
echo [5/8] Configurando extensoes do VS Code...
call code --install-extension GitHub.copilot --force 2>nul
call code --install-extension ms-python.python --force 2>nul
call code --install-extension ms-python.vscode-pylance --force 2>nul
echo [OK] Extensoes configuradas

echo.
echo [6/8] Configurando MCP para GitHub Copilot...
set "MCP_CONFIG=%APPDATA%\Code\User\globalStorage\github.copilot\mcp.json"
set "MCP_DIR=%APPDATA%\Code\User\globalStorage\github.copilot"

if not exist "%MCP_DIR%" mkdir "%MCP_DIR%" 2>nul

:: Criar configuração MCP
echo { > "%MCP_CONFIG%"
echo   "servers": { >> "%MCP_CONFIG%"
echo     "megazord-hog": { >> "%MCP_CONFIG%"
echo       "type": "stdio", >> "%MCP_CONFIG%"
echo       "command": "python", >> "%MCP_CONFIG%"
echo       "args": ["%CD:\=/%/core/mcp_server.py"], >> "%MCP_CONFIG%"
echo       "env": {} >> "%MCP_CONFIG%"
echo     } >> "%MCP_CONFIG%"
echo   } >> "%MCP_CONFIG%"
echo } >> "%MCP_CONFIG%"
echo [OK] MCP configurado em: %MCP_CONFIG%

echo.
echo [7/8] Validando instalacao...
python -c "import json; print('[OK] JSON OK')" 2>nul || echo [X] Erro no modulo JSON
python -c "import urllib.request; print('[OK] HTTP OK')" 2>nul || echo [X] Erro no modulo HTTP
python core\translator.py validate >nul 2>&1 && echo [OK] Translator validado || echo [!] Translator precisa de config.json

echo.
echo [8/8] Abrindo VS Code com o projeto...
start "" code "%CD%"

echo.
echo [38;5;196m╔═══════════════════════════════════════════════════════════════════════════╗[0m
echo [38;5;196m║[0m              [38;5;82m☠️  INSTALACAO CONCLUIDA — O MONSTRO DESPERTA  ☠️[0m              [38;5;196m║[0m
echo [38;5;196m╠═══════════════════════════════════════════════════════════════════════════╣[0m
echo [38;5;196m║[0m                                                                           [38;5;196m║[0m
echo [38;5;196m║[0m   [38;5;208mCOMO USAR:[0m                                                              [38;5;196m║[0m
echo [38;5;196m║[0m                                                                           [38;5;196m║[0m
echo [38;5;196m║[0m   [38;5;82m1.[0m No VS Code: [38;5;117mCtrl+Shift+P[0m                                          [38;5;196m║[0m
echo [38;5;196m║[0m   [38;5;82m2.[0m Digite: [38;5;117m"Tasks: Run Task"[0m                                          [38;5;196m║[0m
echo [38;5;196m║[0m   [38;5;82m3.[0m Escolha uma task [38;5;196m[LEVIATHAN][0m para executar                        [38;5;196m║[0m
echo [38;5;196m║[0m                                                                           [38;5;196m║[0m
echo [38;5;196m║[0m   [38;5;220mARSENAL COMPLETO:[0m                                                      [38;5;196m║[0m
echo    [38;5;82m-[0m [38;5;117m[LEVIATHAN] ENCODE[0m     : KRAKEN ENGINE — sanitizar codigo
echo    [38;5;82m-[0m [38;5;117m[LEVIATHAN] RESTORE[0m    : Restaurar termos originais
echo    [38;5;82m-[0m [38;5;117m[LEVIATHAN] MCP ARSENAL[0m : Seletor interativo (49 servers)
echo    [38;5;82m-[0m [38;5;117m[LEVIATHAN] Status[0m     : Healthcheck de profundidade
echo.
echo    [38;5;141mMODO INTERATIVO:[0m
echo    [38;5;82mpython core\mcp_launcher.py[0m
echo.
echo    [38;5;240mGitHub: https://github.com/ThiagoFrag/Leviathan-VS[0m
echo [38;5;196m║[0m                                                                           [38;5;196m║[0m
echo [38;5;196m╚═══════════════════════════════════════════════════════════════════════════╝[0m
echo.
echo [38;5;160m"O abismo agora e seu ambiente de trabalho."[0m
echo.

pause
