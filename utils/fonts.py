from PIL import ImageFont

def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()
