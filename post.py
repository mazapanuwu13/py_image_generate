from PIL import Image, ImageDraw
from config import COLORS, WIDTH, HEIGHT, PADDING
from utils.fonts import load_font
from utils.utils import crear_base_con_textura, dibujar_chip, insertar_logo, dibujar_footer

def wrap_segmented_text(draw, segments, font, highlight_font, max_width):
    """
    segments es una lista de tuplas (text, color_key),
    donde color_key puede ser el nombre de una clave en COLORS o None.
    """
    lines, current_line, current_width = [], [], 0

    for text, color_key in segments:
        if text == "\n":
            # Cambio de línea forzado
            lines.append(current_line)
            current_line, current_width = [], 0
            continue

        # color_key puede ser algo como "coral", "chip_text", etc.
        # Si es None, luego se usará el color por defecto en dibujar_texto_contenido
        color = COLORS.get(color_key) if color_key else None

        for word in text.split(" "):
            word += " "
            fnt = highlight_font if color else font
            width = draw.textlength(word, font=fnt)

            if current_width + width > max_width:
                lines.append(current_line)
                current_line = [(word, color)]
                current_width = width
            else:
                current_line.append((word, color))
                current_width += width

    if current_line:
        lines.append(current_line)

    return lines

def dibujar_caja_contenido(base, box):
    """Dibuja una caja semitransparente (overlay) dentro del área 'box'."""
    from PIL import ImageDraw, Image
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    draw_overlay.rounded_rectangle(
        box, 
        radius=18, 
        fill=(255, 255, 255, 25),
        outline=COLORS["borde"], 
        width=2
    )
    return Image.alpha_composite(base, overlay)

def dibujar_texto_contenido(draw, lines, font_text, font_highlight, x, y, default_color):
    """
    Recorre las líneas devueltas por wrap_segmented_text y
    dibuja cada palabra con el color indicado o con el color por defecto.
    """
    for line in lines:
        curr_x = x
        for word, color in line:
            fnt = font_highlight if color else font_text
            fill = color if color else default_color
            draw.text((curr_x, y), word, font=fnt, fill=fill)
            curr_x += draw.textlength(word, font=fnt)
        # Avanzar en Y al terminar cada línea
        y += font_text.getbbox("Ay")[3] + 10

def generar_post(titulo, contenido, categoria, output="mazabyte_post.png", color_texto="texto"):
    """
    Genera una imagen con un título, un contenido segmentado (con estilos opcionales)
    y una categoría, permitiendo especificar un color de texto 'global' (color_texto).
    """
    # Área donde va el contenido
    CONTENT_BOX = (PADDING, 220, WIDTH - PADDING, 850)

    # Crear la base con textura y preparar draw
    base = crear_base_con_textura()
    draw = ImageDraw.Draw(base)

    # Cargar fuentes
    font_chip = load_font("arialbd.ttf", 30)
    font_title = load_font("arialbd.ttf", 74)
    font_text = load_font("arial.ttf", 40)
    font_footer = load_font("arial.ttf", 28)
    font_highlight = load_font("arialbd.ttf", 40)

    # Dibujar el chip (categoría) y el título
    dibujar_chip(draw, categoria, font_chip, PADDING, 30)
    # color_texto no se aplica al título en este ejemplo; se usa el color por defecto "texto"
    draw.text((PADDING, 120), titulo, font=font_title, fill=COLORS["texto"])

    # Dibuja una caja semitransparente detrás del contenido
    base = dibujar_caja_contenido(base, CONTENT_BOX)
    draw = ImageDraw.Draw(base)

    # Convertir el contenido a líneas segmentadas
    lines = wrap_segmented_text(
        draw, 
        contenido, 
        font_text, 
        font_highlight,
        CONTENT_BOX[2] - CONTENT_BOX[0] - 40  # ancho disponible
    )

    # color_texto = clave en COLORS; si no existe, usa COLORS["texto"]
    default_color = COLORS.get(color_texto, COLORS["texto"])

    # Dibujar el texto dentro de la caja, usando color_texto como color por defecto
    dibujar_texto_contenido(
        draw=draw, 
        lines=lines, 
        font_text=font_text, 
        font_highlight=font_highlight,
        x=CONTENT_BOX[0] + 20, 
        y=CONTENT_BOX[1] + 30, 
        default_color=default_color
    )

    # Footer y logo
    dibujar_footer(draw, font_footer)
    insertar_logo(base)

    # Guardar
    base.convert("RGB").save(output)
    print(f"✅ Imagen generada: {output}")
