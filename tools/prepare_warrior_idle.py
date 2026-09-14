"""Convert the supplied chroma-key warrior GIF into a transparent canvas sprite.

The site uses the resulting strip as a scroll-driven sprite, rather than
autoplaying the GIF, so the character moves only while the visitor scrolls the
hero panel.
"""

from pathlib import Path

from PIL import Image, ImageSequence


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "static" / "img" / "warrior-idle-source.gif"
DESTINATION = ROOT / "static" / "img" / "warrior-idle-sprite.webp"
COLUMNS = 6
OUTPUT_SIZE = (640, 360)


def key_green(frame: Image.Image) -> Image.Image:
    """Remove saturated chroma green while retaining anti-aliased ink edges."""
    rgba = frame.convert("RGBA")
    pixels = rgba.load()

    for y in range(rgba.height):
        for x in range(rgba.width):
            red, green, blue, alpha = pixels[x, y]
            foreground = max(red, blue)
            chroma = green - foreground
            if green > 50 and chroma > 20:
                # Remove the bright key and neutralise partially keyed pixels.
                # The latter avoids the green halo common on GIF edges.
                edge_alpha = int(max(0, min(255, (110 - chroma) / 70 * 255)))
                pixels[x, y] = (foreground, foreground, foreground, min(alpha, edge_alpha))

    return rgba


def main() -> None:
    source = Image.open(SOURCE)
    frames = [
        key_green(frame.copy()).resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)
        for frame in ImageSequence.Iterator(source)
    ]
    if not frames:
        raise RuntimeError("The source GIF did not contain any frames.")

    frame_width, frame_height = frames[0].size
    rows = (len(frames) + COLUMNS - 1) // COLUMNS
    sprite = Image.new("RGBA", (frame_width * COLUMNS, frame_height * rows))

    for index, frame in enumerate(frames):
        x = (index % COLUMNS) * frame_width
        y = (index // COLUMNS) * frame_height
        sprite.alpha_composite(frame, (x, y))

    sprite.save(DESTINATION, "WEBP", lossless=False, quality=94, method=4)
    print(f"{len(frames)} frames, {frame_width}x{frame_height}, {COLUMNS} columns")


if __name__ == "__main__":
    main()
