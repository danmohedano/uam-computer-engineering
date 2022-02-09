-- Funcion: getTopVentas()
--------------------------
-- Calcula las películas más vendidas cada año en el rango de años proporcionado
-- 
-- ini_year: año inicial del rango
-- end_year: año final del rango
--
-- returns: una tabla con las películas más vendidas de cada año, mostrando el año, titulo de película y número de ventas
-------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION getTopVentas(    ini_year integer,
                                            end_year integer) 
RETURNS TABLE(  year numeric,
                movietitle character varying(255),
                sales numeric) 
AS $$
-- Se escogen con distinct en el año de venta para poder escoger la primera (tras ordenar) 
-- y por lo tanto la película más vendida de ese año
SELECT DISTINCT ON(año)
*
FROM    (SELECT CAST(extract(year FROM orderdate) as numeric) AS año,
                movietitle,
                CAST(SUM(quantity) as numeric) AS ventas
        FROM    orders,
                orderdetail,
                products,
                imdb_movies
        WHERE 	EXTRACT(year FROM orderdate) >= ini_year AND
                EXTRACT(year FROM orderdate) <= end_year AND
                status IS NOT NULL AND
                orders.orderid = orderdetail.orderid AND
                orderdetail.prod_id = products.prod_id AND 
                products.movieid = imdb_movies.movieid 
        GROUP BY año, movietitle) AS calc
ORDER BY año, ventas DESC;
$$ LANGUAGE SQL;        