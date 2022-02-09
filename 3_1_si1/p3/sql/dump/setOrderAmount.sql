-- Funcion: setOrderAmount()
--------------------------
-- Calcula los valores de netamount y totalamount para todos los pedidos
-------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION setOrderAmount() returns void AS $$
    UPDATE orders
    SET netamount = calc.net, 
        totalamount = round(calc.net * (1 + (orders.tax/100)), 2)
        -- Para cada pedido simplemente sumamos los precios de todos los productos de dicho pedido
        FROM    (SELECT orderid,
                        SUM(price) as net 
                FROM    orderdetail
                GROUP BY orderid
                ) as calc
        WHERE orders.orderid = calc.orderid;     
$$ LANGUAGE SQL;