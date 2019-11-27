--Procedimiento del trigger
create or replace function update_products_orders() returns trigger as $$
	begin
	if new.status = 'Paid' then
	update inventory p set sales = sales + (select quantity from orderdetail o where orderid = new.orderid
		and o.prod_id = p.prod_id) where prod_id in (select prod_id from orderdetail where orderid = new.orderid);
	update inventory p set stock = stock - (select quantity from orderdetail o where orderid = new.orderid
		and o.prod_id = p.prod_id) where prod_id in (select prod_id from orderdetail where orderid = new.orderid);
	end if;
    
    --alerta

	return new;
	end;
	$$
	language 'plpgsql';

--Crear trigger
create trigger updInventory after update of status on orders
	for each row execute procedure update_products_orders();