--Seleccionar donde el campo de una columna esta repetido
SELECT c.customerid, c.username
FROM customers c
INNER JOIN
(SELECT username
 FROM customers
 GROUP BY username
 HAVING COUNT(*) > 1) sub
ON c.username = sub.username

select * from --Encontrar repes con username tarp
	(SELECT c.customerid, c.username
	FROM customers c
	INNER JOIN
	(SELECT username
	FROM customers
	GROUP BY username
	HAVING COUNT(*) > 1) sub
	ON c.username = sub.username) as c3
where c3.username='tarp'

SELECT * FROM customers --Encontrar users que contengan tarp en el username
WHERE username LIKE '%tarp%'


--Top peliculas ultimos 3 años
SELECT p.prod_id, p.movieid, movietitle, description, year, sum(quantity) as sales
FROM products p
JOIN imdb_movies im ON p.movieid = im.movieid
JOIN orderdetail od ON p.prod_id = od.prod_id
JOIN orders o ON od.orderid = o.orderid
WHERE (extract(year FROM o.orderdate) > (extract(year FROM now()) - 3)) AND o.status is not NULL
GROUP BY p.prod_id, description, movietitle, year
ORDER BY sales DESC
LIMIT 50;