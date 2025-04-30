from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def stickman_dancing(images: list[BuildImage], texts, args):
    self_head = images[0].convert("RGBA").circle().resize((138, 138))

    # fmt: off
    locs = [
        (194, 53), (194, 53), (194, 52), (195, 52),
        (196, 52), (197, 52), (198, 51), (199, 51),
        (200, 51), (201, 51), (201, 52), (202, 53),
        (200, 53), (198, 54), (196, 54), (194, 54),
        (192, 55), (190, 55), (190, 54), (192, 53),
        (194, 53), (194, 52), (195, 52), (196, 52),
        (195, 52), (194, 52), (194, 53), (193, 53),
        (192, 53), (191, 53), (191, 54), (190, 54),
        (189, 54), (190, 54), (191, 54), (192, 53),
        (192, 53), (193, 53), (194, 53), (194, 52),
        (195, 52), (196, 52), (195, 52), (194, 52),
        (193, 53), (193, 53), (192, 53), (191, 54),
        (190, 54), (190, 54), (190, 54), (191, 54),
        (191, 53), (192, 53), (193, 53), (194, 53),
        (194, 52), (195, 52), (196, 52), (196, 52),
        (197, 52), (198, 51), (199, 51), (200, 51),
        (201, 51), (200, 52), (201, 52), (202, 53),
        (199, 53), (197, 54), (195, 54), (193, 54),
        (191, 55), (190, 54), (192, 53), (194, 53),
        (194, 52), (195, 52), (196, 52), (197, 52),
        (198, 51), (199, 51), (200, 51), (201, 51),
        (201, 52), (202, 53), (200, 53), (197, 54),
        (195, 54), (193, 54), (191, 55), (190, 54),
        (189, 58),
    ]
    # fmt: on

    frames: list[IMG] = []
    for i in range(109):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(self_head, locs[i], alpha=True)
        frames.append(frame.image)

    return save_gif(frames, 0.03)


add_meme(
    "stickman_dancing",
    stickman_dancing,
    min_images=1,
    max_images=1,
    keywords=["跳舞", "火柴人跳舞"],
    tags=MemeTags.stickman,
    date_created=datetime(2025, 4, 30),
    date_modified=datetime(2025, 4, 30),
)
