from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def trolley(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle()
    frames: list[IMG] = []
    for i in range(50):
        frame = BuildImage.open(img_dir / f"{i}.png")
        angle = 0
        if i < 25:
            w, h, x, y = (65, 65, 21, 101)
        elif i < 28:
            w, h, x, y = [
                (65, 65, 0, 101),
                (65, 65, 0, 101),
                (65, 65, -21, 101),
            ][i - 25]
        elif 31 <= i < 44:
            w, h, x, y, angle = [
                (18, 18, 237, 25, 0),
                (18, 18, 215, 25, 0),
                (18, 18, 191, 25, 0),
                (18, 18, 169, 25, 0),
                (18, 18, 150, 25, 0),
                (18, 18, 129, 19, 20),
                (18, 18, 114, 16, 30),
                (18, 18, 92, 13, 40),
                (18, 18, 72, 9, 40),
                (18, 18, 51, 6, 80),
                (18, 18, 27, 7, 90),
                (18, 18, 1, 8, 90),
                (18, 18, -15, 8, 90),
            ][i - 31]
        else:
            frames.append(frame.image)
            continue
        frame.paste(img.resize((w, h)).rotate(angle), (x, y), alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme(
    "trolley",
    trolley,
    min_images=1,
    max_images=1,
    keywords=["推车"],
    date_created=datetime(2025, 4, 12),
    date_modified=datetime(2025, 4, 12),
)
