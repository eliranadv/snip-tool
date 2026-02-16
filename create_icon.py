"""Generate a high-quality scissors icon .ico file."""
from PIL import Image, ImageDraw

def create_scissors_ico(path):
    sizes = [16, 24, 32, 48, 64, 128, 256]
    images = []

    for s in sizes:
        img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)

        # Draw a filled circle background
        pad = max(1, s // 16)
        d.ellipse([pad, pad, s - pad, s - pad], fill="#1e1e2e", outline="#89b4fa", width=max(1, s // 24))

        cx, cy = s / 2, s / 2
        scale = s / 256  # base scale

        # Blade thickness
        lw = max(2, int(8 * scale))

        # Top point (where blades cross)
        top_y = cy - 38 * scale
        # Bottom spread
        spread = 42 * scale
        mid_y = cy + 5 * scale

        # Left blade line
        d.line([(cx - 2 * scale, top_y), (cx - spread, mid_y)], fill="#89b4fa", width=lw)
        # Right blade line
        d.line([(cx + 2 * scale, top_y), (cx + spread, mid_y)], fill="#89b4fa", width=lw)

        # Handle rings
        ring_r = 22 * scale
        ring_lw = max(2, int(6 * scale))

        # Left ring
        lx = cx - spread
        ly = mid_y + ring_r + 4 * scale
        d.ellipse([lx - ring_r, ly - ring_r, lx + ring_r, ly + ring_r],
                  outline="#cba6f7", width=ring_lw)

        # Right ring
        rx = cx + spread
        ry = ly
        d.ellipse([rx - ring_r, ry - ring_r, rx + ring_r, ry + ring_r],
                  outline="#cba6f7", width=ring_lw)

        # Pivot dot (green)
        pr = max(2, int(6 * scale))
        pivot_y = cy - 12 * scale
        d.ellipse([cx - pr, pivot_y - pr, cx + pr, pivot_y + pr], fill="#a6e3a1")

        images.append(img)

    images[-1].save(path, format="ICO", sizes=[(s, s) for s in sizes], append_images=images[:-1])
    print(f"Icon saved: {path}")

if __name__ == "__main__":
    create_scissors_ico(r"C:\LLL\CLUDE\snip_tool.ico")
