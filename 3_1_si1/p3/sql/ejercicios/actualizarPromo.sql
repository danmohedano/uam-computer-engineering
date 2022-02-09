UPDATE  customers
SET     promo = 10
WHERE   customerid = (  SELECT  customerid 
                        FROM    orders 
                        ORDER BY customerid ASC 
                        LIMIT 1)