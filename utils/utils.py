import os
from PIL import Image, ImageDraw
from config import WIDTH, HEIGHT, PADDING, COLORS, LOGO_PATH

def create_folder(ruta_base: str, nombre_carpeta: str) -> str:
    """
    Crea una carpeta con el nombre proporcionado dentro de la ruta especificada.

    Parámetros:
        ruta_base (str): Ruta donde se creará la carpeta.
        nombre_carpeta (str): Nombre de la nueva carpeta.

    Retorna:
        str: Ruta completa de la carpeta creada.
    """
    ruta_completa = os.path.join(ruta_base, nombre_carpeta)
    
    try:
        os.makedirs(ruta_completa, exist_ok=True)
        print(f"Carpeta creada en: {ruta_completa}")
    except Exception as e:
        print(f"Error al crear la carpeta: {e}")
    
    return ruta_completa



def crear_base_con_textura():
    base = Image.new("RGB", (WIDTH, HEIGHT), COLORS["fondo"])
    pattern = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)
    for x in range(0, WIDTH, 40):
        draw.line((x, 0, x - HEIGHT, HEIGHT), fill=(255, 255, 255, 10), width=1)
    return Image.alpha_composite(base.convert("RGBA"), pattern)

def dibujar_chip(draw, texto, font, x, y, padding=20):
    size = font.getbbox(texto)
    w, h = size[2] + padding * 2, size[3] + padding
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=COLORS["chip_bg"])
    draw.text((x + padding, y + 10), texto, font=font, fill=COLORS["chip_text"])

def dibujar_footer(draw, font):
    y = HEIGHT - 80
    draw.line((PADDING, y - 15, WIDTH - PADDING, y - 15), fill=COLORS["sombra"], width=1)
    draw.text((PADDING, y), "Mazabyte  •  @mazabyte.dev  •  #AprendeConMazabyte", font=font, fill=COLORS["texto"])

def insertar_logo(base):
    try:
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo = logo.resize((150, int(logo.height * (150 / logo.width))))
        base.paste(logo, (WIDTH - logo.width - PADDING, HEIGHT - logo.height - PADDING), logo)
    except FileNotFoundError:
        print("⚠️ Logo no encontrado:", LOGO_PATH)

def draw_wrapped_text(draw, text, font, fill, box, line_spacing=10, center=False):
    x, y, max_width = box
    words = text.split()
    line = ""
    lines = []

    for word in words:
        test_line = f"{line} {word}".strip()
        test_width = draw.textlength(test_line, font=font)
        if test_width <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)

    for line in lines:
        if center:
            text_width = draw.textlength(line, font=font)
            draw_x = x + (max_width - text_width) / 2
        else:
            draw_x = x
        draw.text((draw_x, y), line, font=font, fill=fill)
        y += font.getbbox("Ay")[3] + line_spacing

    return lines
