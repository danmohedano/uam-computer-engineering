CREATE OR REPLACE FUNCTION updInventory()
RETURNS TRIGGER
AS $$
BEGIN
    IF OLD.status IS NULL AND NEW.status = 'Paid' THEN
        UPDATE inventory
        -- Actualizar el stock y las sales con la cantidad de cada producto del pedido
        SET stock = stock - sold_products.quantity, 
            sales = sales + sold_products.quantity
        FROM (  SELECT  prod_id,
                        quantity
                FROM orderdetail
                WHERE orderid = NEW.orderid) as sold_products
        WHERE inventory.prod_id = sold_products.prod_id;

        -- Comprobar si el stock ha caido a 0 y añadir una alerta
        INSERT INTO public.alertas (prod_id)
        SELECT  orderdetail.prod_id
        FROM    (inventory
                 NATURAL JOIN products) as A
                 JOIN orderdetail
                 ON orderdetail.prod_id = A.prod_id
        WHERE   orderid = NEW.orderid and stock = 0;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER updInventory
AFTER UPDATE ON orders
FOR EACH ROW EXECUTE
PROCEDURE updInventory();