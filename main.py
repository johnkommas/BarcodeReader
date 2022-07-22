import pandas as pd
import logging
import os
import pathlib
import shutil
import barcode
from barcode.writer import SVGWriter
import sql

path = pathlib.Path(__file__).parent.resolve()


def app(db_codes, folder='svg'):
    options = {
        # 'module_width': 0.2,
        # 'module_height': 120.0,
        # 'quiet_zone': 3.0,
        # 'font_path': 'DejaVuSansMono',
        # 'font_size': 7,
        # 'text_distance': 2.0,
        # 'background': 'white',
        # 'foreground': 'black',
        # 'center_text': True
    }
    for code in db_codes:
        try:
            if len(code) == 13:
                x = barcode.EAN13_GUARD(str(code), writer=SVGWriter())
            elif len(code) == 8:
                x = barcode.EAN8_GUARD(str(code), writer=SVGWriter())
            elif len(code) == 14:
                x = barcode.EAN14(str(code), writer=SVGWriter())
            else:
                raise Exception
            with open(f"{path}/{folder}/{code}.svg", "wb") as f:
                x.write(f, options=options)
        except Exception as e:
            logging.warning(f'BARCODE ERROR: {code} || length is: {len(code)}', e)


def delete_all_files_inside_folder(folder=f'{path}/svg'):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def get_info_from_database(mobile_document_header_code, order_type):
    df = pd.read_sql_query(sql.data_query(mobile_document_header_code, order_type), con='connection string')
    return df

# TODO add slack modal (popup asks for number and type)
# TODO add slack button
# TODO create and image and import svg file in it
# TODO create the DB connection string


if __name__ == '__main__':
    mobile_document_header_code = '1200'
    order_type = 'ΠΠΡ'
    # codes = get_info_from_database(mobile_document_header_code, order_type)
    codes = ['5214000237334', '5213002921425', '52059894']
    app(codes)
    # delete_all_files_inside_folder()

