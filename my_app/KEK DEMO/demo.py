#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved

from DEMOS import sql_query
import pandas as pd
import warnings

warnings.filterwarnings('ignore')


def run(file_in, file_out):
    df_customer = pd.read_excel(file_in)
    df_customer['BARCODE'] = df_customer['BARCODE'].astype("string")
    codes = tuple(df_customer.BARCODE.unique())
    df = sql_query.get_product_cost(codes)
    df.to_csv(file_out, index=False)


run("delta.xlsx", "entersoft.csv")
