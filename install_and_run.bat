@echo off
echo ============================================
echo    Snip Tool - Installing...
echo ============================================
pip install Pillow pywin32 >nul 2>&1
echo Done! Starting Snip Tool...
start "" pythonw "%~dp0snip_tool.pyw"
exit
