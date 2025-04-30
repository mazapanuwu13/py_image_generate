import json
from post import generar_post
from front_page import portada_carrusel
from cta import slide_cta

def main():
    # Cargar datos desde JSON
    with open("carrusel.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Portada
    p = data["portada"]
    portada_carrusel(
        titulo=p["titulo"],
        categoria=p["categoria"],
        output=p["output"],
        color_texto=p["color_texto"]
    )

    # Slides de contenido
    for idx, slide in enumerate(data["slides"], start=2):
        generar_post(
            titulo=slide["titulo"],
            contenido=slide["contenido"],
            categoria=slide["categoria"],
            output=f"solid_slide_{idx}_post.png",
            color_texto=slide["color_texto"]
        )

    # CTA
    c = data["cta"]
    slide_cta(
        bloque1=c["bloque1"],
        bloque2=c["bloque2"],
        bloque3=c["bloque3"],
        output=c["output"],
        color_texto=c["color_texto"]
    )

if __name__ == "__main__":
    main()
