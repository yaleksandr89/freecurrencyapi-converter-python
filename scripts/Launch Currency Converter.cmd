@echo off
setlocal EnableExtensions DisableDelayedExpansion
set "ERRORLEVEL="
pushd "%~dp0" || exit /b 1
".\currency-converter.exe" %*
set "converter_status=%ERRORLEVEL%"
popd
echo Press Enter to close
set /p "close_input="
exit /b %converter_status%
