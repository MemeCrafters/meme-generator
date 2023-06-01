from pil_utils import BuildImage
from typing import List

from meme_generator import add_meme,MemeArgsModel

from pathlib import Path

img_dir = Path(__file__).parent / "images"

def OSHI_NO_KO(images: List[BuildImage], texts, args: MemeArgsModel):
    img = images[0]
    img = img.convert('RGBA').resize_width(691)
    print(texts)
    if texts:
        text = texts[0]
    else:
        text = args.user_infos[0].name
        if len(text)>2:
            text = text[0:2]
    
    frame = BuildImage.open(img_dir/'0.png')
    frame.paste(img, (0,0), alpha = True,below = True)
    frame.draw_text((433,28,589,184),text,fontsize=76, max_fontsize=80, min_fontsize=60, stroke_ratio = 0.1,stroke_fill = 'white')
    return frame.save_jpg()


add_meme(
    "oshi_no_zo",
    OSHI_NO_KO,
    min_images=1,
    max_images=1,
    max_texts=1,
    default_texts=["网友"],
    keywords=["我推的网友"],
)