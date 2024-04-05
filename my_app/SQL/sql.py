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

def lato_prices(barcodes):
    return f"""
SELECT  DISTINCT ESFIItem.BarCode                       AS 'ΚΩΔΙΚΟΣ',
        ESFIItem.Description                            AS 'ΠΕΡΙΓΡΑΦΗ',
        ESMMItemMU.fMUCode                              AS 'MM',
        ESFIItem.Price1                                 AS 'LATO 01',
        ESFIItem.Discount                               AS 'ΕΚΠΤΩΣΗ'
        FROM ESFIItem
            LEFT JOIN ESFIZItemCategory
                ON ESFIItem.fItemCategoryCode = ESFIZItemCategory.Code
            LEFT JOIN ESMMItemMU
                ON ESFIItem.fMainMUGID = ESMMItemMU.GID
        WHERE ESFIItem.BarCode in {barcodes}
"""


def get_products_in_the_period(from_date):
    print(from_date)
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
where '{from_date}' = ValidFromDate 

order by 3,4,5
"""


def ml_test_sales():
    return """
    SELECT

       DATEPART(D,ESFIItemEntry_ESFIItemPeriodics.RegistrationDate) AS 'DATE',
       DATEPART(YY, ESFIItemEntry_ESFIItemPeriodics.RegistrationDate) AS 'YEAR',
       isnull(Sum(ESFIItemEntry_ESFIItemPeriodics.ESFIItemPeriodics_TurnOver),0) AS 'TurnOver'



FROM ESFIItemEntry_ESFIItemPeriodics

WHERE
        (ESFIItemEntry_ESFIItemPeriodics.ESFIItemPeriodics_SalesQty <> 0)
        AND ESFIItemEntry_ESFIItemPeriodics.fSiteGID= '86947579-6885-4E86-914E-46378DB3794F'
group by ESFIItemEntry_ESFIItemPeriodics.RegistrationDate
    """