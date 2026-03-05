import tkinter as tk
import ctypes
import ctypes.wintypes
import io
import os
import datetime
import shutil
from PIL import ImageGrab, ImageTk, ImageEnhance, ImageDraw

# ── Windows 11 compatibility ──
# Set AppUserModelID so Windows treats this as its own app (for taskbar pinning)
APP_ID = "SnipTool.SnipTool.1.0"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

# DPI awareness (Per-Monitor V2 for Win11, fallback for older)
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ICO_PATH = os.path.join(SCRIPT_DIR, "snip_tool.ico")
SAVE_FOLDER = os.path.join(os.path.expanduser("~"), "Pictures", "Snips")
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
os.makedirs(SAVE_FOLDER, exist_ok=True)

# ── Colors (Catppuccin Mocha) ──
BG = "#1e1e2e"
BG2 = "#2a2a3d"
ACCENT = "#89b4fa"
GREEN = "#a6e3a1"
TEXT = "#cdd6f4"
SUBTLE = "#6c7086"
BTN_BG = "#313244"
BTN_HOVER = "#45475a"


def copy_to_clipboard(img):
    output = io.BytesIO()
    img.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    import win32clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


def create_scissors_icon(size=64):
    """Draw scissors + dashed-rect icon (blue circle, white elements)."""
    from PIL import Image as PILImage
    icon = PILImage.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(icon)
    s = size / 64
    white = "#FFFFFF"

    # Blue circle background
    pad = max(1, int(2 * s))
    d.ellipse([pad, pad, size - pad - 1, size - pad - 1], fill="#1e88e5")

    # Gloss highlight
    gh = int(28 * s)
    gp = int(8 * s)
    d.ellipse([pad + gp, pad + int(1 * s), size - pad - gp - 1, pad + gh],
              fill="#42a5f5")

    # Dashed selection rectangle
    rx1, ry1 = int(22 * s), int(14 * s)
    rx2, ry2 = int(54 * s), int(48 * s)
    dash = max(2, int(3.5 * s))
    dw = max(1, int(1.5 * s))

    for edge_start, edge_end, fixed, horizontal in [
        (rx1, rx2, ry1, True), (rx1, rx2, ry2, True),
        (ry1, ry2, rx1, False), (ry1, ry2, rx2, False),
    ]:
        pos = edge_start
        while pos < edge_end:
            end = min(pos + dash, edge_end)
            if horizontal:
                d.line([(pos, fixed), (end, fixed)], fill=white, width=dw)
            else:
                d.line([(fixed, pos), (fixed, end)], fill=white, width=dw)
            pos += dash * 2

    # Corner brackets
    cl = int(6 * s)
    cw = max(2, int(2.5 * s))
    for cx, cy, dx, dy in [
        (rx1, ry1, 1, 1), (rx2, ry1, -1, 1),
        (rx1, ry2, 1, -1), (rx2, ry2, -1, -1),
    ]:
        d.line([(cx, cy), (cx + dx * cl, cy)], fill=white, width=cw)
        d.line([(cx, cy), (cx, cy + dy * cl)], fill=white, width=cw)

    # Scissors blades
    bw = max(3, int(3.5 * s))
    d.line([(int(14 * s), int(20 * s)), (int(50 * s), int(38 * s))],
           fill=white, width=bw)
    d.line([(int(14 * s), int(44 * s)), (int(50 * s), int(26 * s))],
           fill=white, width=bw)

    # Handle rings
    rr = int(5.5 * s)
    rw = max(2, int(2.5 * s))
    for hx, hy in [(int(9 * s), int(16 * s)), (int(9 * s), int(48 * s))]:
        d.ellipse([hx - rr, hy - rr, hx + rr, hy + rr],
                  outline=white, width=rw)

    # Pivot dot
    pr = max(2, int(2 * s))
    px, py = int(30 * s), int(32 * s)
    d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=white)

    return icon


def get_virtual_screen():
    """Get the bounding box of all monitors combined."""
    user32 = ctypes.windll.user32
    left = user32.GetSystemMetrics(76)    # SM_XVIRTUALSCREEN
    top = user32.GetSystemMetrics(77)     # SM_YVIRTUALSCREEN
    width = user32.GetSystemMetrics(78)   # SM_CXVIRTUALSCREEN
    height = user32.GetSystemMetrics(79)  # SM_CYVIRTUALSCREEN
    return left, top, width, height


class SnipTool:
    def __init__(self):
        # Capture ALL screens
        self.screenshot = ImageGrab.grab(all_screens=True)
        self.scr_w, self.scr_h = self.screenshot.size

        # Get virtual screen offset (can be negative if monitor is to the left)
        self.virt_left, self.virt_top, _, _ = get_virtual_screen()

        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.geometry(f"{self.scr_w}x{self.scr_h}+{self.virt_left}+{self.virt_top}")

        self.canvas = tk.Canvas(self.root, cursor="cross", highlightthickness=0,
                                width=self.scr_w, height=self.scr_h)
        self.canvas.pack()

        dimmed = ImageEnhance.Brightness(self.screenshot).enhance(0.7)
        self.bg_photo = ImageTk.PhotoImage(dimmed)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        self.start_x = None
        self.start_y = None
        self.rect_id = None
        self.size_text = None
        self.bright_id = None
        self.bright_photo = None

        # Scissors icon in center
        self.scissors_img = create_scissors_icon(80)
        self.scissors_photo = ImageTk.PhotoImage(self.scissors_img)
        self.scissors_id = self.canvas.create_image(
            self.scr_w // 2, self.scr_h // 2 - 30,
            image=self.scissors_photo
        )

        # Header bar
        self.canvas.create_rectangle(0, 0, self.scr_w, 50, fill="#1e1e2e", stipple="gray50")
        self.canvas.create_text(
            self.scr_w // 2, 25,
            text="✂  Drag to snip  |  ESC to cancel",
            fill="#89b4fa", font=("Segoe UI", 13, "bold")
        )

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.scissors_id:
            self.canvas.delete(self.scissors_id)
            self.scissors_id = None

    def on_drag(self, event):
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        if self.size_text:
            self.canvas.delete(self.size_text)
        if self.bright_id:
            self.canvas.delete(self.bright_id)

        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)

        if x2 - x1 > 2 and y2 - y1 > 2:
            crop = self.screenshot.crop((x1, y1, x2, y2))
            self.bright_photo = ImageTk.PhotoImage(crop)
            self.bright_id = self.canvas.create_image(x1, y1, anchor=tk.NW, image=self.bright_photo)

        self.rect_id = self.canvas.create_rectangle(
            x1, y1, x2, y2, outline=ACCENT, width=2, dash=(6, 4)
        )

        w = x2 - x1
        h = y2 - y1
        self.size_text = self.canvas.create_text(
            x2, y1 - 10, text=f"{w} × {h}",
            anchor=tk.E, fill="white", font=("Segoe UI", 9, "bold")
        )

    def on_release(self, event):
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)

        if x2 - x1 < 5 or y2 - y1 < 5:
            return

        img = self.screenshot.crop((x1, y1, x2, y2))
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(SAVE_FOLDER, f"snip_{timestamp}.png")
        img.save(filepath)
        copy_to_clipboard(img)

        self.root.destroy()
        self.show_result(filepath, img)

    def show_result(self, filepath, snip_img):
        win = tk.Tk()
        win.title("Snip Tool")
        win.attributes("-topmost", True)
        win.configure(bg=BG)
        win.resizable(False, False)

        # Set icon
        if os.path.exists(ICO_PATH):
            win.iconbitmap(ICO_PATH)

        # ── Header (compact) ──
        header = tk.Frame(win, bg=BG2, height=44)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(header, text="✂", font=("Segoe UI", 16), bg=BG2, fg=ACCENT
                 ).pack(side=tk.LEFT, padx=(12, 4), pady=6)
        tk.Label(header, text="Snip Tool", font=("Segoe UI", 11, "bold"), bg=BG2, fg=TEXT
                 ).pack(side=tk.LEFT, pady=6)

        tk.Frame(win, bg=ACCENT, height=2).pack(fill=tk.X)

        # ── Preview (compact) ──
        preview_frame = tk.Frame(win, bg=BG, padx=12, pady=8)
        preview_frame.pack(fill=tk.X)

        pw, ph = snip_img.size
        max_w, max_h = 260, 140
        ratio = min(max_w / pw, max_h / ph, 1.0)
        preview_size = (max(1, int(pw * ratio)), max(1, int(ph * ratio)))
        from PIL import Image as PILImage
        preview_pil = snip_img.resize(preview_size, PILImage.LANCZOS)
        preview_photo = ImageTk.PhotoImage(preview_pil)

        preview_label = tk.Label(preview_frame, image=preview_photo, bg="#11111b",
                                 relief="solid", bd=1, highlightbackground="#45475a")
        preview_label.image = preview_photo
        preview_label.pack(pady=(0, 4))

        file_size = os.path.getsize(filepath)
        size_str = f"{file_size / 1024:.1f} KB" if file_size < 1048576 else f"{file_size / 1048576:.1f} MB"
        tk.Label(preview_frame, text=f"{pw}×{ph}  •  {size_str}",
                 font=("Segoe UI", 8), bg=BG, fg=SUBTLE).pack()

        # ── Status ──
        tk.Label(win, text="✓ Copied to clipboard  (Ctrl+V)",
                 font=("Segoe UI", 9, "bold"), bg=BG, fg=GREEN, padx=12, anchor=tk.W
                 ).pack(fill=tk.X, pady=(4, 6))

        tk.Frame(win, bg="#313244", height=1).pack(fill=tk.X, padx=12)

        # ── Buttons (compact row) ──
        btn_frame = tk.Frame(win, bg=BG, padx=12, pady=8)
        btn_frame.pack(fill=tk.X)

        dl_label = tk.Label(btn_frame, text="", font=("Segoe UI", 8), bg=BG, fg=GREEN)

        # Filename entry (editable, pre-filled with default name)
        default_name = os.path.splitext(os.path.basename(filepath))[0]
        name_entry = tk.Entry(
            btn_frame, font=("Segoe UI", 8), width=18,
            bg=BTN_BG, fg=TEXT, insertbackground=TEXT,
            relief="flat", highlightthickness=1,
            highlightbackground=SUBTLE, highlightcolor=ACCENT
        )
        name_entry.insert(0, default_name)
        name_entry.icursor(tk.END)

        def save_to_downloads():
            custom_name = name_entry.get().strip()
            if not custom_name:
                custom_name = default_name
            dest = os.path.join(DOWNLOADS_FOLDER, custom_name + ".png")
            shutil.copy2(filepath, dest)
            dl_label.config(text="✓ Saved!")

        def make_btn(parent, text, cmd, primary=False):
            return tk.Button(
                parent, text=text, font=("Segoe UI", 9, "bold" if primary else ""),
                bg=ACCENT if primary else BTN_BG,
                fg="#1e1e2e" if primary else TEXT,
                activebackground=BTN_HOVER, activeforeground=TEXT,
                relief="flat", cursor="hand2", padx=10, pady=3, command=cmd
            )

        def new_snip():
            win.destroy()
            SnipTool()
            tk.mainloop()

        make_btn(btn_frame, "✂ New", new_snip, True).pack(side=tk.LEFT, padx=(0, 4))
        name_entry.pack(side=tk.LEFT, padx=(0, 4), ipady=2)
        make_btn(btn_frame, "⬇", save_to_downloads).pack(side=tk.LEFT, padx=(0, 4))
        make_btn(btn_frame, "🖼 Open", lambda: os.startfile(filepath)).pack(side=tk.LEFT, padx=(0, 4))
        make_btn(btn_frame, "✕", win.destroy).pack(side=tk.RIGHT)
        dl_label.pack(side=tk.LEFT, padx=4)

        # Center on screen
        win.update_idletasks()
        sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
        ww, wh = win.winfo_width(), win.winfo_height()
        win.geometry(f"+{(sw - ww) // 2}+{(sh - wh) // 2}")

        win.mainloop()


if __name__ == "__main__":
    SnipTool()
    tk.mainloop()
