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
SELECT p.movieid, movietitle, year, sum(sales) as sales
FROM products p
JOIN inventory iv ON p.prod_id = iv.prod_id
JOIN imdb_movies im ON p.movieid = im.movieid
GROUP BY p.movieid, movietitle, year
ORDER BY sales DESC
LIMIT 50;