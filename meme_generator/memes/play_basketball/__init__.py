from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def play_basketball(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((77, 77))

    frames_info = [
        ((297, 321), 0),
        ((300, 327), -7.2),
        ((308, 410), -5),
        ((308, 412), -5),
        ((301, 355), 0),
        ((296, 317), 0),
        ((296, 320), 0),
        ((296, 320), 0),
        ((352, 435), 0),
        (None, None),
        (None, None),
        (None, None),
        (None, None),
        ((175, 343), -5),
        ((173, 353), -5),
        ((173, 353), -2),
        ((171, 354), -2),
        ((189, 158), 0),
        ((213, 149), 0),
        ((238, 139), 0),
        ((245, 139), 0),
        ((252, 139), 12),
        ((257, 142), 12),
        ((261, 142), 17),
        ((265, 145), 17),
        ((271, 148), 18),
        ((279, 156), 18),
        ((286, 163), 25),
        ((287, 160), 25),
        ((289, 159), 27),
        ((286, 165), 27),
        ((285, 167), 20),
        ((285, 179), 20),
        ((282, 192), -25),
        ((284, 219), -25),
        ((280, 242), -32),
        ((283, 280), -32),
        ((287, 315), -32),
    ]

    frames: list[IMG] = []
    for loc, rotation in frames_info:
        frame = BuildImage.open(img_dir / f"{len(frames)}.png")
        if loc is not None:
            x, y = loc
            current_img = img.copy()
            if rotation:
                current_img = current_img.rotate(
                    rotation, expand=True, fillcolor=(0, 0, 0, 0)
                )
            w, h = current_img.size
            pos = (x - w // 2, y - h // 2)
            frame.paste(current_img, pos, below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.08)


add_meme(
    "play_basketball",
    play_basketball,
    min_images=1,
    max_images=1,
    keywords=["打篮球", "火柴人打篮球"],
    tags=MemeTags.stickman,
    date_created=datetime(2025, 4, 30),
    date_modified=datetime(2025, 4, 30),
)
