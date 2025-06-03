from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from PIL.Image import Transpose
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def play_baseball(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((150, 150))
    ball_x = 0
    ball_v = 40
    ball_angle = 0
    frames: list[IMG] = []
    for i in range(20):
        frame = BuildImage.new("RGBA", (1000, 300))
        ball_x += ball_v
        ball_angle += -60 if ball_v > 0 else 60
        if ball_x >= 200:
            ball_x = 200
            ball_v = -ball_v
        elif ball_x <= -200:
            ball_x = -200
            ball_v = -ball_v
        frame.paste(img.rotate(ball_angle), (425 + ball_x, 120), alpha=True)
        right_index = i - 2 if i in [3, 4, 5, 6, 7] else 0
        left_index = i - 12 if i in [13, 14, 15, 16, 17] else 0
        right = BuildImage.open(img_dir / f"{right_index}.png")
        left = BuildImage.open(img_dir / f"{left_index}.png").transpose(
            Transpose.FLIP_LEFT_RIGHT
        )
        frame.paste(right, (630, 6), alpha=True)
        frame.paste(left, (0, 6), alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.08)


add_meme(
    "play_baseball",
    play_baseball,
    min_images=1,
    max_images=1,
    keywords=["打棒球"],
    tags=MemeTags.capoo,
    date_created=datetime(2025, 6, 3),
    date_modified=datetime(2025, 6, 3),
)
