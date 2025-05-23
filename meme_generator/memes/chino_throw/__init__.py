from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def chino_throw(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square()
    frames: list[IMG] = []
    
    locs = [
        (133, 299, 372, 485, 240, 186),
        (133, 299, 372, 485, 240, 186),
        (133, 299, 372, 485, 240, 186),
        (133, 299, 372, 485, 240, 186),
        (133, 299, 372, 485, 240, 186),
        (93, 260, 343, 473, 250, 220),
        (74, 226, 308, 454, 234, 228),
        (95, 176, 331, 402, 236, 226),
        (95, 176, 331, 402, 236, 226),
        (70, 45, 208, 168, 138, 123),
        (104, 51, 232, 161, 128, 112),
        (126, 57, 229, 152, 103, 95),
        (49, 23, 238, 169, 190, 146),
        (0, 0, 144, 163, 142, 163),
        (0, 0, 500, 500, 500, 500),
        (0, 0, 500, 500, 500, 500),
        (0, 0, 500, 500, 500, 500),
        (0, 0, 500, 500, 500, 500),
        (0, 0, 500, 500, 500, 500),
        (0, 0, 500, 500, 500, 500),
        (0, 0, 500, 500, 500, 500),
    ]
    
    for i in range(21):
        frame = BuildImage.open(img_dir / f"{i}.png")
        x1, y1, x2, y2, w, h = locs[i]
        avatar_w, avatar_h = x2 - x1, y2 - y1
        frame.paste(img.resize((avatar_w, avatar_h)), (x1, y1), below=True)
        frames.append(frame.image)
    
    return save_gif(frames, 0.07)


add_meme(
    "chino_throw",
    chino_throw,
    min_images=1,
    max_images=1,
    keywords=["智乃扔", "智乃抛"],
    tags=MemeTags.kafu_chino,
    date_created=datetime(2025, 5, 23),
    date_modified=datetime(2025, 5, 23),
)
