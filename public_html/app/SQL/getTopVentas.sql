DROP FUNCTION IF EXISTS getTopVentas(integer);
CREATE OR REPLACE FUNCTION getTopVentas(anioRef integer)   RETURNS TABLE (
     anio   double precision   -- also visible as OUT parameter inside function
               , Pelicula   character varying(255)
               , Ventas   bigint) AS
$func$
BEGIN
  LOOP
  EXIT WHEN anioRef = 2020;
  RETURN QUERY
    SELECT * FROM (
    SELECT date_part('year', orders.orderdate), movietitle, count(imdb_movies.movieid) as cou
    FROM orders
    INNER JOIN orderdetail
    ON orders.orderid = orderdetail.orderid
    INNER JOIN products
    ON orderdetail.prod_id = products.prod_id
    INNER JOIN imdb_movies
    ON products.movieid = imdb_movies.movieid
    WHERE date_part('year', orders.orderdate) = anioRef
    GROUP BY movietitle, date_part('year', orders.orderdate)
    ORDER BY cou DESC
    LIMIT 1) as a
    ORDER BY a.cou DESC;
  anioRef := anioRef + 1;
  END LOOP;
END;
$func$  LANGUAGE plpgsql;

SELECT * FROM getTopVentas(2015);