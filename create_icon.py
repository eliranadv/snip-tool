"""Generate a scissors-cutting-paper icon .ico file."""
from PIL import Image, ImageDraw


def create_scissors_ico(path):
    sizes = [16, 24, 32, 48, 64, 128, 256]
    images = []

    for size in sizes:
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        s = size / 64  # scale factor

        # Circle background
        pad = max(1, int(2 * s))
        d.ellipse([pad, pad, size - pad, size - pad],
                  fill="#1e1e2e", outline="#89b4fa", width=max(1, int(1.5 * s)))

        lw = max(2, int(2.5 * s))

        # Paper (white rectangle)
        d.rectangle([22 * s, 10 * s, 54 * s, 48 * s],
                    fill="#cdd6f4", outline="#9399b2", width=max(1, int(s)))

        # Dashed cut line
        cut_y = 28 * s
        dash_len = max(3, int(4 * s))
        for x in range(int(18 * s), int(56 * s), dash_len * 2):
            d.line([(x, cut_y), (min(x + dash_len, 56 * s), cut_y)],
                   fill="#f38ba8", width=max(1, int(1.2 * s)))

        # Scissors blades
        d.line([(10 * s, 22 * s), (36 * s, 34 * s)], fill="#89b4fa", width=lw)
        d.line([(10 * s, 38 * s), (36 * s, 24 * s)], fill="#89b4fa", width=lw)

        # Handle rings
        ring_r = 5 * s
        ring_lw = max(1, int(1.8 * s))
        d.ellipse([5 * s - ring_r, 19 * s - ring_r, 5 * s + ring_r, 19 * s + ring_r],
                  outline="#cba6f7", width=ring_lw)
        d.ellipse([5 * s - ring_r, 41 * s - ring_r, 5 * s + ring_r, 41 * s + ring_r],
                  outline="#cba6f7", width=ring_lw)

        # Pivot dot
        pr = max(2, int(2.5 * s))
        px, py = 22 * s, 29 * s
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill="#a6e3a1")

        images.append(img)

    images[-1].save(path, format="ICO", sizes=[(sz, sz) for sz in sizes],
                    append_images=images[:-1])
    print(f"Icon saved: {path}")


if __name__ == "__main__":
    create_scissors_ico(r"C:\LLL\CLUDE\snip_tool.ico")
