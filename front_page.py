from PIL import Image, ImageDraw
from config import WIDTH, HEIGHT, COLORS, PADDING
from utils.fonts import load_font
from utils.utils import (
    crear_base_con_textura,
    dibujar_chip,
    dibujar_footer,
    insertar_logo,
    draw_wrapped_text  # ✅ nueva utilidad para textos multilínea centrados
)

def portada_carrusel(titulo, categoria, output="mazabyte_portada.png", color_texto="texto"):
    base = crear_base_con_textura()
    draw = ImageDraw.Draw(base)

    font_chip = load_font("arialbd.ttf", 30)
    font_title = load_font("arialbd.ttf", 84)
    font_swipe = load_font("arial.ttf", 32)
    font_footer = load_font("arial.ttf", 28)

    # Chip de categoría
    dibujar_chip(draw, categoria, font_chip, PADDING, 40)

    # --- Título centrado con envoltura automática
    y = 320
    max_width = WIDTH - 2 * PADDING
    # Usa el color del texto recibido
    draw_wrapped_text(draw, titulo, font_title, COLORS.get(color_texto, COLORS["texto"]), box=(PADDING, y, max_width), center=True)

    # --- Indicador “Desliza”
    mensaje = "→ Desliza para aprender"
    swipe_w = draw.textlength(mensaje, font=font_swipe)
    draw.text(((WIDTH - swipe_w) / 2, HEIGHT - 180), mensaje, font=font_swipe, fill=COLORS["chip_text"])

    dibujar_footer(draw, font_footer)
    insertar_logo(base)

    base.convert("RGB").save(output)
    print(f"✅ Imagen de portada generada: {output}")
