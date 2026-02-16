# ✂ Snip Tool

A lightweight screen snipping tool for Windows 11, built with Python and Tkinter.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D6?logo=windows)

## Features

- **Drag to snip** - Click and drag to select any area on your screen
- **Instant clipboard copy** - Paste anywhere with `Ctrl+V` right after snipping
- **Save to Downloads** - One-click save to your Downloads folder
- **Live preview** - See the selected area highlighted in real-time with size indicator
- **Compact result window** - Preview your snip with quick action buttons
- **Taskbar ready** - Pin to Windows taskbar with a custom scissors icon
- **Windows 11 compatible** - Per-Monitor DPI awareness, AppUserModelID support

## Screenshot

1. Launch the app → screen dims slightly with a crosshair cursor
2. Drag to select the area you want to capture
3. Release → image is saved & copied to clipboard
4. A compact result window shows a preview with action buttons

## Installation

### Requirements

- Python 3.10+
- Windows 10/11

### Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/snip-tool.git
cd snip-tool

# Install dependencies
pip install Pillow pywin32

# Run
pythonw snip_tool.pyw
```

### Pin to Taskbar

```bash
# Run the shortcut creator
cscript create_shortcut.vbs
```

Then search **"Snip Tool"** in the Start menu → Right-click → **Pin to taskbar**.

## Files

| File | Description |
|------|-------------|
| `snip_tool.pyw` | Main application |
| `snip_tool.ico` | Scissors icon for taskbar |
| `create_icon.py` | Script to regenerate the icon |
| `create_shortcut.vbs` | Creates Desktop & Start Menu shortcuts |

## How It Works

1. Takes a full screenshot before showing the overlay
2. Displays a dimmed version of the screenshot
3. As you drag, the selected area is shown at full brightness
4. On release, crops from the pre-captured screenshot (no overlay artifacts)
5. Copies to clipboard using `win32clipboard` and saves to `~/Pictures/Snips/`

## License

MIT
