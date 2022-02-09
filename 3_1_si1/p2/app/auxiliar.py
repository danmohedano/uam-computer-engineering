import os
from app import app
import json


def search_movie_by_id(movie_id):
    """
    Método que busca una película a raiz de su id
    :param movie_id: el id de la pelicula
    :return: la pelicula (diccionario con la informacion), None si no existe
    """
    catalogue_data = open(
        os.path.join(app.root_path, 'catalogue/catalogue.json'),
        encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    for movie in catalogue['peliculas']:
        if movie['id'] == movie_id:
            return movie

    return None


def search_movie_by_prod_id(prod_id):
    """
    Método que busca una película a raiz de su prod_id
    :param prod_id: id del producto
    :return: la pelicula con ese producto
    """
    catalogue_data = open(
        os.path.join(app.root_path, 'catalogue/catalogue.json'),
        encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    for movie in catalogue['peliculas']:
        if movie['producto'] == prod_id:
            return movie

    return None
