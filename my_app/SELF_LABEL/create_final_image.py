#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved
import itertools
import subprocess
import textwrap
from wand.api import library
import wand.color
import wand.image

from PIL import Image, ImageFont, ImageDraw
import pathlib
import pandas as pd
from datetime import datetime
from xml.dom.minidom import parse
import os
import logging

from tqdm import tqdm

logger=logging.getLogger(__name__)

def svg_to_png(svg_filename, output_filename, dpi=1200):
    """
    Μετατρέπει SVG σε PNG χρησιμοποιώντας τη βιβλιοθήκη Wand.

    Args:
        svg_filename (str): Το μονοπάτι του αρχείου SVG.
        output_filename (str): Το επιθυμητό όνομα του PNG αρχείου εξόδου.
        dpi (int): Η ανάλυση της εικόνας σε Dots Per Inch (προεπιλεγμένο: 1200).
    """
    try:
        # Φορτώνουμε το SVG αρχείο
        with open(svg_filename, "rb") as svg_file:
            # Δημιουργούμε το wand image αντικείμενο
            with wand.image.Image() as image:
                # Ορίζουμε το DPI (ανάλυση)
                image.resolution = (dpi, dpi)

                # Ορίζουμε το background σε transparent
                with wand.color.Color("transparent") as background_color:
                    library.MagickSetBackgroundColor(
                        image.wand, background_color.resource
                    )

                # Φορτώνουμε το SVG μέσα στο Wand Image
                image.read(blob=svg_file.read(), format="svg")

                # Μετατροπή σε PNG (με 32-bit transparency)
                png_image = image.make_blob("png32")

                # Αποθήκευση του PNG σε αρχείο εξόδου
                with open(output_filename, "wb") as out_file:
                    out_file.write(png_image)

        # print(f"H μετατροπή ολοκληρώθηκε: {svg_filename} -> {output_filename} | DPI: {dpi}")

    except Exception as e:
        print(f"Σφάλμα κατά τη μετατροπή SVG σε PNG: {e}")




def run(df, file_name, init_price, tags):
    path = pathlib.Path(__file__).parent.resolve()
    barcode = df['BarCode'].values[0]
    title = df['Περιγραφή'].values[0]
    price = (df[init_price].values[0] if df['ΕΚΠΤΩΣΗ'].values[0] <= 0 else round(df[init_price].values[0] * (100 - df['ΕΚΠΤΩΣΗ'].values[0]) / 100, 2))
    fMUCode = df['MM'].values[0]
    euro_price = int(price)
    # Διαίρεση με το 0 όταν η τιμή είναι 0.50 μας βγάζει σφάλμα έτσι το μετατρέπουμε σε 1
    copper_price = int(round(price % (euro_price if euro_price>0 else 1), 2) * 100)
    if len(str(copper_price)) == 1:
        copper_price = "0"+str(copper_price)

    svg_to_png(f"{path}/svg/{barcode}.svg", f"{path}/svg/{barcode}.png")
    my_image = Image.open(f'{path}/images/{file_name}')
    title_font = ImageFont.truetype('Avenir Next.ttc', 80)
    detailed_info_retail_discount = ImageFont.truetype('Avenir Next.ttc', 58)
    detailed_info_retail = ImageFont.truetype('Futura.ttc', 120)
    euro_font = ImageFont.truetype('Futura.ttc', 700)
    euro_font_2 = ImageFont.truetype('Futura.ttc', 550)
    copper_font = ImageFont.truetype('Futura.ttc', 300)
    euro_sign_font = ImageFont.truetype('Futura.ttc', 400)
    fMUCode_font = ImageFont.truetype('Times.ttc', 98)
    image_editable = ImageDraw.Draw(my_image)

    # TITLE
    # TODO SPLIT THE TEXT MAKE THE BELOW CODE EXECUTABLE BY TESTING
    s_wrap_list = textwrap.wrap(title, 42)
    image_editable.text((100, 80), s_wrap_list[0], (0, 0, 0), font=title_font)
    if len(s_wrap_list) > 1:
        image_editable.text((100, 160), s_wrap_list[1], (0, 0, 0), font=title_font)

    # image_editable.text((100, 80), title, (0, 0, 0), font=title_font)

    # BARCODE
    overlay = Image.open(f"{path}/svg/{barcode}.png").convert("RGBA")
    overlay = overlay.rotate(270, Image.NEAREST, expand=True)
    size = (overlay.size[0] // 4, overlay.size[1] // 4)
    overlay = overlay.resize(size, Image.Resampling.LANCZOS)

    my_image.paste(overlay, (2250, 388), mask=overlay)

    # TAGS
    overlay = Image.open(f"{path}/images/{tags}.png").convert("RGBA")
    size = (overlay.size[0] // 1, overlay.size[1] // 1)
    overlay = overlay.resize(size, Image.Resampling.LANCZOS)


    if (df['ΕΚΠΤΩΣΗ'].values[0] > 0) and (tags == "no_tags"):
        # DETAILED DATA STRUCTURE
        data_a = f"Retail Price: {df[init_price].values[0]}€"
        data_b = f"Discount: {df['ΕΚΠΤΩΣΗ'].values[0]}% "

        # Detailed Info about Price and Discount
        image_editable.text((100, 300), data_a, (255, 255, 255), font=detailed_info_retail)
        image_editable.text((100, 550), data_b, (255, 255, 255), font=detailed_info_retail)

    elif df['ΕΚΠΤΩΣΗ'].values[0] > 0:
        data = f"Retail Price: {df[init_price].values[0]}€ || Discount: {df['ΕΚΠΤΩΣΗ'].values[0]}%"

        # Detailed Info about Price and Discount
        image_editable.text((100, 820), data, (0, 0, 0), font=detailed_info_retail_discount)



    if len(str(euro_price)) == 1:
        image_editable.text((1346 - 40, 80),  str(euro_price) + ".", (244, 36, 7), font=euro_font)
        my_image.paste(overlay, (186 - 40, 211), mask=overlay)
    elif len(str(euro_price)) == 2:
        image_editable.text((1050, 200),  str(euro_price) + ".", (244, 36, 7), font=euro_font_2)
        my_image.paste(overlay, (48 - 40, 211), mask=overlay)
    elif len(str(euro_price)) == 3:
        image_editable.text((555 - 40, 80),  str(euro_price) + ".", (244, 36, 7), font=euro_font)
        my_image.paste(overlay, (-212, 211), mask=overlay)
    # Εμφανίζει ένα δεκαδικό όταν η τιμή είναι π.χ. 1.0 έτσι προσθέτουμε ακόμα ένα 0
    image_editable.text((1755 - 40, 195), (str(copper_price) if len(str(copper_price)) == 2 else str(copper_price) + "0"), (244, 36, 7), font=copper_font)
    image_editable.text((2087 - 40, 340), "€", (244, 36, 7), font=euro_sign_font)
    image_editable.text((2141 - 40, 261), str(fMUCode).lower(), (0, 0, 0), font=fMUCode_font)


    my_image.save(f"{path}/merged_images/{barcode}.png")


def special_price(df, file_name, init_price, tags):
    path = pathlib.Path(__file__).parent.resolve()
    barcode = df['ΚΩΔΙΚΟΣ'].values[0]
    title = df['ΠΕΡΙΓΡΑΦΗ'].values[0]
    price = (df['ΝΕΑ ΤΙΜΗ'].values[0] if df['ΕΚΠΤΩΣΗ'].values[0] <= 0 else round(df[init_price].values[0] * (100 - df['ΕΚΠΤΩΣΗ'].values[0]) / 100, 2))
    fMUCode = df['MM'].values[0]
    euro_price = int(price)
    # Διαίρεση με το 0 όταν η τιμή είναι 0.50 μας βγάζει σφάλμα έτσι το μετατρέπουμε σε 1
    copper_price = int(round(price % (euro_price if euro_price > 0 else 1), 2) * 100)
    if len(str(copper_price)) == 1:
        copper_price = "0"+str(copper_price)

    svg_to_png(f"{path}/svg/{barcode}.svg", f"{path}/svg/{barcode}.png")
    my_image = Image.open(f'{path}/images/{file_name}')
    title_font = ImageFont.truetype('Avenir Next.ttc', 80)
    detailed_info_retail_discount = ImageFont.truetype('Avenir Next.ttc', 38)
    detailed_info_retail = ImageFont.truetype('Futura.ttc', 120)
    euro_font = ImageFont.truetype('Futura.ttc', 700)
    euro_font_2 = ImageFont.truetype('Futura.ttc', 500)
    copper_font = ImageFont.truetype('Futura.ttc', 300)
    euro_sign_font = ImageFont.truetype('Futura.ttc', 400)
    fMUCode_font = ImageFont.truetype('Times.ttc', 98)
    image_editable = ImageDraw.Draw(my_image)

    # TITLE
    # TODO SPLIT THE TEXT MAKE THE BELOW CODE EXECUTABLE BY TESTING
    # s_wrap_list = textwrap.wrap(title, 42)
    # image_editable.text((100, 80), s_wrap_list[0], (0, 0, 0), font=title_font)
    # if len(s_wrap_list) > 1:
    #     image_editable.text((100, 345), s_wrap_list[1], (0, 0, 0), font=title_font)

    image_editable.text((100, 80), title, (0, 0, 0), font=title_font)

    # BARCODE
    overlay = Image.open(f"{path}/svg/{barcode}.png").convert("RGBA")
    overlay = overlay.rotate(270, Image.NEAREST, expand=True)
    size = (overlay.size[0] // 4, overlay.size[1] // 4)
    overlay = overlay.resize(size, Image.Resampling.LANCZOS)

    my_image.paste(overlay, (2250, 388), mask=overlay)

    # TAGS
    overlay = Image.open(f"{path}/images/{tags}.png").convert("RGBA")
    size = (overlay.size[0] // 1, overlay.size[1] // 1)
    overlay = overlay.resize(size, Image.Resampling.LANCZOS)

    starts = str(df['ΕΝΑΡΞΗ'].values[0])[:10]
    starts = datetime.strptime(starts, '%Y-%m-%d').strftime('%d-%m-%Y')
    ends = str(df['ΛΗΞΗ'].values[0])[:10]
    ends = datetime.strptime(ends, '%Y-%m-%d').strftime('%d-%m-%Y')

    # DETAILED DATA STRUCTURE
    data_a = f"Retail Price: {df[init_price].values[0]}€"
    data_b = f"Discount: {df['ΕΚΠΤΩΣΗ'].values[0]}% "
    data_c = f"Starts: {starts} / Ends: {ends}"

    # Detailed Info about Price and Discount
    image_editable.text((100, 300), data_a, (255, 255, 255), font=detailed_info_retail)
    image_editable.text((100, 550), data_b, (255, 255, 255), font=detailed_info_retail)
    image_editable.text((150, 700), data_c, (255, 255, 255), font=detailed_info_retail_discount)

    # FINAL RETAIL PRICE
    if len(str(euro_price)) == 1:
        image_editable.text((1346 - 40, 80), str(euro_price) + ".", (244, 36, 7), font=euro_font)
        my_image.paste(overlay, (186 - 40, 211), mask=overlay)
    elif len(str(euro_price)) == 2:
        image_editable.text((1150, 280), str(euro_price) + ".", (244, 36, 7), font=euro_font_2)
        my_image.paste(overlay, (48 - 40, 211), mask=overlay)
    elif len(str(euro_price)) == 3:
        image_editable.text((555 - 40, 80), str(euro_price) + ".", (244, 36, 7), font=euro_font)
        my_image.paste(overlay, (-212, 211), mask=overlay)

    # Εμφανίζει ένα δεκαδικό όταν η τιμή είναι π.χ. 1.0 έτσι προσθέτουμε ακόμα ένα 0
    image_editable.text((1755 - 40, 195),
                        (str(copper_price) if len(str(copper_price)) == 2 else str(copper_price) + "0"), (244, 36, 7),
                        font=copper_font)
    image_editable.text((2087 - 40, 340), "€", (244, 36, 7), font=euro_sign_font)
    image_editable.text((2141 - 40, 261), str(fMUCode).lower(), (0, 0, 0), font=fMUCode_font)

    my_image.save(f"{path}/merged_images/{barcode}.png")


def split_labels_to_fit_a4(big=False):
    path = pathlib.Path(__file__).parent.resolve()

    # Get the File List of names
    list_of_names = os.listdir(f"{path}/merged_images")
    logger.info(list_of_names)

    if big:
        labels_per_page = 8
    else:
        labels_per_page = 14

    # every A4 page can have maximum of 14 image labels
    total_pages = (len(list_of_names) // labels_per_page) + (1 if len(list_of_names) % labels_per_page > 0 else 0)

    logger.info(f"Total Labels in PATH: {len(list_of_names)}")
    logger.info(f"Total A4 Pages to Build: {total_pages}")

    page_number = 1
    while list_of_names:
        labels = list_of_names[:labels_per_page]
        logger.info(f"Labels to PUt inside A4 PAGE {page_number}: {labels}")
        del list_of_names[:labels_per_page]
        a4_page_fit_images(labels, f"A4_PAGE{page_number}.png", big=big)
        page_number += 1



def a4_page_fit_images(labels, ouptut_name, big=False):
    path = pathlib.Path(__file__).parent.resolve()
    if big:
        image_name = "A4_Labels_Saloon_big.png"
        # Συντεταγμένες για κάθε εικόνα
        x = [163, 1754]
        y = [56, 653, 1250, 1847]
        c = list(itertools.product(x, y))
        size = (1591, 597)
    else:
        image_name = "A4_Labels_Saloon.png"
        # Συντεταγμένες για κάθε εικόνα
        x = [49, 1240]
        y = [158, 604, 1050, 1496, 1942, 2388, 2834]
        c = list(itertools.product(x, y))
        size = (1191, 446)

    my_image = Image.open(f'{path}/images/{image_name}')
    for name, place in tqdm(zip(labels, c), "A4 Page Maker"):
        logger.info(f"Fitting IMAGE: {name} to A4 in (X, Y): {place}")
        overlay = Image.open(f"{path}/merged_images/{name}")
        overlay = overlay.resize(size, Image.Resampling.LANCZOS)

        my_image.paste(overlay, place, mask=overlay)
    file_out = f"{path}/to_print_labels/{ouptut_name}"
    my_image.save(file_out)




def export_to_printer(printer_name='KOMMAS'):
    path = pathlib.Path(__file__).parent.resolve()
    if printer_name == "0":
        logger.info("No Print Asked, Opening Folder Instead")
        subprocess.call(['open', f"{path}/to_print_labels"])
    else:
        list_of_names = os.listdir(f"{path}/to_print_labels")
        for file_name in list_of_names:
            file = f"{path}/to_print_labels/{file_name}"
            # print(printer_name)
            os.system(f"lpr -P {printer_name} {file}")




