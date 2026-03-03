@echo off
chcp 65001 >nul
title ☠️ LEVIATHAN VS v66.6.0 — ABYSSAL SOVEREIGN — Threat Level OMEGA
color 0C

:menu
cls
echo.
echo    [38;5;196m▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
echo    ██                                                                       ██
echo    ██  ██╗     ███████╗██╗   ██╗██╗ █████╗ ████████╗██╗  ██╗ █████╗ ███╗   ██║
echo    ██  ██║     ██╔════╝██║   ██║██║██╔══██╗╚══██╔══╝██║  ██║██╔══██╗████╗  ██║
echo    ██  ██║     █████╗  ██║   ██║██║███████║   ██║   ███████║███████║██╔██╗ ██║
echo    ██  ██║     ██╔══╝  ╚██╗ ██╔╝██║██╔══██║   ██║   ██╔══██║██╔══██║██║╚██╗██║
echo    ██  ███████╗███████╗ ╚████╔╝ ██║██║  ██║   ██║   ██║  ██║██║  ██║██║ ╚████║
echo    ██  ╚══════╝╚══════╝  ╚═══╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
echo    ██                                                                       ██
echo    ██  [38;5;160m▓▓▓  V U L N E R A B I L I T Y   S O V E R E I G N T Y  ▓▓▓[38;5;196m       ██
echo    ██                                                                       ██
echo    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀[0m
echo.
echo    [38;5;160m╔══════════════════════════════════════════════════════════════╗[0m
echo    [38;5;160m║[0m  [38;5;196m☢️  THREAT LEVEL: [5m████████████████████[0m [38;5;196mOMEGA  ☢️[0m   [38;5;160m║[0m
echo    [38;5;160m╚══════════════════════════════════════════════════════════════╝[0m
echo.
echo    [38;5;160mv66.6.0 ABYSSAL SOVEREIGN[0m  ^|  [38;5;208m49 MCPs[0m  ^|  [38;5;82m704+ Tools[0m  ^|  [38;5;141m640+ Regras[0m
echo.
echo    [38;5;196m═══════════════════════════════════════════════════════════════[0m
echo.
echo    [38;5;196m[1][0m [38;5;208m⚔  SUBMERGIR[0m      — Encodar codigo (KRAKEN ENGINE)
echo    [38;5;196m[2][0m [38;5;82m🔄 EMERGIR[0m        — Restaurar termos originais
echo    [38;5;196m[3][0m [38;5;117m👁  RECONHECER[0m    — Preview sem alterar (recon passivo)
echo    [38;5;196m[4][0m [38;5;220m📊 INTELIGENCIA[0m   — Estatisticas de profundidade
echo    [38;5;196m[5][0m [38;5;141m💀 ECO ABISSAL[0m    — Historico de operacoes
echo    [38;5;196m[6][0m [38;5;213m🌊 PROFUNDEZAS[0m    — Modo interativo (operador)
echo    [38;5;196m[7][0m [38;5;43m🔍 DIAGNOSTICO[0m    — Validar configuracao de guerra
echo    [38;5;196m[8][0m [38;5;196m☠  MCP ARSENAL[0m    — Seletor de MCPs (49 servers / 704+ tools)
echo    [38;5;196m[9][0m [38;5;250m🏥 DOCTOR[0m         — Healthcheck de profundidade total
echo    [38;5;196m[0][0m [38;5;240m↑  SUPERFICIE[0m     — Retornar a superficie
echo.
echo    [38;5;196m═══════════════════════════════════════════════════════════════[0m
echo.

set /p choice="    [38;5;196m☠️[0m  Escolha sua profundidade [0-9]: "

if "%choice%"=="1" goto encode
if "%choice%"=="2" goto decode
if "%choice%"=="3" goto preview
if "%choice%"=="4" goto stats
if "%choice%"=="5" goto history
if "%choice%"=="6" goto interactive
if "%choice%"=="7" goto validate
if "%choice%"=="8" goto launcher
if "%choice%"=="9" goto doctor
if "%choice%"=="0" goto exit
goto menu

:encode
echo.
echo    [38;5;196m[LEVIATHAN][0m [38;5;208m⚔ Submergindo codigo no abismo — KRAKEN ENGINE ativado...[0m
python core\translator.py encode
pause
goto menu

:decode
echo.
echo    [38;5;82m[LEVIATHAN][0m [38;5;82m🔄 Emergindo com termos originais — decodificacao abissal...[0m
python core\translator.py restore
pause
goto menu

:preview
echo.
echo    [38;5;117m[LEVIATHAN][0m [38;5;117m👁 Reconhecimento passivo — escaneando as aguas...[0m
python core\translator.py preview
pause
goto menu

:stats
echo.
echo    [38;5;220m[LEVIATHAN][0m [38;5;220m📊 Relatorio de inteligencia de profundidade...[0m
python core\translator.py stats
pause
goto menu

:history
echo.
echo    [38;5;141m[LEVIATHAN][0m [38;5;141m💀 Eco do abismo — historico de operacoes...[0m
python core\translator.py history
pause
goto menu

:interactive
echo.
echo    [38;5;213m[LEVIATHAN][0m [38;5;213m🌊 Mergulhando nas profundezas — modo operador ativado...[0m
python core\translator.py interactive
pause
goto menu

:validate
echo.
echo    [38;5;43m[LEVIATHAN][0m [38;5;43m🔍 Validando configuracao do covil abissal...[0m
python core\translator.py validate
pause
goto menu

:launcher
echo.
echo    [38;5;196m[LEVIATHAN][0m [38;5;196m☠ Abrindo Arsenal MCP — 49 servers / 704+ ferramentas...[0m
python core\mcp_launcher.py
pause
goto menu

:doctor
echo.
echo    [38;5;250m[LEVIATHAN][0m [38;5;250m🏥 Diagnostico de profundidade — healthcheck total...[0m
python core\doctor.py
pause
goto menu

:exit
echo.
echo    [38;5;160m[LEVIATHAN][0m Retornando a superficie...
echo    [38;5;240m"O abismo nao esquece quem o visitou."[0m
timeout /t 2 >nul
exit
