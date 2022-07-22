
def data_query(input_param, type_of_forma):
    return f"""
SELECT  distinct IMP_MobileDocumentLines.BarCode,
        IMP_MobileDocumentLines.ItemDescription as 'Περιγραφή',
        sum(quant) as 'Ποσότητα',
        ESFIZItemCategory.Description AS 'Κατηγορία'
        FROM IMP_MobileDocumentLines
        left join IMP_MobileDocumentHeaders
        on IMP_MobileDocumentHeaders.GID = IMP_MobileDocumentLines.fDocGID
        left join ESFITradeAccount
        on ESFITradeAccount.gid = IMP_MobileDocumentHeaders.Supplier
        left JOIN ESFIItem
            ON ESFIItem.GID = IMP_MobileDocumentLines.fItemGID
        LEFT JOIN ESFIZItemCategory
        ON ESFIItem.fItemCategoryCode = ESFIZItemCategory.Code
        where DATEPART(yyyy,RealImportTime) = DATEPART(yyyy,getdate())
        --and DATEPART(mm,RealImportTime) = DATEPART(mm,getdate())
        and IMP_MobileDocumentHeaders.Code = {input_param}
        and OrderType = '{type_of_forma}'
        group by IMP_MobileDocumentLines.ItemDescription, IMP_MobileDocumentLines.BarCode
                 ,ESFIZItemCategory.Description
        order by 4, 2
"""