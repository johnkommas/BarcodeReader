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
        ESFIItem.Price2                                 AS 'LATO 02',
        ESFIItem.Discount                               AS 'ΕΚΠΤΩΣΗ'
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
                 ,ESFIItem.Discount
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
       ESFIItem.RetailPrice                       AS 'RetailPrice',
       ESFIItem.Price1                            AS 'LATO 01',
       ESFIItem.Price2                            AS 'LATO 02',
       ESFIPricelistItem.Price                    AS 'ΝΕΑ ΤΙΜΗ',
       ESFIPricelistItem.PercentageOnBasePrice    AS 'ΕΚΠΤΩΣΗ',
       ESFIItem.fItemSubcategoryCode              AS 'BRAND',
              ESMMItemMU.fMUCode                  AS 'MM'
from ESFIPricelistItem
         left join ESFIItem
                   on ESFIPricelistItem.fItemGID = ESFIItem.GID
         inner JOIN ESFIPricelist
                    on ESFIPricelistItem.fPricelistGID = ESFIPricelist.GID
         LEFT JOIN ESMMItemMU
                    ON ESFIItem.fMainMUGID = ESMMItemMU.GID
where ValidFromDate = '{from_date}' 

order by 3,4,5
"""

