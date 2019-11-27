#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from app import database
from flask import render_template, request, url_for, redirect, session, make_response, Flask, jsonify, request
import json
import os
import sys
import hashlib
from random import randrange
from flask import flash
import ast
from datetime import date
import random 
import datetime


@app.route('/', methods=['POST', 'GET', 'PUT'])
@app.route('/index', methods=['POST', 'GET', 'PUT'])
def index():
    top_last3years = database.db_topMovies_last3years()
    if 'user_id' in session:
        saldo = database.db_saldo(session['user_id'])
        if saldo:
            session['saldo'] = int(saldo)
        else:
            session['saldo'] = 0

    return render_template('index.html', title="Home", top_movies=top_last3years, session=session)



@app.route('/<titulo>')
def detalle(titulo):
    catalogue_data = open(os.path.join(
        app.root_path, 'catalogue/catalogo.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    movies = catalogue['peliculas']
    pelicula = next((item for item in movies if item["titulo"] == titulo), False)
    
    if 'logged_in' in session:
        if pelicula:
            historial_dir = open(os.path.join(app.root_path, 'usuarios',
                                            session['usuario'], 'historial.json'), encoding="utf-8").read()
            compradas = []
            historial = json.loads(historial_dir)
            datosHistorial = historial['historial']
            for x in datosHistorial:
                for y in x['peliculas']:
                    compradas.append(int(y))
            if int(pelicula['id']) in compradas:
                return render_template('detail.html', coleccion='true', selection=pelicula)
    
    return render_template('detail.html', selection=pelicula)


@app.route('/sesion')
def sesion():
    last_user = request.cookies.get('username')
    if last_user:
        return render_template('sesion.html', title="Sesion", last_user=last_user)
    return render_template('sesion.html', title="Sesion")


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == "POST":
        usuario = {"username": request.form['usuario'],
                   "nombre": request.form['nombre'],
                   "apellidos": request.form['apellidos'],
                   "direccion": request.form['direccion'],
                   "region": request.form['region'],
                   "pais": request.form['pais'],
                   "ciudad": request.form['ciudad'],
                   "password": request.form['password'],
                   "email": request.form['email'],
                   "genero": request.form['genero'],
                   "edad": request.form['edad'],
                   "card_type": request.form['card_type'],
                   "tarjeta": request.form['tarjeta'],
                   "caducidad_tarjeta": datetime.datetime.strptime(request.form['cardexpiration'],
                                                                   '%Y-%m-%d').strftime('%Y%d%m')[2:],
                   "saldo":  randrange(101),
                   "nPedidos": 0}
        
        if database.db_check_user(usuario['username']) is True:
            flash('¡El usuario ya existe!')
            return redirect(url_for('sesion'))

        database.db_registro(usuario)

        # directorio = os.path.join(
        #     app.root_path, 'usuarios', request.form['usuario'])
        # try:
        #     os.makedirs(directorio)
        # except OSError:
        #     flash('¡El usuario ya existe!')
        #     return redirect(url_for('sesion'))

        # directorio = os.path.join(
        #     app.root_path, 'usuarios', request.form['usuario'], 'datos.dat')
        # data_file = open(directorio, "w")
        # data_file.write(str(usuario))
        # data_file.close()

        # directorio = os.path.join(
        #     app.root_path, 'usuarios', request.form['usuario'], 'historial.json')
        # historial = open(directorio, "w")
        # json.dump({
        #     "historial": []
        # }, historial)
        # historial.close()
        
        
        session['logged_in'] = True
        session['usuario'] = usuario['username']
        session["saldo"] = usuario['saldo']
        session.modified = True

        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('username', usuario['username'])
        return resp

    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        usuario = request.form['usuario']
        password = request.form['password']

        if database.db_check_user(usuario) is False:
            flash('¡El usuario no existe!')
            flash('Puedes registrarte en esta misma página.')
            return redirect(url_for('sesion'))

        user_id = database.db_check_login(usuario, password)
        if user_id is None:
            flash('¡Contraseña errónea!')
            return redirect(url_for('sesion'))

        session['logged_in'] = True
        session['user_id'] = user_id
        session['usuario'] = request.form['usuario']
        session["saldo"] = randrange(101)
        session.modified = True

        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('username', usuario)
        return resp
    else:
        flash('Error en el login, pruebe otra vez.')
        return redirect(url_for('sesion'))


@app.route('/logout/<user>')
def logout(user):
    if 'logged_in' in session:
        session.pop('usuario', None)
        session.pop('logged_in', None)
        session.modified = True
    else:
        flash('Hubo un error al cerrar sesión')

    return redirect(url_for('index'))


@app.route("/carrito")
def carrito():
    if 'user_id' in session:
        movies = database.db_carrito(session['user_id'])
    else:
        session['cart'].append(int(id))
    # catalogue_data = open(os.path.join(
    #     app.root_path, 'catalogue/catalogo.json'), encoding="utf-8").read()
    # catalogue = json.loads(catalogue_data)

    # ids_in_cart = session.get('cart', [])
    # movies = []
    # precio = 0

    # for x in catalogue['peliculas']:
    #     if x['id'] in ids_in_cart:
    #         movies.append(x)
    #         precio += x['precio']
    # session['total'] = precio
    # session.modified = True
    if not movies:
        movies = []
    precio = 0
    for movie in movies:
        precio += movie["precio"]*movie["cantidad"]
    return render_template("carrito.html", movies=movies, precio=precio)


@app.route("/pedidos")
def pedidos():
    catalogue_data = open(os.path.join(
        app.root_path, 'catalogue/catalogo.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    if 'logged_in' in session:
        historial_dir = open(os.path.join(app.root_path, 'usuarios',
                                          session['usuario'], 'historial.json'), encoding="utf-8").read()
        historial = json.loads(historial_dir)
        datosHistorial = historial['historial']

        return render_template("pedidos.html", datosHistorial=datosHistorial, movies=catalogue['peliculas'])
    redirect(url_for('index'))
    
    
@app.route("/coleccion")
def coleccion():
    catalogue_data = open(os.path.join(
        app.root_path, 'catalogue/catalogo.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    if 'logged_in' in session:
        historial_dir = open(os.path.join(app.root_path, 'usuarios',
                                          session['usuario'], 'historial.json'), encoding="utf-8").read()
        movies = []
        historial = json.loads(historial_dir)
        datosHistorial = historial['historial']
        for x in datosHistorial:
            for y in x['peliculas']:
                for z in catalogue['peliculas']:
                    if y == z['id']:
                        movies.append(z)

        return render_template("coleccion.html", movies=movies)
    redirect(url_for('carrito'))


@app.route("/add_to_cart/<id>")
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = []
    if 'user_id' in session:
        database.db_add_to_cart(id, session['user_id'], 1)
    else:
        session['cart'].append(int(id))

    flash('Elemento añadido al carrito')

    return redirect(url_for('index'))


@app.route('/borrarCarrito')
def borrarCarrito():
    if 'user_id' in session:
        database.db_borrarcarrito(session['user_id'])
    session.pop('cart', None)
    session.modified = True

    return redirect(url_for('carrito'))


@app.route('/borrarElemento/<id>')
def borrarElemento(id):
    if 'user_id' in session:
        database.db_borrarelemento(session['user_id'], id)
    else:
        session['cart'].remove(int(id))
        session.modified = True

    return redirect(url_for('carrito'))


@app.route('/comprarCarrito')
def comprarCarrito():
    if 'logged_in' in session:
        retorno = database.db_comprarcarrito(session['user_id'])
        if not retorno:
            flash('No tienes suficiente saldo')
            return redirect(url_for('carrito'))
        flash('¡Carrito comprado!')
        return redirect(url_for('carrito'))
        # directorio = os.path.join(
        #     app.root_path, 'usuarios', session['usuario'], 'datos.dat')
        # try:
        #     with open(directorio, "r") as data_file:
        #         data_dictionary = ast.literal_eval(data_file.read())
        # except IOError:
        #     flash('¡El usuario no existe!')
        # saldo = data_dictionary.get('saldo')
        # if saldo >= session['total']:
        #     catalogue_data = open(os.path.join(
        #         app.root_path, 'catalogue/catalogo.json'), encoding="utf-8").read()
        #     catalogue = json.loads(catalogue_data)

        #     ids_in_cart = session.get('cart', [])

        #     historial_data = open(os.path.join(
        #         app.root_path, 'usuarios', session['usuario'], 'historial.json'), encoding="utf-8").read()
        #     historial = json.loads(historial_data)
        #     datosHistorial = historial['historial']
        #     id = data_dictionary.get('nPedidos')
        #     data = {
        #         "id": id,
        #         "fecha": str(date.today()),
        #         "precio": session['total'],
        #         "peliculas": ids_in_cart
        #     }
        #     datosHistorial.append(data)

        #     directorioHistorial = os.path.join(
        #         app.root_path, 'usuarios', session['usuario'], 'historial.json')
        #     file = open(directorioHistorial, "w")
        #     json.dump({
        #         "historial": datosHistorial}, file)
        #     file.close()
        #     session.pop('cart', None)
        #     session.modified = True
        #     data_dictionary["saldo"] -= session['total']
        #     data_dictionary["nPedidos"] += 1

        #     directorio_datos = os.path.join(
        #         app.root_path, 'usuarios', session['usuario'], 'datos.dat')
        #     datos_file = open(directorio_datos, "w")
        #     datos_file.write(str(data_dictionary))
        #     datos_file.close()
        #     session["saldo"] = data_dictionary["saldo"]

        #     flash('¡Carrito comprado!')
        #     return redirect(url_for('carrito'))
        # else:
        #     flash('No tienes suficiente saldo. Haz click en saldo (barra lateral) para añadir más')
        #     return redirect(url_for('carrito'))
    else:
        flash('¡Para comprar debes estar logueado!')
        return redirect(url_for('sesion'))

@app.route('/saldo')
def saldo():
    return render_template("saldo.html", title="Saldo", session=session)


@app.route('/aumentarSaldo', methods=['GET', 'POST'])
def aumentarSaldo():
    if request.method == "POST":
        aumento = int(request.form['cantidad'])

        directorio = os.path.join(
            app.root_path, 'usuarios', session['usuario'], 'datos.dat')
        try:
            with open(directorio, "r+") as data_file:
                data_dictionary = ast.literal_eval(data_file.read())
                saldo = data_dictionary.get('saldo')
                saldo += aumento
                data_dictionary['saldo'] = saldo
                data_file.seek(0)
                data_file.write(str(data_dictionary))
                data_file.truncate()
        except IOError:
            flash('¡El usuario no existe!')
            return redirect(url_for('saldo'))

        session["saldo"] += aumento
        session.modified = True
        flash('¡Saldo aumentado!')
        return redirect(url_for('index'))
    else:
        flash('Error al incrementar saldo, pruebe otra vez.')
        return redirect(url_for('saldo'))


@app.route('/connectedUsers')
def connectedUsers():
    return jsonify(result = random.randrange(150,200))

