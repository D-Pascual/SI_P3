DROP FUNCTION IF EXISTS getTopMonths(integer, integer);
CREATE OR REPLACE FUNCTION getTopMonths(imp integer, prods integer)   RETURNS TABLE (
     year   double precision   -- also visible as OUT parameter inside function
    ,month   double precision   -- also visible as OUT parameter inside function
               , Importe   numeric
               , Productos   bigint) AS
$func$
        BEGIN
    RETURN QUERY
    SELECT date_part('year', orderdate), date_part('month', orderdate), SUM(TAX), count(prod_id) as s -- SUSTITUIR SUM(TAX) por SUM(TOTALAMOUNT)
    FROM orders
    INNER JOIN orderdetail
    ON orders.orderid=orderdetail.orderid
    GROUP BY date_part('year', orderdate), date_part('month', orderdate)
    HAVING SUM(TAX) > imp AND count(prod_id) > prods
    ORDER BY date_part('year', orderdate), date_part('month', orderdate);
        END;
$func$  LANGUAGE plpgsql;

SELECT * FROM getTopMonths(1, 1);