-- Agrupados duplicados orderdetail
INSERT INTO public.orderdetail
SELECT orderid, prod_id, price, SUM(quantity)
FROM public.orderdetail
GROUP BY orderid, prod_id, price
HAVING COUNT(*) > 1;

DELETE FROM public.orderdetail
WHERE orderid IN (
    SELECT orderid
    FROM public.orderdetail
    GROUP BY orderid, prod_id, price
    HAVING COUNT(*) > 1
);


--Añadir primary y foreign key a actormovies 
ALTER TABLE public.imdb_actormovies
ADD CONSTRAINT imdb_actormovies_pkey PRIMARY KEY (actorid, movieid, "character"),
ADD CONSTRAINT imdb_actormovies_actorid_fkey FOREIGN KEY (actorid) 
    REFERENCES public.imdb_actors (actorid) MATCH SIMPLE 
    ON UPDATE NO ACTION ON DELETE NO ACTION, 
ADD CONSTRAINT imdb_actormovies_movieid_fkey FOREIGN KEY (movieid) 
    REFERENCES public.imdb_movies (movieid) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION;

--Añadir foreign key a inventory
ALTER TABLE public.inventory
ADD CONSTRAINT inventory_prod_id_fkey FOREIGN KEY (prod_id) 
    REFERENCES public.products (prod_id) MATCH SIMPLE 
    ON UPDATE NO ACTION ON DELETE NO ACTION; 

--Añadir primary y foreign key a orderdetail 
ALTER TABLE public.orderdetail
ADD CONSTRAINT orderdetail_pkey PRIMARY KEY (orderid, prod_id), 
ADD CONSTRAINT orderdetail_orderid_fkey FOREIGN KEY (orderid) 
    REFERENCES public.orders (orderid) MATCH SIMPLE 
    ON UPDATE NO ACTION ON DELETE NO ACTION, 
ADD CONSTRAINT orderdetail_prod_id_fkey FOREIGN KEY (prod_id) 
    REFERENCES public.products (prod_id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION;

--Añadir primary y foreign key a orders
ALTER TABLE public.orders
ADD CONSTRAINT orders_customerid_fkey FOREIGN KEY (customerid) 
    REFERENCES public.customers (customerid) MATCH SIMPLE 
    ON UPDATE NO ACTION ON DELETE NO ACTION;

--Resincronizar sequence orders
BEGIN;
    -- protect against concurrent inserts while you update the counter
LOCK TABLE orders IN EXCLUSIVE MODE;
    -- Update the sequence
SELECT setval('orders_orderid_seq'::regclass, 
	      COALESCE((SELECT MAX(orderid)+1 FROM orders), 1), false);
COMMIT;

--Resincronizar sequence idcustomers
BEGIN;
    -- protect against concurrent inserts while you update the counter
LOCK TABLE customers IN EXCLUSIVE MODE;
    -- Update the sequence
SELECT setval('customers_customerid_seq'::regclass, 
	      COALESCE((SELECT MAX(customerid)+1 FROM customers), 1), false);
COMMIT;

select setval('imdb_movies_movieid_seq', (select max(movieid) from imdb_movies));
select setval('imdb_actors_actorid_seq', (select max(actorid) from imdb_actors));
select setval('imdb_directors_directorid_seq', (select max(directorid) from imdb_directors));
select setval('products_prod_id_seq', (select max(prod_id) from products));

--Usuarios duplicados cambiar username a username+id
UPDATE public.customers AS q1
SET username = CONCAT(q1.username,q1.customerid)
FROM 
    (SELECT c.customerid
    FROM customers AS c
    INNER JOIN
        (SELECT username
        FROM customers
        GROUP BY username
        HAVING COUNT(*) > 1) sub
    ON c.username = sub.username) AS dupl
WHERE q1.customerid = dupl.customerid;

--Añadir clave unique a username
ALTER TABLE public.customers 
ADD CONSTRAINT customers_username_unique UNIQUE (username);

--Tabla alertas
CREATE TABLE public.alertas
(
    prod_id integer NOT NULL,
    status character varying(50),
    CONSTRAINT alertas_pkey PRIMARY KEY (prod_id),
    CONSTRAINT alertas_prod_id_fkey FOREIGN KEY (prod_id)
        REFERENCES public.products (prod_id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  FILLFACTOR=85, 
  OIDS=FALSE
);
ALTER TABLE public.alertas
  OWNER TO alumnodb;

UPDATE alertas
SET alertas.prod_id = products.prod_id
FROM products