#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved

from PIL import Image, ImageFont, ImageDraw
import pathlib
from cairosvg import svg2png


def run(df, file_name, price, tags):
    path = pathlib.Path(__file__).parent.resolve()
    barcode = df['BarCode'].values[0]
    title = df['Περιγραφή'].values[0]
    price = df[price].values[0]
    fMUCode = df['MM'].values[0]
    euro_price = int(price)
    # Διαίρεση με το 0 όταν η τιμή είναι 0.50 μας βγάζει σφάλμα έτσι το μετατρέπουμε σε 1
    copper_price = int(round(price % (euro_price if euro_price>0 else 1), 2) * 100)

    svg2png(url=f"{path}/svg/{barcode}.svg", write_to=f"{path}/svg/{barcode}.png", dpi=1200)
    my_image = Image.open(f'{path}/images/{file_name}')
    title_font = ImageFont.truetype('Times.ttc', 80)
    euro_font = ImageFont.truetype('Futura.ttc', 700)
    copper_font = ImageFont.truetype('Futura.ttc', 300)
    euro_sign_font = ImageFont.truetype('Futura.ttc', 400)
    fMUCode_font = ImageFont.truetype('Times.ttc', 98)
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((100, 80), title, (0, 0, 0), font=title_font)

    # BARCODE
    overlay = Image.open(f"{path}/svg/{barcode}.png").convert("RGBA")
    overlay = overlay.rotate(270, Image.NEAREST, expand=True)
    size = (overlay.size[0] // 4, overlay.size[1] // 4)
    overlay = overlay.resize(size, Image.ANTIALIAS)
    my_image.paste(overlay, (2250, 388), mask=overlay)

    # TAGS
    overlay = Image.open(f"{path}/images/{tags}.png").convert("RGBA")
    size = (overlay.size[0] // 1, overlay.size[1] // 1)
    overlay = overlay.resize(size, Image.ANTIALIAS)
    if len(str(euro_price)) == 1:
        image_editable.text((1346 - 40, 80),  str(euro_price) + ".", (244, 36, 7), font=euro_font)
        my_image.paste(overlay, (186 - 40, 211), mask=overlay)
    elif len(str(euro_price)) == 2:
        image_editable.text((930 - 40, 80),  str(euro_price) + ".", (244, 36, 7), font=euro_font)
        my_image.paste(overlay, (48 - 40, 211), mask=overlay)
    elif len(str(euro_price)) == 3:
        image_editable.text((555 - 40, 80),  str(euro_price) + ".", (244, 36, 7), font=euro_font)
        my_image.paste(overlay, (-212, 211), mask=overlay)
    # Εμφανίζει ένα δεκαδικό όταν η τιμή είναι π.χ. 1.0 έτσι προσθέτουμε ακόμα ένα 0
    image_editable.text((1755 - 40, 195), (str(copper_price) if len(str(copper_price)) == 2 else str(copper_price) + "0"), (244, 36, 7), font=copper_font)
    image_editable.text((2087 - 40, 340), "€", (244, 36, 7), font=euro_sign_font)
    image_editable.text((2141 - 40, 261), str(fMUCode).lower(), (0, 0, 0), font=fMUCode_font)

    my_image.save(f"{path}/merged_images/{barcode}.png")
