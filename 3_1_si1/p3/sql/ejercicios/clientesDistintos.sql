--Regular Query
EXPLAIN 
SELECT 	COUNT(distinct(customerid))
FROM 	orders
WHERE 	totalamount > 100 AND 
        CAST(EXTRACT(year from orderdate) AS varchar) || 
        RIGHT('0' || CAST(EXTRACT(month from orderdate) AS varchar), 2) = '201504';

--Crear Index en la función sobre la fecha
CREATE INDEX idx_date_orders ON orders((CAST(EXTRACT(year from orderdate) AS varchar) || RIGHT('0' || CAST(EXTRACT(month from orderdate) AS varchar), 2)));
EXPLAIN 
SELECT 	COUNT(distinct(customerid))
FROM 	orders
WHERE 	totalamount > 100 AND 
        CAST(EXTRACT(year from orderdate) AS varchar) || 
        RIGHT('0' || CAST(EXTRACT(month from orderdate) AS varchar), 2) = '201504';

--Crear Index en totalamount
DROP INDEX idx_date_orders;
CREATE INDEX idx_totalamount_orders ON orders(totalamount);
EXPLAIN 
SELECT 	COUNT(distinct(customerid))
FROM 	orders
WHERE 	totalamount > 100 AND 
        CAST(EXTRACT(year from orderdate) AS varchar) || 
        RIGHT('0' || CAST(EXTRACT(month from orderdate) AS varchar), 2) = '201504';

--Crear index en la fecha y amount
DROP INDEX idx_totalamount_orders;
CREATE INDEX idx_both_orders ON orders((CAST(EXTRACT(year from orderdate) AS varchar) || RIGHT('0' || CAST(EXTRACT(month from orderdate) AS varchar), 2)), totalamount);
EXPLAIN 
SELECT 	COUNT(distinct(customerid))
FROM 	orders
WHERE 	totalamount > 100 AND 
        CAST(EXTRACT(year from orderdate) AS varchar) || 
        RIGHT('0' || CAST(EXTRACT(month from orderdate) AS varchar), 2) = '201504';

--Crear index en el amount y la fecha
DROP INDEX idx_both_orders;
CREATE INDEX idx_both_orders ON orders(totalamount, (CAST(EXTRACT(year from orderdate) AS varchar) || RIGHT('0' || CAST(EXTRACT(month from orderdate) AS varchar), 2)));
EXPLAIN 
SELECT 	COUNT(distinct(customerid))
FROM 	orders
WHERE 	totalamount > 100 AND 
        CAST(EXTRACT(year from orderdate) AS varchar) || 
        RIGHT('0' || CAST(EXTRACT(month from orderdate) AS varchar), 2) = '201504';
DROP INDEX idx_both_orders;