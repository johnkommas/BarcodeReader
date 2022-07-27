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

