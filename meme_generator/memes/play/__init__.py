from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def play(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square()
    # fmt: off
    locs = [
        (180, 60, 100, 100), (184, 75, 100, 100), (183, 98, 100, 100),
        (179, 118, 110, 100), (156, 194, 150, 48), (178, 136, 122, 69),
        (175, 66, 122, 85), (170, 42, 130, 96), (175, 34, 118, 95),
        (179, 35, 110, 93), (180, 54, 102, 93), (183, 58, 97, 92),
        (174, 35, 120, 94), (179, 35, 109, 93), (181, 54, 101, 92),
        (182, 59, 98, 92), (183, 71, 90, 96), (180, 131, 92, 101)
    ]
    # fmt: on
    raw_frames: list[BuildImage] = [
        BuildImage.open(img_dir / f"{i}.png") for i in range(38)
    ]
    img_frames: list[BuildImage] = []
    for i in range(len(locs)):
        frame = raw_frames[i]
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        img_frames.append(frame)
    frames = (
        img_frames[0:12]
        + img_frames[0:12]
        + img_frames[0:8]
        + img_frames[12:18]
        + raw_frames[18:38]
    )
    frames = [frame.image for frame in frames]
    return save_gif(frames, 0.06)


add_meme(
    "play",
    play,
    min_images=1,
    max_images=1,
    keywords=["顶", "玩"],
    tags=MemeTags.capoo,
    date_created=datetime(2021, 10, 9),
    date_modified=datetime(2023, 2, 14),
)
