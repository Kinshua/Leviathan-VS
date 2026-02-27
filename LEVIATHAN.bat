@echo off
chcp 65001 >nul
title LEVIATHAN VS — O Abismo Aguarda
color 0B

:menu
cls
echo.
echo    ██╗     ███████╗██╗   ██╗██╗ █████╗ ████████╗██╗  ██╗ █████╗ ███╗   ██╗
echo    ██║     ██╔════╝██║   ██║██║██╔══██╗╚══██╔══╝██║  ██║██╔══██╗████╗  ██║
echo    ██║     █████╗  ██║   ██║██║███████║   ██║   ███████║███████║██╔██╗ ██║
echo    ██║     ██╔══╝  ╚██╗ ██╔╝██║██╔══██║   ██║   ██╔══██║██╔══██║██║╚██╗██║
echo    ███████╗███████╗ ╚████╔╝ ██║██║  ██║   ██║   ██║  ██║██║  ██║██║ ╚████║
echo    ╚══════╝╚══════╝  ╚═══╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
echo.
echo                     [ Ambiente VS Code para as Profundezas ]
echo.
echo    ═══════════════════════════════════════════════════════════════════════
echo.
echo    [1] SUBMERGIR   - Encodar (sanitizar codigo)
echo    [2] EMERGIR     - Restaurar (decodar codigo)
echo    [3] ESCANEAR    - Preview das mudancas
echo    [4] CACAR       - Estatisticas
echo    [5] ECO         - Historico
echo    [6] PROFUNDEZAS - Modo interativo
echo    [7] VALIDAR     - Checar configuracao
echo    [8] MCP ARSENAL - Abrir seletor de MCPs (49 servers / 704+ tools)
echo    [9] SAIR        - Retornar a superficie
echo.
echo    ═══════════════════════════════════════════════════════════════════════
echo.

set /p choice="    Entrar nas profundezas [1-9]: "

if "%choice%"=="1" goto encode
if "%choice%"=="2" goto decode
if "%choice%"=="3" goto preview
if "%choice%"=="4" goto stats
if "%choice%"=="5" goto history
if "%choice%"=="6" goto interactive
if "%choice%"=="7" goto validate
if "%choice%"=="8" goto launcher
if "%choice%"=="9" goto exit
goto menu

:encode
echo.
echo    [LEVIATHAN] Submergindo codigo no abismo...
python core\translator.py encode
pause
goto menu

:decode
echo.
echo    [LEVIATHAN] Emergindo com termos originais...
python core\translator.py restore
pause
goto menu

:preview
echo.
echo    [LEVIATHAN] Escaneando as aguas...
python core\translator.py preview
pause
goto menu

:stats
echo.
echo    [LEVIATHAN] Relatorio de profundidade...
python core\translator.py stats
pause
goto menu

:history
echo.
echo    [LEVIATHAN] Eco das profundezas...
python core\translator.py history
pause
goto menu

:interactive
echo.
echo    [LEVIATHAN] Entrando no abismo...
python core\translator.py interactive
pause
goto menu

:validate
echo.
echo    [LEVIATHAN] Validando configuracao do covil...
python core\translator.py validate
pause
goto menu

:launcher
echo.
echo    [LEVIATHAN] Abrindo Arsenal MCP...
python core\mcp_launcher.py
pause
goto menu

:exit
echo.
echo    [LEVIATHAN] Retornando a superficie...
timeout /t 2 >nul
exit
