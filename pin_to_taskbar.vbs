Set WshShell = WScript.CreateObject("WScript.Shell")

appDir = "C:\LLL\CLUDE\NEWSNIP"
batFile = appDir & "\Snip Tool.bat"
icoFile = appDir & "\snip_tool.ico"

' Create in Start Menu (required for taskbar pinning)
startPath = WshShell.SpecialFolders("Programs")
Set lnk = WshShell.CreateShortcut(startPath & "\Snip Tool.lnk")
lnk.TargetPath = batFile
lnk.WorkingDirectory = appDir
lnk.IconLocation = icoFile & ", 0"
lnk.WindowStyle = 7
lnk.Description = "Screen Snip Tool"
lnk.Save

' Also create on Desktop
desktopPath = WshShell.SpecialFolders("Desktop")
Set lnk2 = WshShell.CreateShortcut(desktopPath & "\Snip Tool.lnk")
lnk2.TargetPath = batFile
lnk2.WorkingDirectory = appDir
lnk2.IconLocation = icoFile & ", 0"
lnk2.WindowStyle = 7
lnk2.Description = "Screen Snip Tool"
lnk2.Save

WScript.Echo "Done! Now:" & vbCrLf & vbCrLf & _
    "1. Click Start" & vbCrLf & _
    "2. Search: Snip Tool" & vbCrLf & _
    "3. Right-click -> Pin to taskbar"
