UPDATE public.orderdetail as OD
SET price = ROUND(CAST(P.price / power(1.02, extract(year FROM now()) - extract(year FROM O.orderdate)) AS NUMERIC), 2) --products.price / power(1.02, 2019- extract(year FROM orders.orderdate))
FROM public.products as P, public.orders as O 
WHERE OD.prod_id = P.prod_id AND OD.orderid = O.orderid;
