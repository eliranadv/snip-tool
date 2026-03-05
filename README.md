# ✂ Snip Tool

A lightweight, fast screen snipping tool for Windows.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D6?logo=windows)

## Features

- **Free-drag selection** — Click and drag to capture any area of your screen
- **Multi-monitor support** — Works across all connected displays
- **Instant clipboard copy** — Snip is copied to clipboard automatically (Ctrl+V to paste)
- **Save to Downloads** — One-click save to your Downloads folder
- **Custom filename** — Edit the filename before saving
- **New Snip button** — Quickly take another screenshot without restarting
- **Open in viewer** — Open the saved snip directly from the app
- **Dimmed overlay** — Screen dims while selecting, with a bright preview of the selected area
- **Size indicator** — Shows pixel dimensions while dragging
- **Catppuccin Mocha theme** — Dark, modern UI design
- **Silent VBS launcher** — No console window flash on startup
- **Custom scissors icon** — Professional icon for taskbar pinning
- **Windows 11 compatible** — Per-Monitor DPI awareness, AppUserModelID support

## How It Works

1. Launch the app — screen dims slightly with a crosshair cursor
2. Drag to select the area you want to capture
3. Release — image is saved & copied to clipboard
4. A compact result window shows a preview with action buttons:
   - **✂ New** — Take another snip
   - **⬇** — Save to Downloads folder (with optional custom filename)
   - **🖼 Open** — Open the snip image
   - **✕** — Close

Press **ESC** to cancel at any time.

## Installation

### Requirements

- Python 3.10+
- Windows 10/11

### Setup

```bash
git clone https://github.com/eliranadv/snip-tool.git
cd snip-tool
pip install Pillow pywin32
```

### Run

Double-click `Snip Tool.vbs` (silent, no console flash) or run:

```bash
pythonw snip_tool.pyw
```

### Pin to Taskbar

Drag `Snip Tool.lnk` to your taskbar.

## Files

| File | Description |
|------|-------------|
| `snip_tool.pyw` | Main application |
| `snip_tool.ico` | Scissors icon for taskbar |
| `Snip Tool.vbs` | Silent launcher (no console flash) |

## License

MIT
