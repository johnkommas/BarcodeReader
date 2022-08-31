#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved
from my_app.SQL import sql_connect
import pandas as pd


def get_product_cost(codes):
    database_query = f"""
    SELECT
           ESFIItem.BarCode                                                                                     AS 'BARCODE',
           ESFIItem.RetailPrice                                                                                 AS 'RETAIL',
           ESFIITEM.fVATCategoryCode                                                                            AS 'VAT'


    FROM ESFIItem
             
    WHERE  ESFIItem.BarCode in {codes}

    """
    df = pd.read_sql_query(database_query, sql_connect.connect())
    return df

