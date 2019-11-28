# -*- coding: utf-8 -*-

import os
import sys, traceback
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select
from datetime import date

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)

# Tabla orders
db_table_orders = Table('orders', db_meta, autoload=True, autoload_with=db_engine)
# Tabla orderdetail 
db_table_orderdetail = Table('orderdetail', db_meta, autoload=True, autoload_with=db_engine)
# Tabla customers
db_table_customers = Table('customers', db_meta, autoload=True, autoload_with=db_engine)


def db_check_user(username):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        check_login = db_table_customers.select().where(text("username = :username"))
        db_result = db_conn.execute(check_login, {'username': username})

        db_conn.close()

        rows = db_result.fetchall() 
        if len(rows): # Si la query no esta vacia
            return True
        else:
            return False

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False


def db_check_login(username, password):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        check_login = select([db_table_customers.c.customerid]) \
                                        .where(text("username = :username AND password = :password"))
        db_result = db_conn.execute(check_login, {'username': username, 'password': password})

        db_conn.close()

        row = db_result.fetchone()
        if row: # Si la query no esta vacia
            return row[0] # Devuelve usuario
        else:
            return None

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return None


def db_registro(usuario):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        stmt = db_table_customers.insert()
        stmt = stmt.values({"username": usuario['username'], 
                            "firstname": usuario['nombre'],
                            "lastname": usuario['apellidos'],
                            "address1": usuario['direccion'],
                            "region": usuario['region'],
                            "country": usuario['pais'],
                            "city": usuario['ciudad'],
                            "password": usuario['password'],
                            "email": usuario['email'],
                            "gender": usuario['genero'],
                            "age": usuario['edad'],
                            "creditcardtype": usuario['card_type'],
                            "creditcard": usuario['tarjeta'],
                            "creditcardexpiration": usuario['caducidad_tarjeta'],
                            "saldo": usuario['saldo']})

        db_conn.execute(stmt)

        db_conn.close()

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def db_user_id_by_username(username):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        query = select([db_table_customers.c.customerid]) \
                                        .where(text("username = :username"))
        db_result = db_conn.execute(query, {'username': username})

        db_conn.close()

        row = db_result.fetchone()
        if row: # Si la query no esta vacia
            return row[0] # Devuelve usuario
        else:
            return None

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return None


def db_carrito(userid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        movies = []
        query_carrito = "SELECT * FROM orders WHERE status is null and customerid={}".format(userid)
        db_result = db_conn.execute(query_carrito)
        row = db_result.fetchone()
        if not row:
            return None
        query_carrito = "SELECT movietitle, quantity, orderdetail.price, products.prod_id FROM orderdetail INNER JOIN products ON orderdetail.prod_id = products.prod_id INNER JOIN imdb_movies ON products.movieid = imdb_movies.movieid WHERE orderid = {}".format(row[0]) #row[0] = orderid
        db_result = db_conn.execute(query_carrito)
        rowDetail = db_result.fetchone()
        while rowDetail:
            movie = {
                "titulo": rowDetail[0],
                "cantidad": rowDetail[1],
                "precio": rowDetail[2],
                "id": rowDetail[3]
            }
            movies.append(movie)
            rowDetail = db_result.fetchone()
        db_conn.close()

        return movies
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def db_orderdetail_by_orderid(id):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        query_carrito = "SELECT * FROM orderdetail WHERE orderid={}".format(id)
        db_result = db_conn.execute(query_carrito)

        db_conn.close()

        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'
    return None
    
def db_add_to_cart(id, customerid, quantity):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        query_carrito = "SELECT * FROM orders WHERE status is null and customerid = {}".format(customerid)
        db_result = db_conn.execute(query_carrito)
        row = db_result.fetchone()
        if not row: # si el usuario no tiene un carrito
            query_carrito = "INSERT INTO orders (orderdate, status, customerid) VALUES (NOW(), null, {})".format(customerid)
            db_conn.execute(query_carrito)
            query_carrito = "SELECT * FROM orders WHERE status is null and customerid = {}".format(customerid)
            db_result = db_conn.execute(query_carrito)
            row = db_result.fetchone()
        query_carrito = "SELECT * FROM orderdetail WHERE prod_id = {} and orderid = {}".format(id, row[0]) #id = prod_id, row[0] = orderid
        db_result = db_conn.execute(query_carrito)
        rowDetail = db_result.fetchone()
        if rowDetail:
            query_carrito = "UPDATE orderdetail SET quantity={} WHERE orderid = {} and prod_id = {}".format(rowDetail[3]+quantity, rowDetail[0], id)
            db_result = db_conn.execute(query_carrito)
        else:
            query_carrito = "SELECT price FROM products WHERE prod_id = {}".format(id) #id = prod_id, row[0] = orderid
            db_result = db_conn.execute(query_carrito)
            rowDetail = db_result.fetchone()
            price = rowDetail[0]
            query_carrito = "INSERT INTO orderdetail (orderid, prod_id, price, quantity) VALUES ({}, {}, {}, {})".format(row[0], id, price, quantity)
            db_conn.execute(query_carrito)
        db_conn.close()
        return True
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)
        return None
    
def db_comprarcarrito(userid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        saldo = db_saldo(userid)
        precioTotal = 0
        query_carrito = "SELECT * FROM orders WHERE status is null and customerid = {}".format(userid)
        db_result = db_conn.execute(query_carrito)
        row = db_result.fetchone() #row[0] = orderid del carrito
        query_carrito = "SELECT price FROM orderdetail WHERE orderid = {}".format(row[0]) #row[0] = orderid
        db_result = db_conn.execute(query_carrito)
        rowDetail = db_result.fetchone()
        while rowDetail:
            precioTotal += rowDetail[0] #precio
            rowDetail = db_result.fetchone()
        if saldo < precioTotal:
            return None
        else:
            saldo -= precioTotal
        movies = []
        query_carrito = "SELECT * FROM orders WHERE status is null and customerid={}".format(userid)
        db_result = db_conn.execute(query_carrito)
        row = db_result.fetchone()
        query_carrito = "SELECT * FROM orders WHERE status is null and customerid={}".format(userid)
        db_result = db_conn.execute(query_carrito)
        row = db_result.fetchone()
        query_carrito = "UPDATE orders SET status='Paid' WHERE orderid = {}".format(row[0])
        db_result = db_conn.execute(query_carrito)
        query_carrito = "UPDATE customers SET saldo={} WHERE customerid = {}".format(saldo, userid)
        db_result = db_conn.execute(query_carrito)
        db_conn.close()
        return True
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'
    
def db_borrarcarrito(userid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        movies = []
        #obtenemos el carrito
        query_carrito = "SELECT * FROM orders WHERE status is null and customerid={}".format(userid)
        db_result = db_conn.execute(query_carrito)
        row = db_result.fetchone()
        #borramos los detalles del carrito
        query_carrito = "DELETE FROM orderdetail WHERE orderid={}".format(row[0])
        db_conn.execute(query_carrito)
        #borramos el carrito
        query_carrito = "DELETE FROM orders WHERE orderid={}".format(row[0])
        db_conn.execute(query_carrito)
        db_conn.close()
        return True
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'
    
def db_borrarelemento(userid, prod_id):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        movies = []
        #obtenemos el carrito
        query_carrito = "SELECT * FROM orders WHERE status is null and customerid={}".format(userid)
        db_result = db_conn.execute(query_carrito)
        row = db_result.fetchone()
        #borramos los detalles del carrito
        query_carrito = "DELETE FROM orderdetail WHERE orderid={} and prod_id={}".format(row[0], prod_id)
        db_conn.execute(query_carrito)
        db_conn.close()
        return True
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_saldo(id):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        #obtenemos el saldo del usuario
        query_carrito = "SELECT saldo FROM customers WHERE customerid={}".format(id)
        db_result = db_conn.execute(query_carrito)
        row = db_result.fetchone()
        return row[0]
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return None

def db_topMovies_last3years():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        movies = []
        statement = text("""SELECT p.prod_id, p.movieid, movietitle, description, year, sum(quantity) as sales, p.price
                            FROM products p
                            JOIN imdb_movies im ON p.movieid = im.movieid
                            JOIN orderdetail od ON p.prod_id = od.prod_id
                            JOIN orders o ON od.orderid = o.orderid
                            WHERE (extract(year FROM o.orderdate) > (extract(year FROM now()) - 3)) AND o.status is not NULL
                            GROUP BY p.prod_id, description, movietitle, year
                            ORDER BY sales DESC
                            LIMIT 30;""")

        db_result = db_conn.execute(statement)
        row = db_result.fetchone()
        while row:
            movie = {
                "titulo": row[2],
                "edicion": row[3],
                "ventas": row[5],
                "precio": row[6],
                "prod_id": row[0]
            }
            movies.append(movie)
            row = db_result.fetchone()
        db_conn.close()

        return movies
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)