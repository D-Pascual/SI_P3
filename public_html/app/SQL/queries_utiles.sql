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