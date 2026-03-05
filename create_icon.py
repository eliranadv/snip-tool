"""Generate a scissors-cutting-paper icon .ico file."""
from PIL import Image, ImageDraw


def _draw_icon(d, size):
    """Draw the scissors + dashed-rect icon on a given ImageDraw at `size`."""
    s = size / 64  # scale factor
    white = "#FFFFFF"

    # ── Blue circle background ──
    pad = max(1, int(2 * s))
    d.ellipse([pad, pad, size - pad - 1, size - pad - 1], fill="#1e88e5")

    # Gloss highlight (upper lighter blue)
    gh = int(28 * s)
    gp = int(8 * s)
    d.ellipse([pad + gp, pad + int(1 * s), size - pad - gp - 1, pad + gh],
              fill="#42a5f5")

    # ── Dashed selection rectangle ──
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

    # ── Scissors blades ──
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


def create_scissors_ico(path):
    sizes = [16, 24, 32, 48, 64, 128, 256]
    images = []

    for size in sizes:
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        _draw_icon(d, size)
        images.append(img)

    images[-1].save(path, format="ICO", sizes=[(sz, sz) for sz in sizes],
                    append_images=images[:-1])
    print(f"Icon saved: {path}")


if __name__ == "__main__":
    create_scissors_ico(r"C:\LLL\CLUDE\snip_tool.ico")
