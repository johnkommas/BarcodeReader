import pandas as pd
import logging
import os
import pathlib
import shutil
import barcode
from barcode.writer import SVGWriter
from app import sql
from private import sql_connect
from tqdm import tqdm

parent_path = pathlib.Path(__file__).parent.resolve()


def app(db_codes, color, folder='svg'):
    options = {
        # 'module_width': 0.2,
        # 'module_height': 120.0,
        # 'quiet_zone': 3.0,
        # 'font_path': 'Times.ttc',
        # 'font_size': 7,
        # 'text_distance': 2.0,
        'background': color,
        'foreground': 'black',
        # 'center_text': True
    }
    for code in tqdm(db_codes, desc="Barcode Generator: Creating SVG Files"):
        try:
            if len(code) == 13:
                x = barcode.EAN13_GUARD(str(code), writer=SVGWriter())
            elif len(code) == 8:
                x = barcode.EAN8_GUARD(str(code), writer=SVGWriter())
            elif len(code) == 14:
                x = barcode.EAN14(str(code), writer=SVGWriter())
            else:
                raise Exception
            with open(f"{parent_path}/{folder}/{code}.svg", "wb") as f:
                x.write(f, options=options)
        except Exception as e:
            logging.warning(f'BARCODE ERROR: {code} || length is: {len(code)}', e)


def delete_all_files_inside_folder(folder=f'{parent_path}/svg'):
    for filename in tqdm(os.listdir(folder), desc=f'Barcode Generator: Deleting Files on {folder}'):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def get_info_from_database(mobile_document_header_code, order_type):
    df = pd.read_sql_query(sql.data_query(mobile_document_header_code, order_type), con=sql_connect.connect())
    return df


def run(mobile_document_header_code, order_type, color):
    # ----------------MAKE DF Reports Viewable----------------------------
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    delete_all_files_inside_folder()
    delete_all_files_inside_folder(folder=f'{parent_path}/merged_images')
    df = get_info_from_database(mobile_document_header_code, order_type)
    barcodes = df['BarCode'].tolist()
    app(barcodes, color)
    return df
