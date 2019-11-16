--orderdetail rellenar columna price
--precio actual en price de products
--fecha del pedido en orderdate de orders
--
--estamos en 2019
  --  -precio ahora: 20eur
  --  -año pedido: 2015
  --  -Ha ido aumentando un 2% anualmente

UPDATE public.orderdetail
SET price = 0 --products.price / power(1.02, 2019- extract(year FROM orders.orderdate))
FROM public.orderdetail as OD 
JOIN public.products ON OD.prod_id = products.prod_id
JOIN public.orders ON OD.orderid = orders.orderid 
