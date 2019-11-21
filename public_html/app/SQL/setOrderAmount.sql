--Añadir Proc. almacenado setOrderAmount
CREATE OR REPLACE FUNCTION setOrderAmount() RETURNS VOID
AS $$    
BEGIN
    UPDATE public.orders as ORD
    SET netamount = SUB.na_sum, totalamount = ROUND(((100+tax)/100) * SUB.na_sum, 2)
    FROM (
        SELECT SUM(price) as na_sum, orderid
        FROM public.orderdetail
        GROUP BY orderid
    ) as SUB
    WHERE ORD.orderid = SUB.orderid;
END; $$
LANGUAGE plpgsql;
 
SELECT * FROM setOrderAmount(); -- Ejecuta funcion