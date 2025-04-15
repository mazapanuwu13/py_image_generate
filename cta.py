from PIL import Image, ImageDraw
from config import WIDTH, HEIGHT, PADDING, COLORS
from utils.fonts import load_font
from utils.utils import crear_base_con_textura, dibujar_footer, insertar_logo, draw_wrapped_text

def slide_cta(bloque1, bloque2, bloque3, output="mazabyte_slide_cta.png", color_texto="texto"):
    base = crear_base_con_textura()
    draw = ImageDraw.Draw(base)

    # --- Fuentes
    font_main = load_font("arialbd.ttf", 64)
    font_secondary = load_font("arial.ttf", 50)
    font_tertiary = load_font("arial.ttf", 42)
    font_footer = load_font("arial.ttf", 28)

    # --- Configuración inicial
    y = 240
    max_width = WIDTH - 2 * PADDING
    # Se obtiene el color de texto a partir de la llave pasada
    texto_color = COLORS.get(color_texto, COLORS["texto"])

    # --- Bloque 1: título centrado
    lines_1 = draw_wrapped_text(draw, bloque1, font_main, texto_color, box=(PADDING, y, max_width), center=True)
    y += len(lines_1) * (font_main.getbbox("Ay")[3] + 20) + 40

    # --- Bloque 2: subtítulo centrado
    lines_2 = draw_wrapped_text(draw, bloque2, font_secondary, texto_color, box=(PADDING, y, max_width - 100), center=True)
    y += len(lines_2) * (font_secondary.getbbox("Ay")[3] + 20) + 40

    # --- Bloque 3: alineado a la izquierda (concentrado en centro: si se requiere otra alineación, se ajusta el parámetro center)
    draw_wrapped_text(draw, bloque3, font_tertiary, texto_color, box=(PADDING, y, max_width), center=True)

    # --- Footer y logo
    dibujar_footer(draw, font_footer)
    insertar_logo(base)

    base.convert("RGB").save(output)
    print(f"✅ Slide CTA generado: {output}")
