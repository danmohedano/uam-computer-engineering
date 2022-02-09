CREATE OR REPLACE FUNCTION updOrders()
RETURNS TRIGGER
AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        UPDATE orders
        SET netamount = netamount + NEW.price, 
            totalamount = totalamount + round(NEW.price*(1+(orders.tax/100)), 2)
        WHERE orders.orderid = NEW.orderid;
        RETURN NEW;
    ELSIF (TG_OP = 'UPDATE') THEN
        UPDATE orders
        SET netamount = netamount + NEW.price - OLD.price, 
            totalamount = totalamount + round(NEW.price*(1+(orders.tax/100)), 2) - round(OLD.price*(1+(orders.tax/100)), 2)
        WHERE orders.orderid = NEW.orderid;
        RETURN NEW;
    ELSIF (TG_OP = 'DELETE') THEN
        UPDATE orders
        SET netamount = netamount - OLD.price, 
            totalamount = totalamount - round(OLD.price*(1+(orders.tax/100)), 2)
        WHERE orders.orderid = OLD.orderid;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER updOrders
AFTER INSERT OR UPDATE OR DELETE ON orderdetail
FOR EACH ROW EXECUTE
PROCEDURE updOrders();