--Procedimiento del trigger
create or replace function update_orders() returns trigger as $$
	begin
	if TG_OP = 'INSERT' then
	update orders set netamount = netamount + new.price * new.quantity,
		totalamount = (select (netamount + (new.price * new.quantity))* (select 1+(tax*0.01) from orders where orderid = new.orderid) from orders where orderid = new.orderid )
	where orderid = new.orderid;
	return new;
	elsif tg_op = 'UPDATE' then
	update orders set netamount = netamount + new.price * (new.quantity - old.quantity),
		totalamount = (select (netamount + (new.price * (new.quantity-old.quantity)))* (select 1+(tax*0.01) from orders where orderid = new.orderid) from orders where orderid = new.orderid )
	where orderid = new.orderid;
	return new;
	elsif TG_OP ='DELETE' then
	update orders set netamount = netamount - old.price * old.quantity,
		totalamount = (select (netamount - (old.price * old.quantity))* (select 1+(tax*0.01) from orders where orderid = old.orderid) from orders where orderid = old.orderid )
	where orderid = old.orderid;
	return old;
	end if;
	end;  $$
	language 'plpgsql';
	
--Crear trigger
create trigger updOrders after insert or update or delete on orderdetail
	for each row execute procedure update_orders();