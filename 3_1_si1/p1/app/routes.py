#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session, \
    flash, make_response
import json
import os
import random
import hashlib
from datetime import date


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    catalogue_data = open(os.path.join(app.root_path,
                                       'catalogue/catalogue.json'),
                          encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    categories = ['Todas']
    for movie in catalogue['peliculas']:
        if movie['categoria'] not in categories:
            categories.append(movie['categoria'])

    if request.method == 'GET':
        return render_template('index.html', title="Home",
                               movies=catalogue['peliculas'],
                               categories=categories)
    else:
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
                                    movie['categoria'] == request.
                                    form['category'])]

        return render_template('index.html', title="Home",
                               movies=search_catalogue, categories=categories)


@app.route('/login', methods=['GET', 'POST'])
def login():
    salt = "0asdf56qwef4asdf!"
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            path = os.path.join(os.path.dirname(app.root_path), 'usuarios',
                                request.form['username'])
            if os.path.exists(path) and os.path.isdir(path):
                datos = open(os.path.join(path, 'datos.dat'),
                             encoding="utf-8").read()
                datos_dict = json.loads(datos)
                if datos_dict['password'] == hashlib.sha512(
                        (salt + request.form['password']).encode(
                                'utf-8')).hexdigest():
                    session['usuario'] = request.form['username']
                    session.modified = True
                    return redirect(url_for('index'))
                else:
                    return render_template('login.html', title="Sign In")
            else:
                return render_template('login.html', title="Sign In")
    else:
        return render_template('login.html', title='Sign In',
                               last_user=request.cookies.get('last_user'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('last_user', session['usuario'])
    session.pop('usuario', None)
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    salt = "0asdf56qwef4asdf!"
    if request.method == 'GET':
        return render_template('register.html', title='Register')
    else:
        path = os.path.join(os.path.dirname(app.root_path), 'usuarios')
        if not (os.path.exists(path) and os.path.isdir(path)):
            os.mkdir(path)
            os.chmod(path, 0o777)

        path = os.path.join(path, request.form['username'])
        if os.path.exists(path) and os.path.isdir(path):
            return render_template('register.html', title='Register')

        os.mkdir(path)
        os.chmod(path, 0o777)
        data_dict = {}
        hist_dict = {}
        for i in request.form:
            data_dict[i] = request.form[i]

        data_dict['password'] = hashlib.sha512(
            (salt + request.form['password']).encode('utf-8')).hexdigest()
        data_dict['saldo'] = float(random.randint(0, 100))
        hist_dict['compras'] = []
        save_user_data(request.form['username'], data_dict)
        save_user_history(request.form['username'], hist_dict)
        session['usuario'] = request.form['username']
        session.modified = True
        return redirect(url_for('index'))


@app.route('/carrito', methods=['GET', 'POST'])
def carrito():
    carrito_data = []
    total_pagar = 0
    if 'carrito' in session:
        for movie_id in session['carrito']:
            movie = search_movie_by_id(int(movie_id))
            if movie is not None:
                carrito_data.append((movie, session['carrito'][movie_id]))
                total_pagar += movie['precio'] * session['carrito'][movie_id]

    saldo = None
    if 'usuario' in session:
        saldo = load_user_data(session['usuario'])['saldo']

    if request.method == 'GET':
        return render_template('carrito.html', title="Tu carro",
                               carrito=carrito_data,
                               total_pagar=round(total_pagar, 2), saldo=saldo)
    else:
        if 'usuario' not in session:
            flash('Debes estar loggeado para finalizar la compra')
            return redirect(url_for('login'))
        elif not carrito_data:
            flash('El carro está vacío')
            return render_template('carrito.html', title="Tu carro",
                                   carrito=carrito_data,
                                   total_pagar=round(total_pagar, 2),
                                   saldo=saldo)
        else:
            user_data = load_user_data(session['usuario'])
            if total_pagar > user_data['saldo']:
                flash("Saldo Insuficiente")
                return render_template('carrito.html', title="Tu carro",
                                       carrito=carrito_data,
                                       total_pagar=round(total_pagar, 2),
                                       saldo=saldo)
            else:
                user_data['saldo'] = round(user_data['saldo'] - total_pagar, 2)
                save_user_data(session['usuario'], user_data)
                user_history = load_user_history(session['usuario'])
                pedido_peliculas = []
                for movie, quantity in carrito_data:
                    for i in range(quantity):
                        pedido_peliculas.append(movie['id'])

                pedido_id = calculate_history_id(user_history)
                user_history['compras'].append(
                    {'id': pedido_id, 'fecha': str(date.today()),
                     'precio': round(total_pagar, 2),
                     'peliculas': pedido_peliculas})

                save_user_history(session['usuario'], user_history)
                session['carrito'] = {}
                session.modified = True
                return redirect(url_for('historial'))


@app.route('/historial', methods=['GET', 'POST'])
def historial():
    if request.method == 'GET':
        if 'usuario' in session:
            history = load_user_history(session['usuario'])
            for pedido in history['compras']:
                pedido['peliculasfull'] = []
                for pelicula_id in pedido['peliculas']:
                    pelicula = search_movie_by_id(pelicula_id)
                    pedido['peliculasfull'].append(
                        (pelicula['titulo'], pelicula['precio']))

            return render_template('historial.html', title="Historial",
                                   saldo=load_user_data(session['usuario'])[
                                       'saldo'], compras=history['compras'])
        else:
            return redirect(url_for('login'))
    else:
        user_data = load_user_data(session['usuario'])
        user_data['saldo'] = round(float(request.form['saldo']), 2)
        save_user_data(session['usuario'], user_data)
        return redirect(url_for('historial'))


@app.route('/detail/<int:movie_id>', methods=['GET', 'POST'])
def detail(movie_id):
    print(movie_id)
    if request.method == 'GET':
        return render_template('detail.html', title="Detalle",
                               movie=search_movie_by_id(movie_id))
    else:
        # Crear el carrito en la sesión si no existe y añadirlo al carrito
        # (o incrementar la cantidad en 1)
        if 'carrito' not in session:
            session['carrito'] = {}

        if str(movie_id) in session['carrito']:
            session['carrito'][str(movie_id)] += 1
        else:
            session['carrito'][str(movie_id)] = 1

        session.modified = True
        return redirect(url_for('detail', movie_id=movie_id))


@app.route('/add_one_movie/<int:movie_id>', methods=['POST'])
def add_one_movie(movie_id):
    session['carrito'][str(movie_id)] += 1
    session.modified = True
    return redirect(url_for('carrito'))


@app.route('/sub_one_movie/<int:movie_id>', methods=['POST'])
def sub_one_movie(movie_id):
    session['carrito'][str(movie_id)] -= 1
    if session['carrito'][str(movie_id)] == 0:
        session['carrito'].pop(str(movie_id), None)

    session.modified = True
    return redirect(url_for('carrito'))


@app.route('/vaciar_carro', methods=['POST'])
def vaciar_carro():
    session['carrito'] = {}
    session.modified = True
    return redirect(url_for('carrito'))


@app.route('/generar', methods=['GET'])
def generar():
    return str(random.randint(1, 400))


def search_movie_by_id(movie_id):
    catalogue_data = open(
        os.path.join(app.root_path, 'catalogue/catalogue.json'),
        encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    for movie in catalogue['peliculas']:
        if movie['id'] == movie_id:
            return movie

    return None


def load_user_data(usuario):
    path = os.path.join(os.path.dirname(app.root_path), 'usuarios', usuario,
                        'datos.dat')
    if os.path.exists(path):
        datos_data = open(path, encoding="utf-8").read()
        datos = json.loads(datos_data)
        return datos
    else:
        return None


def load_user_history(usuario):
    path = os.path.join(os.path.dirname(app.root_path), 'usuarios', usuario,
                        'historial.json')
    if os.path.exists(path):
        datos_data = open(path, encoding="utf-8").read()
        datos = json.loads(datos_data)
        return datos
    else:
        return None


def save_user_data(usuario, data):
    if os.path.exists(
            os.path.join(os.path.dirname(app.root_path), 'usuarios', usuario)):
        path = os.path.join(os.path.dirname(app.root_path), 'usuarios',
                            usuario, 'datos.dat')
        with open(path, 'w') as outfile:
            json.dump(data, outfile)


def save_user_history(usuario, hist):
    if os.path.exists(
            os.path.join(os.path.dirname(app.root_path), 'usuarios', usuario)):
        path = os.path.join(os.path.dirname(app.root_path), 'usuarios',
                            usuario, 'historial.json')
        with open(path, 'w') as outfile:
            json.dump(hist, outfile)


def calculate_history_id(history):
    max_id = 0
    for pedido in history['compras']:
        if pedido['id'] > max_id:
            max_id = pedido['id']

    return max_id + 1
