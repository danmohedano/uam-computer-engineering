# -*- coding: utf-8 -*-

import datetime
import random
import sys
import traceback

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import NullPool


class DatabaseAccess:
    """
    Clase que maneja el acceso a la base de datos

    Originalmente creada para evitar crear una nueva conexión cada vez que
    se realiza una query pero eso no funciona con Apache puesto que deja
    las conexiones abiertas (el objeto nunca se destruye). Simplemente
    agrupa toda la funcionanildad con la base de datos.
    """

    def __init__(self):
        self.db_engine = create_engine("postgresql://alumnodb:alumnodb"
                                       "@localhost/si1",
                                       echo=False, poolclass=NullPool)
        self.db_meta = MetaData(bind=self.db_engine)

    def treat_error(self):
        """
        Trata errores de la DB
        """
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return None

    def consulta(self, text):
        """
        Esta función se encarga de ejecutar la consulta que se le pasa en
        formato de texto (así no se repite el mismo código en todas las
        funciones).
        :param text: texto con la consulta
        :return: resultado de la consulta
        """
        try:
            with self.db_engine.connect() as connection:
                db_result = connection.execute(text)
                if db_result.returns_rows:
                    db_result = list(db_result)
                    if len(db_result) == 0:
                        return None

                    return db_result
                return None

        except SQLAlchemyError:
            return self.treat_error()

    def db_top_ventas(self):
        """
        Obtiene las películas más vendidas en los últimos 3 años a través
        de la función getTopVentas()
        :return: las peliculas con el formato (año, titulo, ventas)
        """
        now = datetime.datetime.now()
        query = "SELECT * " \
                "FROM getTopVentas({}, {})".format(now.year - 2, now.year)

        result = self.consulta(query)
        return result

    def db_get_user_info(self, user_email):
        """
        Obtiene la información de un usuario a partir de su email.
        Esto es utilizado sobretodo cuando el usuario intenta loggearse
        a través de su email.
        :param user_email: email del usuario que se busca
        :return: el customerid si lo encuentra, None si no
        """
        query = "SELECT * " + \
                "FROM customers " + \
                "WHERE email = '{}'".format(user_email)

        result = self.consulta(query)
        if result is None:
            return None
        else:
            return result[0]

    def db_register_user(self, username, password, email, cardnumber):
        """
        Esta función registra en la database un usuario y devuelve su
        nuevo customerid
        :param username: nombre del usuario a registrar
        :param password: contraseña del usuario a registrar
        :param email: email del usuario a registrar
        :param cardnumber: numero de tarjeta del usuario a registrar
        :return: customerid del usuario creado
        """
        # Los campos de la DB que no pueden ser NULL se han decidido rellenar
        # con datos genéricos (firstname, lastname, address1, city, country,
        # region, creditcardtype, creditcardexpiration)
        query = "INSERT INTO public.customers (customerid, firstname, " \
                "lastname, address1, city, country, region, creditcardtype, " \
                "creditcardexpiration, username, password, email, " \
                "creditcard, saldo) " \
                "VALUES ({}, 'John', 'Smith', 'francisco tomás valiente 11'," \
                " 'Madrid', 'Spain', 'region', 'VISA', 'never', '{}', '{}', " \
                "'{}', '{}', {}) " \
                "RETURNING customerid".format(self.db_max_customerid() + 1,
                                              username, password, email,
                                              cardnumber,
                                              random.randint(1, 100))

        result = self.consulta(query)
        if result is None:
            return None
        return result[0][0]

    def db_max_customerid(self):
        """
        Función que calcula el valor máximo de customerid
        (ya que el nextval de la db no parece funcionar)
        :return: el customerid máximo encontrado en la DB
        """

        result = self.consulta("SELECT MAX(customerid) "
                               "FROM customers")

        return result[0][0]

    def db_get_genres(self):
        """
        Función que obtiene todas las categorías de películas
        :return: una lista con todas las categorías de películas de la DB
        """
        result = self.consulta("SELECT genrename "
                               "FROM genres")

        categorias = []
        for record in result:
            categorias.append(record[0])

        return categorias

    def db_get_order(self, customerid):
        """
        Obtiene el pedido activo del customer o returnea None en caso de que
        este no exista.
        :param customerid: id del customer
        :return: la id del pedido activo o None si no existe
        """
        result = self.consulta("SELECT orderid "
                               "FROM orders "
                               "WHERE customerid = {} and status IS NULL"
                               "".format(customerid))

        if result is None:
            return None
        else:
            return result[0][0]

    def db_create_order(self, customerid):
        """
        Crea un nuevo pedido activo para el usuario
        :param customerid: id del customer al que crear el pedido
        :return: id del pedido creado
        """
        orderid = self.db_max_orderid() + 1
        query = "INSERT INTO public.orders (orderid, orderdate, customerid, " \
                "netamount, tax, totalamount, status) " \
                "VALUES ({}, NOW(), {}, 0, 15, 0, NULL)" \
                "".format(orderid, customerid)
        self.consulta(query)

        return orderid

    def db_max_orderid(self):
        """
        Busca el orderid máxima de la tabla orders
        :result: el máximo id de la tabla orders
        """
        result = self.consulta("SELECT MAX(orderid) "
                               "FROM orders")

        return result[0][0]

    def db_order_add_product(self, orderid, movie):
        """
        Función que añade el producto al pedido en orderdetails.
        Se encarga de incrementar la cantidad o crear un nuevo record
        dependiendo de si el pedido ya contiene el producto o no.
        :param orderid: id del pedido
        :param movie: pelicula que se añadirá al pedido
        :return: 0 si funciona bien, 1 si no
        """
        # Obtener la cantidad del producto (si existe)
        result = self.consulta("SELECT quantity "
                               "FROM orderdetail "
                               "WHERE orderid = {} and prod_id = {}"
                               "".format(orderid, movie['producto']))

        if result is None:
            quantity = None
        else:
            quantity = result[0][0]

        # Obtener el stock actual del producto (para ver si la compra se puede
        # realizar o no)
        result = self.consulta("SELECT stock "
                               "FROM inventory "
                               "WHERE prod_id = {}".format(movie['producto']))
        if result is None:
            return 1
        else:
            stock = result[0][0]

        if quantity is None:
            # Si no existe la pareja orderid, prod_id se debe insertar
            if stock < 1:
                return 1
            self.consulta("INSERT INTO public.orderdetail "
                          "(orderid, prod_id, price, quantity) "
                          "VALUES ({}, {}, {}, 1)"
                          "".format(orderid, movie['producto'],
                                    movie['precio']))
        else:
            # Si ya existe la pareja, se incrementa en 1 la cantidad
            # (siempre que haya suficiente stock)
            if stock < quantity + 1:
                return 1

            # Esta consulta se realiza de esta forma por si por algún motivo
            # está repetida la pareja orderid, prod_id
            self.consulta("UPDATE public.orderdetail "
                          "SET quantity = {}, price = {} "
                          "WHERE CTID IN "
                          "( SELECT CTID "
                          "FROM orderdetail "
                          "WHERE orderid = {} and "
                          "prod_id = {} and "
                          "quantity = {} "
                          "LIMIT 1)"
                          "".format(quantity + 1,
                                    movie['precio'] * (quantity + 1),
                                    orderid, movie['producto'], quantity))

        return 0

    def db_order_remove_product(self, orderid, movie):
        """
        Función que quita el producto al pedido en orderdetails.
        Se encarga de reducir la cantidad o eliminar el record dependiendo
        de si el pedido ya contiene el producto o no.
        :param orderid: id del pedido
        :param movie: pelicula de la que reducir la cantidad
        :return: None
        """
        # Obtener la cantidad del producto
        result = self.consulta("SELECT quantity "
                               "FROM orderdetail "
                               "WHERE orderid = {} and prod_id = {}"
                               "".format(orderid, movie['producto']))

        if result is None:
            return
        else:
            quantity = result[0][0]

        if quantity == 1:
            # Si la cantidad solo es 1 se eliminará el record de la tabla
            self.consulta("DELETE FROM public.orderdetail "
                          "WHERE CTID IN "
                          "( SELECT CTID "
                          "FROM orderdetail "
                          "WHERE orderid = {} and "
                          "prod_id = {} and "
                          "quantity = {} "
                          "LIMIT 1)".format(orderid, movie['producto'],
                                            quantity))
        else:
            # Se reduce en 1 la cantidad
            self.consulta("UPDATE public.orderdetail "
                          "SET quantity = {}, price = {} "
                          "WHERE CTID IN "
                          "( SELECT CTID "
                          "FROM orderdetail "
                          "WHERE orderid = {} and "
                          "prod_id = {} and "
                          "quantity = {} "
                          "LIMIT 1)"
                          "".format(quantity - 1,
                                    movie['precio'] * (quantity - 1),
                                    orderid, movie['producto'], quantity))

    def db_get_order_price(self, orderid):
        """
        Función que te devuelve el precio de un pedido (totalamount)
        :param orderid: id del pedido
        :return: el precio del pedido, None si no existe
        """
        result = self.consulta("SELECT totalamount "
                               "FROM orders "
                               "WHERE orderid = {}".format(orderid))

        if result is None:
            return None

        price = result[0][0]
        return float(price)

    def db_get_order_products(self, orderid):
        """
        Función que obtiene los productos y cantidades que forman
        parte de un pedido
        :param orderid: id del pedido
        :return: lista con elementos (prod_id, quantity)
        """
        result = self.consulta("SELECT prod_id, quantity "
                               "FROM orderdetail "
                               "WHERE orderid = {}".format(orderid))
        return result

    def db_order_pay(self, orderid, totalamount, customerid, saldo):
        """
        Función que pasa un pedido al estado: 'Paid' y actualiza el saldo del
        customer tras esto.
        :param orderid: id del pedido
        :param totalamount: precio del pedido (se pasa por argumento para
                            evitar una consulta extra)
        :param customerid: id del usuario
        :param saldo: saldo actual del usuario (de nuevo, evita consulta extra)
        """
        # Cambiar a pagado el status
        self.consulta("UPDATE public.orders "
                      "SET status = 'Paid' "
                      "WHERE orderid = {}".format(orderid))

        # Actualizar saldo del customer
        self.db_update_saldo(customerid, saldo - totalamount)

    def db_update_saldo(self, customerid, new_saldo):
        """
        Actualiza el saldo de un customer
        :param customerid: id del usuario
        :param new_saldo: saldo nuevo que se le debe asignar al usuario
        """
        self.consulta("UPDATE public.customers "
                      "SET saldo = {} "
                      "WHERE customerid = {}".format(new_saldo, customerid))

    def db_order_empty(self, orderid):
        """
        Vacia el carro activo de un customer
        :param orderid: pedido que se debe vaciar
        """
        self.consulta("DELETE FROM public.orderdetail "
                      "WHERE orderid = {}".format(orderid))

    def db_get_history(self, customerid):
        """
        Función que obtiene el historial de un determinado usuario
        :param customerid: id del usuario
        :return: diccionario con el historial
        """
        historial = []
        # Se obtienen todos los pedidos del usuario
        result = self.consulta("SELECT orderid, orderdate, totalamount "
                               "FROM orders "
                               "WHERE customerid = {} and status IS NOT NULL "
                               "ORDER BY orderdate".format(customerid))
        if result is None:
            return []
        orders = result
        # Por cada pedido se obtiene la información
        for orderid, fecha, precio in orders:
            # Se guarda la id, fecha y precio del pedido
            pedido = {'id': orderid,
                      'fecha': fecha.strftime('%d/%m/%Y'),
                      'precio': float(precio),
                      'peliculas': []}

            # Se obtienen el titulo, precio y cantidad de cada producto
            result = self.consulta(
                "SELECT movietitle, orderdetail.price, quantity "
                "FROM (products "
                "NATURAL JOIN imdb_movies) as A "
                "JOIN orderdetail ON orderdetail.prod_id = A.prod_id "
                "WHERE orderid = {}".format(orderid))

            for item in result:
                pedido['peliculas'].append(item)

            # Se añade el pedido a la lista de pedidos
            historial.append(pedido)

        return historial
