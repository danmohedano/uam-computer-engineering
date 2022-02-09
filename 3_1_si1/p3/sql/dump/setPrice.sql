-- xo = xf/(1.02)^t, t = cantidad de años que han pasado desde el pedido, xf = el precio actual (products), xo = precio en la fecha de pedido (orderdetail)   
    
UPDATE orderdetail
SET price = round(CAST((CALC.priceNow/POWER(1.02, EXTRACT(YEAR FROM now()) - CALC.dateoforder)) as numeric ), 2) * quantity
    -- Realizamos una query para ver para cada producto de cada pedido
    -- cuanto tiempo ha pasado desde que se realizó el pedido
    FROM    (SELECT A.orderid,
                    A.prod_id,
                    EXTRACT (YEAR FROM A.orderdate) as dateoforder,
                    B.price as priceNow
            FROM    (orderdetail NATURAL 
                    INNER JOIN orders) as A
                    INNER JOIN (SELECT * FROM products) as B
                    on A.prod_id = B.prod_id
            ) as CALC
    WHERE   orderdetail.orderid = CALC.orderid and 
            orderdetail.prod_id = CALC.prod_id
