#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from app import database
from app import auxiliar
from flask import render_template, request, url_for, redirect, session, \
    make_response, flash
import json
import os
import random

DB_ACCESS = database.DatabaseAccess()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    Método que se encarga de manejar la página principal donde se muestra el
    catálogo de películas y la tabla con el
    resultado de la query getTopVentas()
    """
    # Se carga el catálogo
    catalogue_data = open(os.path.join(app.root_path,
                                       'catalogue/catalogue.json'),
                          encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    # Se cargan las categorías
    categories = ['Todas'] + DB_ACCESS.db_get_genres()

    if request.method == 'GET':
        top_peliculas = DB_ACCESS.db_top_ventas()
        return render_template('index.html', title="Home",
                               movies=catalogue['peliculas'],
                               categories=categories,
                               top_peliculas=top_peliculas)
    else:
        # Si el método es POST se trata el formulario enviado
        # para la búsqueda de películas en el catálogo
        str_titulo = ""
        if 'titulo' in request.form:
            str_titulo = request.form['titulo']

        if request.form['category'] == 'Todas':
            search_catalogue = [movie for movie in catalogue['peliculas']
                                if str_titulo.lower() in
                                movie['titulo'].lower()]
        else:
            search_catalogue = [movie for movie in catalogue['peliculas']
                                if (str_titulo.lower() in
                                    movie['titulo'].lower() and
                                    request.form['category'] in movie[
                                        'categoria'])]

        return render_template('index.html', title="Home",
                               movies=search_catalogue, categories=categories)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Método que se encarga de loguear al usuario
    """
    if request.method == 'POST':
        # Si en el formulario enviado se han incluido
        # los campos email y password
        if 'email' in request.form and 'password' in request.form:
            # Comprobar que el usuario existe
            user_data = DB_ACCESS.db_get_user_info(request.form['email'])
            if user_data is not None:
                # Comprobar si la contraseña es la correcta (columna 16)
                if request.form['password'] == user_data[16]:
                    # Guardar la id del usuario para identificarlo
                    session['usuario'] = user_data[0]
                    session['user_nombre'] = user_data[15]
                    session['user_email'] = request.form['email']
                    session.modified = True
                    # Comprobar si había un carro en la sesión
                    # (mientras no estaba loggeado)
                    if 'carrito' in session:
                        # Si lo había, pasar los contenidos al
                        # pedido activo del usuario
                        orderid = DB_ACCESS.db_get_order(session['usuario'])
                        if orderid is None:
                            orderid = DB_ACCESS.db_create_order(
                                session['usuario'])

                        for movie_id in session['carrito']:
                            movie = auxiliar.search_movie_by_id(int(movie_id))
                            if movie is not None:
                                for i in range(session['carrito'][movie_id]):
                                    DB_ACCESS.db_order_add_product(orderid,
                                                                   movie)

                        session.pop('carrito', None)

                    if 'url_origen' in session:
                        url = session['url_origen']
                        session.pop('url_origen', None)
                        return redirect(url)
                    else:
                        return redirect(url_for('index'))
                else:
                    # Error en el login si la contraseña
                    # y/o usuario son incorrectos
                    return render_template('login.html', title="Sign In",
                                           error_msg='La combinación usuario/'
                                                     'contraseña no es la corr'
                                                     'ecta.')
            else:
                # Error en el login si no existe el usuario
                return render_template('login.html', title="Sign In",
                                       error_msg='No existe este usuario.')
    else:
        return render_template('login.html', title='Sign In',
                               last_user=request.cookies.get('last_user'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    Método que se encarga de cerrar la sesión
    """
    response = make_response(redirect(url_for('index')))
    response.set_cookie('last_user', session['user_email'])
    session.pop('usuario', None)
    session.pop('user_nombre', None)
    session.pop('user_email', None)
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Método que se encarga de registrar nuevos usuarios
    """
    if request.method == 'GET':
        return render_template('register.html', title='Register')
    else:

        if DB_ACCESS.db_get_user_info(request.form['email']) is not None:
            # Si ya existe el usuario que se pretende registrar,
            # volver a la página de registro
            return render_template('register.html', title='Register',
                                   error_msg='Este usuario ya existe.')

        # Si el usuario no existe, se registra
        user_id = DB_ACCESS.db_register_user(request.form['username'],
                                             request.form['password'],
                                             request.form['email'],
                                             request.form['cardnumber'])

        session['usuario'] = user_id
        session['user_nombre'] = request.form['username']
        session['user_email'] = request.form['email']
        session.modified = True
        return redirect(url_for('index'))


@app.route('/carrito', methods=['GET', 'POST'])
def carrito():
    """
    Método utilizado para el manejo del carrito del usuario conectado.
    """
    session['url_origen'] = url_for('carrito')
    session.modified = True
    carrito_data = []
    total_pagar = 0
    if 'usuario' in session:
        # Si el usuario está loggeado, se obtienen los datos de la DB
        orderid = DB_ACCESS.db_get_order(session['usuario'])
        if orderid is not None:
            # Si tiene un pedido activo, se obtienen los datos
            total_pagar = DB_ACCESS.db_get_order_price(orderid)
            productos = DB_ACCESS.db_get_order_products(orderid)
            for p, quantity in productos:
                movie = auxiliar.search_movie_by_prod_id(p)
                if movie is not None:
                    carrito_data.append((movie, quantity))
    else:
        # Si no está loggeado, se obtienen de la sesión flask
        if 'carrito' in session:
            for movie_id in session['carrito']:
                movie = auxiliar.search_movie_by_id(int(movie_id))
                if movie is not None:
                    carrito_data.append((movie, session['carrito'][movie_id]))
                    total_pagar += movie['precio'] * session['carrito'][
                        movie_id]

            # Incrementar el total a pagar por los impuestos (15%)
            total_pagar *= 1.15

    saldo = None
    # Se carga el saldo del usuario en la sesión
    if 'usuario' in session:
        user_data = DB_ACCESS.db_get_user_info(session['user_email'])
        if user_data is None:
            return redirect(url_for('logout'))

        saldo = float(user_data[20])

    if request.method == 'GET':
        return render_template('carrito.html', title="Tu carro",
                               carrito=carrito_data,
                               total_pagar=round(total_pagar, 2), saldo=saldo)
    else:
        # Si el usuario no está conectado no puede usar el carrito,
        # por lo que es redirigido a la página de inicio de sesión
        if 'usuario' not in session:
            return redirect(url_for('login'))
        elif not carrito_data:
            return render_template('carrito.html', title="Tu carro",
                                   carrito=carrito_data,
                                   total_pagar=round(total_pagar, 2),
                                   saldo=saldo,
                                   error_msg='El carro está vacío.')
        else:
            # Se indica que el usuario no tiene suficiente
            # saldo para realizar la compra
            if total_pagar > saldo:
                return render_template('carrito.html', title="Tu carro",
                                       carrito=carrito_data,
                                       total_pagar=round(total_pagar, 2),
                                       saldo=saldo,
                                       error_msg='Saldo insuficiente.')
            else:
                DB_ACCESS.db_order_pay(orderid, total_pagar,
                                       session['usuario'], saldo)
                return redirect(url_for('historial'))


@app.route('/historial', methods=['GET', 'POST'])
def historial():
    """
    Método utilizado para manejar el historial del usuario conectado y
    la edición del saldo
    """
    if request.method == 'GET':
        # Si el usuario está loggeado, mostrar el historial
        if 'usuario' in session:
            historial_data = DB_ACCESS.db_get_history(session['usuario'])
            user_data = DB_ACCESS.db_get_user_info(session['user_email'])
            if user_data is None:
                return redirect(url_for('logout'))

            saldo = float(user_data[20])

            return render_template('historial.html', title="Historial",
                                   saldo=saldo, compras=historial_data)
        # Si no está loggeado, redirigir al login
        else:
            session['url_origen'] = url_for('historial')
            session.modified = True
            return redirect(url_for('login'))
    else:
        # Se guarda el nuevo saldo proporcionado en el post
        DB_ACCESS.db_update_saldo(session['usuario'],
                                  round(float(request.form['saldo']), 2))
        return redirect(url_for('historial'))


@app.route('/detail/<int:movie_id>', methods=['GET', 'POST'])
def detail(movie_id):
    """
    Método utilizado para mostrar los detalles de una película y manejar
    la inclusión de la película en el carro.
    """
    session['url_origen'] = url_for('detail', movie_id=movie_id)
    session.modified = True

    if request.method == 'GET':
        return render_template('detail.html', title="Detalle",
                               movie=auxiliar.search_movie_by_id(movie_id))
    else:
        correct_msg = 'Acción completada correctamente.'
        error_msg = 'Acción no se pudo completar. Stock insuficiente'

        # Crear el carrito en la sesión si no existe y añadirlo al carrito
        # (o incrementar la cantidad en 1) si el usuario no esta loggeado
        if 'usuario' not in session:
            if 'carrito' not in session:
                session['carrito'] = {}

            if str(movie_id) in session['carrito']:
                session['carrito'][str(movie_id)] += 1
            else:
                session['carrito'][str(movie_id)] = 1

            session.modified = True
            return render_template('detail.html', title="Detalle",
                                   movie=auxiliar.search_movie_by_id(movie_id),
                                   msg=correct_msg)
        else:
            # Si el usuario si está loggeado, se debe
            # incluir en la tabla de la DB
            orderid = DB_ACCESS.db_get_order(session['usuario'])
            if orderid is None:
                # Si no tiene un pedido activo, se crea
                orderid = DB_ACCESS.db_create_order(session['usuario'])

            movie = auxiliar.search_movie_by_id(movie_id)
            if DB_ACCESS.db_order_add_product(orderid, movie) == 0:
                return render_template('detail.html', title="Detalle",
                                       movie=auxiliar.search_movie_by_id(
                                           movie_id),
                                       msg=correct_msg)
            else:
                return render_template('detail.html', title="Detalle",
                                       movie=auxiliar.search_movie_by_id(
                                           movie_id),
                                       msg=error_msg)


@app.route('/add_one_movie/<int:movie_id>', methods=['POST'])
def add_one_movie(movie_id):
    """
    Método utilizado para aumentar en 1 la cantidad en el carro de la película
    indicada en la URL
    """
    if 'usuario' not in session:
        session['carrito'][str(movie_id)] += 1
        session.modified = True
    else:
        movie = auxiliar.search_movie_by_id(movie_id)
        orderid = DB_ACCESS.db_get_order(session['usuario'])
        if DB_ACCESS.db_order_add_product(orderid, movie) != 0:
            # Mostrar mensaje de error
            flash('Acción no se pudo completar. Stock insuficiente')

    return redirect(url_for('carrito'))


@app.route('/sub_one_movie/<int:movie_id>', methods=['POST'])
def sub_one_movie(movie_id):
    """
    Método utilizado para reducir en 1 la cantidad en el carro de la película
    indicada en la URL
    """
    if 'usuario' not in session:
        session['carrito'][str(movie_id)] -= 1
        if session['carrito'][str(movie_id)] == 0:
            session['carrito'].pop(str(movie_id), None)

        session.modified = True
    else:
        movie = auxiliar.search_movie_by_id(movie_id)
        orderid = DB_ACCESS.db_get_order(session['usuario'])
        DB_ACCESS.db_order_remove_product(orderid, movie)

    return redirect(url_for('carrito'))


@app.route('/vaciar_carro', methods=['POST'])
def vaciar_carro():
    """
    Método utilizado para vaciar el carro
    """
    if 'usuario' not in session:
        session['carrito'] = {}
        session.modified = True
    else:
        orderid = DB_ACCESS.db_get_order(session['usuario'])
        if orderid is not None:
            DB_ACCESS.db_order_empty(orderid)

    return redirect(url_for('carrito'))


@app.route('/generar', methods=['GET'])
def generar():
    """
    Método llamado por AJAX para generar aleatóriamente
    el número de usuarios conectados
    """
    return str(random.randint(1, 400))


@app.route('/topusa', methods=['GET'])
def topusa():
    """
    Método encargado de calcular las tablas y mostrar la información
    de la colección topUSA
    """
    tabla1 = DB_ACCESS.db_get_tabla1()
    tabla2 = DB_ACCESS.db_get_tabla2()
    tabla3 = DB_ACCESS.db_get_tabla3()
    return render_template('topusa.html', title="TopUSA", tabla1=tabla1,
                            tabla2=tabla2, tabla3=tabla3)