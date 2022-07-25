from PIL import Image, ImageFont, ImageDraw
import pathlib
from cairosvg import svg2png


def run(df, file_name, price):
    path = pathlib.Path(__file__).parent.resolve()
    barcode = df['BarCode'].values[0]
    title = df['Περιγραφή'].values[0]
    price = df[price].values[0]
    fMUCode = df['MM'].values[0]
    euro_price = int(price)
    copper_price = int(round(price % euro_price, 2) * 100)

    svg2png(url=f"{path}/svg/{barcode}.svg", write_to=f"{path}/svg/{barcode}.png",
            dpi=1200)
    my_image = Image.open(f'{path}/images/{file_name}')
    title_font = ImageFont.truetype('Times.ttc', 80)
    euro_font = ImageFont.truetype('Times.ttc', 700)
    copper_font = ImageFont.truetype('Times.ttc', 300)
    euro_sign_font = ImageFont.truetype('Times.ttc', 400)
    fMUCode_font = ImageFont.truetype('Times.ttc', 100)
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((100, 80), title, (0, 0, 0), font=title_font)
    if len(str(euro_price)) == 1:
        image_editable.text((1478, 249),  str(euro_price) + ",", (244, 36, 7), font=euro_font)
    elif len(str(euro_price)) == 2:
        image_editable.text((1128, 249),  str(euro_price) + ",", (244, 36, 7), font=euro_font)
    elif len(str(euro_price)) == 3:
        image_editable.text((1478, 249),  str(euro_price) + ",", (244, 36, 7), font=euro_font)

    image_editable.text((1796, 293), str(copper_price), (244, 36, 7), font=copper_font)
    image_editable.text((2086, 440), "€", (244, 36, 7), font=euro_sign_font)
    image_editable.text((2123, 303), fMUCode, (0, 0, 0), font=fMUCode_font)
    overlay = Image.open(f"{path}/svg/{barcode}.png").convert("RGBA")
    size = (overlay.size[0] // 3, overlay.size[1] // 3)
    overlay = overlay.resize(size, Image.ANTIALIAS)
    my_image.paste(overlay, (44, 383), mask=overlay)

    my_image.save(f"{path}/merged_images/{barcode}.png")
