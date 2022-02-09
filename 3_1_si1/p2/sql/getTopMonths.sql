-- Funcion: getTopMonths()
--------------------------
-- Calcula los meses en los que se supera alguno de los dos umbrales proporcionados (productos vendidos o importe total)
-- 
-- umbral_importe: umbral del importe obtenido a lo largo de todo el mes
-- umbral_productos: umbral de la cantidad de productos vendida ese mes
--
-- returns: una tabla con las películas más vendidas de cada año, mostrando el año, titulo de película y número de ventas
-------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION getTopMonths(    umbral_importe integer,
                                            umbral_productos integer) 
RETURNS TABLE(  año numeric,
                mes numeric,
                importe numeric,
                productos numeric) 
AS $$
SELECT *
FROM (  SELECT  cast(EXTRACT(YEAR FROM orderdate) as numeric) as año,
                cast(EXTRACT(MONTH FROM orderdate) as numeric) as mes,
                cast(SUM(totalamount) as numeric) as importe,
                cast(SUM(products) as numeric) as productos
        FROM    orders NATURAL JOIN
                (   SELECT  orderid, 
                            SUM(quantity) as products -- Calculamos para cada pedido el número de productos vendidos
                    FROM    orderdetail
                    GROUP BY orderid) as products_table
        WHERE status IS NOT NULL
        GROUP BY año, mes) as final_table -- Sumamos para cada pareja (año,mes) el total de productos vendidos y dinero recaudado
WHERE importe > umbral_importe or productos > umbral_productos; -- Solo seleccionamos aquellos que superen los umbrales
$$ LANGUAGE SQL;  