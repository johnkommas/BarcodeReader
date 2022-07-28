#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved

def data_query(input_param, type_of_forma):
    return f"""
SELECT  DISTINCT IMP_MobileDocumentLines.BarCode        AS 'BarCode',
        IMP_MobileDocumentLines.ItemDescription         AS 'Περιγραφή',
        sum(quant)                                      AS 'Ποσότητα',
        ESFIZItemCategory.Description                   AS 'Κατηγορία',
        ESMMItemMU.fMUCode                              AS 'MM',
        ESFIItem.RetailPrice                            AS 'RetailPrice',
        ESFIItem.Price1                                 AS 'LATO 01',
        ESFIItem.Price2                                 AS 'LATO 02'
        FROM IMP_MobileDocumentLines
            LEFT JOIN IMP_MobileDocumentHeaders
                ON IMP_MobileDocumentHeaders.GID = IMP_MobileDocumentLines.fDocGID
--             LEFT JOIN ESFITradeAccount
--                 ON ESFITradeAccount.gid = IMP_MobileDocumentHeaders.Supplier
            LEFT JOIN ESFIItem
                ON ESFIItem.GID = IMP_MobileDocumentLines.fItemGID
            LEFT JOIN ESFIZItemCategory
                ON ESFIItem.fItemCategoryCode = ESFIZItemCategory.Code
            LEFT JOIN ESMMItemMU
                ON ESFIItem.fMainMUGID = ESMMItemMU.GID
        WHERE DATEPART(yyyy,RealImportTime) = DATEPART(yyyy,getdate())
            AND IMP_MobileDocumentHeaders.Code = {input_param}
            AND OrderType = '{type_of_forma}'
        GROUP BY IMP_MobileDocumentLines.ItemDescription
                 ,IMP_MobileDocumentLines.BarCode
                 ,ESFIZItemCategory.Description
                 ,ESMMItemMU.fMUCode 
                 ,ESFIItem.RetailPrice 
                 ,ESFIItem.Price1
                 ,ESFIItem.Price2
        ORDER BY 4, 2
"""


def get_products_in_the_period(from_date):
    return f"""
SELECT ESFIPricelist.Code                         AS 'ΤΙΜΟΚΑΤΑΛΟΓΟΣ',
       ESFIPricelistItem.fItemPricingCategoryCode AS 'ΚΑΤΗΓΟΡΙΑ',
       ESFIPricelistItem.ValidFromDate            AS 'ΕΝΑΡΞΗ',
       ESFIPricelistItem.ValidToDate              AS 'ΛΗΞΗ',
       ESFIItem.Description                       AS 'ΠΕΡΙΓΡΑΦΗ',
       ESFIItem.BarCode                           AS 'ΚΩΔΙΚΟΣ',
       ESFIItem.RetailPrice                       AS 'ΤΙΜΗ ΛΙΑΝΙΚΗΣ',
       ESFIItem.Price1                            AS 'LATO 01',
       ESFIItem.Price2                            AS 'LATO 02',
       ESFIPricelistItem.Price                    AS 'ΝΕΑ ΤΙΜΗ',
       ESFIPricelistItem.PercentageOnBasePrice    AS 'ΠΟΣΟΣΤΟ',
       ESFIItem.fItemSubcategoryCode              AS 'BRAND'
from ESFIPricelistItem
         left join ESFIItem
                   on ESFIPricelistItem.fItemGID = ESFIItem.GID
         inner JOIN ESFIPricelist
                    on ESFIPricelistItem.fPricelistGID = ESFIPricelist.GID
where ValidFromDate = '{from_date}' 

order by 3,4,5
"""

# example
# import pandas as pd
# from private import sql_connect
#
# df= pd.read_sql_query(get_products_in_the_period("2022-07-29"), sql_connect.connect())
# print(df['ΚΩΔΙΚΟΣ'].values)