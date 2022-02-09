import pymongo
import database
import math


def crear_database():
    """
    Crea la base de datos en MongoDB a partir de la 
    información obtenida de la db de postgres
    """
    # Crea la database
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["si1"]

    # Borrar la colección topUSA si ya existía
    mydb['topUSA'].drop()

    # Se vuelve a crear
    collection = mydb['topUSA']

    # Obtenemos acceso a la DB de PostgreSQL para obtener los datos
    psql = database.DatabaseAccess('simongo')

    # Obtenemos los ids de todas las peliculas que debemos insertar en mongoDB
    ids = psql.consulta("select imdb_movies.movieid "
                        "from	imdb_movies, "
                        "imdb_moviecountries "
                        "where 	imdb_movies.movieid = imdb_moviecountries.movieid and "
                        "imdb_moviecountries.country = 'USA' "
                        "order by imdb_movies.year desc, imdb_movies.movietitle ASC "
                        "limit 800")

    # Creamos una lista para almacenar todos los documentos y para 
    # cada id de pelicula obtenemos los datos de la pelicula y creamos 
    # un documento/diccionario con esa información 
    peliculas = []

    for id in ids:
        document = {}
        # Obtener el titulo
        titulo = psql.consulta("select  movietitle "
                               "from    imdb_movies "
                               "where   movieid = {}".format(id[0]))
        document['title'] = titulo[0][0]

        # Obtener los géneros
        document['genres'] = []

        generos = psql.consulta("select  genre "
                                "from    imdb_moviegenres "
                                "where   imdb_moviegenres.movieid = {}".
                                format(id[0]))
        if generos is not None:
            for genero in generos:
                document['genres'].append(genero[0])
        # Obtener año
        year = psql.consulta("select  year "
                             "from    imdb_movies "
                             "where   movieid = {}".format(id[0]))
        document['year'] = year[0][0]

        # Obtener directores
        document['directors'] = []

        directores = psql.consulta("select  directorname "
                                   "from    imdb_directors, "
                                   "imdb_directormovies "
                                   "where   imdb_directormovies.movieid = {} and "
                                   "imdb_directormovies.directorid = imdb_directors.directorid".
                                   format(id[0]))

        if directores is not None:
            for director in directores:
                document['directors'].append(director[0])

        # Obtener actores
        document['actors'] = []
        actores = psql.consulta("select  actorname "
                                "from    imdb_actors, "
                                "imdb_actormovies "
                                "where   imdb_actormovies.movieid = {} and "
                                "imdb_actormovies.actorid = imdb_actors.actorid".
                                format(id[0]))

        if actores is not None:
            for actor in actores:
                document['actors'].append(actor[0])
        peliculas.append(document)

    collection.insert_many(peliculas)


def calcular_relaciones():
    """
    Calculas para todas las películas las películas más 
    relacionadas y las relacionadas
    """
    # Obtener acceso a la DB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["si1"]

    # Obtener acceso a la colección
    collection = mydb['topUSA']

    # Calculamos las películas más relacionadas y relacionadas
    for pelicula in collection.find():
        mas_relacionadas = []
        relacionadas = []
        result = []

        cursor = collection.find({'genres': pelicula['genres']}). \
            sort('year', -1)
        for item in cursor:
            if item['_id'] != pelicula['_id']:
                result.append(item)

        for i in range(0, min(10, len(result))):
            mas_relacionadas.append({'title': result[i]['title'],
                                     'year': result[i]['year']})

        # Añadir al documento las películas más relacionadas
        collection.update({'_id': pelicula['_id']},
                          {'$set': {'most_related_movies': mas_relacionadas}})

        if len(pelicula['genres']) == 1:
            collection.update({'_id': pelicula['_id']},
                              {'$set': {'related_movies': []}})
        else:
            if len(result) > 10:
                # El resto de las más relacionadas se incluyen en relacionadas
                for i in range(10, min(20, len(result))):
                    relacionadas.append({'title': result[i]['title'],
                                         'year': result[i]['year']})

            # Calcular las películas relacionadas
            if len(relacionadas) < 10:
                filtro = [{"$project": {
                    "title": 1,
                    "year": 1,
                    "common": {"$size": {
                        "$setIntersection": [pelicula['genres'], "$genres"]}}
                }
                }, {"$match": {
                    "$and": [
                        {"common": {
                            "$gte": math.floor(len(pelicula['genres']) / 2)}},
                        {"common": {"$lt": len(pelicula['genres'])}}
                    ]
                }
                }, {"$sort": {
                    "common": -1,
                    "year": -1,
                    "title": 1
                }
                }, {"$limit": 10 - len(relacionadas)}]

                for item in collection.aggregate(filtro):
                    relacionadas.append(
                        {'title': item['title'], 'year': item['year']})

            # Añadir al documento las películas relacionadas
            collection.update({'_id': pelicula['_id']},
                              {'$set': {'related_movies': relacionadas}})


if __name__ == "__main__":
    crear_database()
    calcular_relaciones()
