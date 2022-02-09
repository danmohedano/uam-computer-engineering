ALTER TABLE public.customers
ADD COLUMN promo integer;

CREATE OR REPLACE FUNCTION updPromo()
RETURNS TRIGGER
AS $$
BEGIN 
    PERFORM pg_sleep(10);
    UPDATE  orderdetail
    SET     price = products.price*(1-(NEW.promo/100))
    FROM    products
    WHERE   orderdetail.prod_id = products.prod_id AND
            orderid IN (SELECT  orderid 
                        FROM    orders 
                        WHERE   customerid = NEW.customerid AND
                                status is NULL);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER updPromo
AFTER UPDATE ON customers
FOR EACH ROW EXECUTE
PROCEDURE updPromo();
