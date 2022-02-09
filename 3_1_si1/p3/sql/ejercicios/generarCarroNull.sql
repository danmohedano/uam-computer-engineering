UPDATE  orders
SET     status = NULL
WHERE   customerid = (  SELECT  customerid 
                        FROM    orders 
                        ORDER BY customerid ASC 
                        LIMIT 1)
RETURNING customerid