import os
from PIL import Image, ImageDraw, ImageFont
import itertools

# ✅ Lista squadre con colori principali
squadre = {
    "Atalanta": [(0, 0, 0), (0, 0, 255)],
    "Bologna": [(153, 0, 0), (0, 0, 153)],
    "Cagliari": [(178, 34, 34), (0, 0, 139)],
    "Como": [(30, 144, 255)],
    "Empoli": [(0, 191, 255)],
    "Fiorentina": [(138, 43, 226)],
    "Frosinone": [(255, 255, 0)],
    "Genoa": [(220, 20, 60), (0, 0, 139)],
    "Verona": [(255, 255, 0), (0, 0, 139)],
    "Inter": [(0, 51, 153), (0, 0, 0)],
    "Juventus": [(255, 255, 255), (0, 0, 0)],
    "Lazio": [(135, 206, 235), (255, 255, 255)],
    "Lecce": [(255, 215, 0), (255, 0, 0)],
    "Milan": [(255, 0, 0), (0, 0, 0)],
    "Monza": [(255, 0, 0)],
    "Napoli": [(0, 102, 204)],
    "Roma": [(212, 175, 55), (128, 0, 0)],
    "Torino": [(128, 0, 32)],
    "Udinese": [(192, 192, 192), (0, 0, 0)],
    "Venezia": [(0, 128, 0), (255, 165, 0), (0, 0, 0)],
    "Parma": [(255, 221, 51), (0, 51, 153)]
}

# ✅ Crea cartelle se non esistono
os.makedirs("output", exist_ok=True)
os.makedirs("partite", exist_ok=True)

# ✅ Dimensioni immagine
larghezza = 200
altezza = 100
spessore_linea = 2  # Spessore linea bianca centrale

# ✅ Funzioni

# Ottieni iniziali della squadra
def iniziale(squadra):
    return ''.join([word[0].upper() for word in squadra.split()])

# Ottieni il font corretto che sta nell'area
def ottieni_font(draw, iniziali, larghezza_area, altezza_area, max_font_size=20):
    font_size = max_font_size
    font = ImageFont.truetype("arial.ttf", font_size)

    text_bbox = draw.textbbox((0, 0), iniziali, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    while text_width > larghezza_area - 10 or text_height > altezza_area - 10:
        font_size -= 1
        font = ImageFont.truetype("arial.ttf", font_size)
        text_bbox = draw.textbbox((0, 0), iniziali, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

    return font

# Carica e ridimensiona il logo
def carica_logo(nome_squadra, dimensione_logo=(40, 40)):  # Dimensione predefinita per il logo
    percorso_logo = os.path.join("loghi", f"{nome_squadra}.png")
    if not os.path.exists(percorso_logo):
        return None  # Logo non trovato
    logo = Image.open(percorso_logo).convert("RGBA")
    logo = logo.resize(dimensione_logo, Image.LANCZOS)  # Ridimensiona il logo
    return logo

# Aggiungi il logo o le iniziali
def aggiungi_logo_o_iniziali(img, draw, squadra, posizione_x, posizione_y, larghezza, altezza, dimensione_logo=(40, 40)):
    logo = carica_logo(squadra, dimensione_logo)  # Passa dimensione_logo
    if logo:
        posizione_logo = (
            posizione_x + (larghezza - logo.width) // 2,
            posizione_y + (altezza - logo.height) // 2
        )
        img.paste(logo, posizione_logo, logo)  # Usa alfa del logo
    else:
        iniziali = iniziale(squadra)
        font = ottieni_font(draw, iniziali, larghezza, altezza)
        text_bbox = draw.textbbox((posizione_x, posizione_y), iniziali, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        position = (posizione_x + (larghezza // 2 - text_width // 2), posizione_y + (altezza // 2 - text_height // 2))
        # Ombra nera
        draw.text((position[0] - 1, position[1] - 1), iniziali, font=font, fill=(0, 0, 0))
        draw.text((position[0] + 1, position[1] - 1), iniziali, font=font, fill=(0, 0, 0))
        draw.text((position[0] - 1, position[1] + 1), iniziali, font=font, fill=(0, 0, 0))
        draw.text((position[0] + 1, position[1] + 1), iniziali, font=font, fill=(0, 0, 0))
        # Testo bianco
        draw.text(position, iniziali, font=font, fill=(255, 255, 255))

# ✅ Generazione immagini
for casa, trasferta in itertools.permutations(squadre.keys(), 2):
    img = Image.new("RGB", (larghezza, altezza), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Colori squadra casa
    colori_casa = squadre[casa]
    if len(colori_casa) == 1:
        draw.rectangle([(0, 0), (larghezza // 2, altezza)], fill=colori_casa[0])
    else:
        draw.rectangle([(0, 0), (larghezza // 4, altezza)], fill=colori_casa[0])
        draw.rectangle([(larghezza // 4, 0), (larghezza // 2, altezza)], fill=colori_casa[1])

    # Colori squadra trasferta
    colori_trasferta = squadre[trasferta]
    if len(colori_trasferta) == 1:
        draw.rectangle([(larghezza // 2, 0), (larghezza, altezza)], fill=colori_trasferta[0])
    else:
        draw.rectangle([(larghezza // 2, 0), (larghezza * 3 // 4, altezza)], fill=colori_trasferta[0])
        draw.rectangle([(larghezza * 3 // 4, 0), (larghezza, altezza)], fill=colori_trasferta[1])

    # Linea bianca centrale
    draw.line([(larghezza // 2, 0), (larghezza // 2, altezza)], fill=(255, 255, 255), width=spessore_linea)

    # Aggiungi logo o iniziali
    dimensione_logo = (60, 60)  # Dimensione desiderata per il logo
    aggiungi_logo_o_iniziali(img, draw, casa, 0, 0, larghezza // 2, altezza, dimensione_logo)
    aggiungi_logo_o_iniziali(img, draw, trasferta, larghezza // 2, 0, larghezza // 2, altezza, dimensione_logo)

    # Cornice esterna
    # draw.rectangle([(0, 0), (larghezza - 1, altezza - 1)], outline=(255, 255, 255), width=spessore_linea)

    # Nome file
    nome_file = f"{casa.lower().replace(' ', '_')}_vs_{trasferta.lower().replace(' ', '_')}.png"

    # Salva immagine
    img.save(os.path.join("partite", nome_file))

print("✅ Tutte le immagini generate nella cartella 'partite'!")