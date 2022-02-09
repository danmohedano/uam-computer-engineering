# -*- coding: utf-8 -*-

import os
import sys, traceback, time

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/simongo",
                          echo=False, execution_options={"autocommit": False})


def dbConnect():
    return db_engine.connect()


def dbCloseConnect(db_conn):
    db_conn.close()


def getListaCliMes(db_conn, mes, anio, iumbral, iintervalo, use_prepare,
                   break0, niter):
    # TODO: implementar la consulta; asignar nombre 'cc' al contador resultante
    consulta = " ... "

    # TODO: ejecutar la consulta 
    # - mediante PREPARE, EXECUTE, DEALLOCATE si use_prepare es True
    # - mediante db_conn.execute() si es False

    # Array con resultados de la consulta para cada umbral
    dbr = []

    for ii in range(niter):
        # TODO: ...

        # Guardar resultado de la query
        dbr.append({"umbral": iumbral, "contador": res['cc']})

        # TODO: si break0 es True, salir si contador resultante es cero

        # Actualizacion de umbral
        iumbral = iumbral + iintervalo

    return dbr


def getMovies(anio):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query = "select movietitle from imdb_movies where year = '" + anio + "'"
    resultproxy = db_conn.execute(query)

    a = []
    for rowproxy in resultproxy:
        d = {}
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for tup in rowproxy.items():
            # build up the dictionary
            d[tup[0]] = tup[1]
        a.append(d)

    resultproxy.close()

    db_conn.close()

    return a


def getCustomer(username, password):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query = "select * from customers where username='" + username + "' and password='" + password + "'"
    res = db_conn.execute(query).first()

    db_conn.close()

    if res is None:
        return None
    else:
        return {'firstname': res['firstname'], 'lastname': res['lastname']}


def delCustomer(customerid, bFallo, bSQL, duerme, bCommit):
    # Array de trazas a mostrar en la página
    dbr = []

    # Mensajes
    orderdetail_ini = "Iniciando borrado en tabla 'orderdetail'"
    orderdetail_end = "Finalizado borrado en tabla 'orderdetail'"
    orders_ini = "Iniciando borrado en tabla 'orders'"
    orders_end = "Finalizado borrado en tabla 'orders'"
    customers_ini = "Iniciando borrado en tabla 'customers'"
    customers_end = "Finalizado borrado en tabla 'customers'"
    error_ini = "Error encontrado, iniciando rollback"
    error_end = "Rollback realizado"
    ok_ini = "Todo correcto, realizando commit"
    ok_end = "Commit realizado"
    commit_intermedio = "Realizado commit intermedio"
    non_exist = "Customer no existe"

    q1 = "DELETE FROM orderdetail USING orders " + \
         "WHERE orderdetail.orderid = orders.orderid AND " + \
         "orders.customerid = {};".format(customerid)

    q2 = "DELETE FROM orders " + \
         "WHERE customerid = {};".format(customerid)

    q3 = "DELETE FROM customers " + \
         "WHERE customerid = {};".format(customerid)

    transaction = None

    try:
        # Conexion a la base de datos
        db_conn = db_engine.connect()

        # Comprobar que existe el customerid
        res = db_conn.execute(
            "SELECT * FROM customers WHERE customerid = {}".format(
                customerid)).first()
        if not res:
            dbr.append(non_exist)
            return dbr

        if bSQL:
            db_conn.execute("BEGIN;")
        else:
            transaction = db_conn.begin()

        dbr.append(orderdetail_ini)
        db_conn.execute(q1)
        dbr.append(orderdetail_end)

        if bCommit:
            # Se realiza un commit intermedio
            if bSQL:
                db_conn.execute("COMMIT;")
                dbr.append(commit_intermedio)
                db_conn.execute("BEGIN;")
            else:
                transaction.commit()
                dbr.append(commit_intermedio)
                transaction = db_conn.begin()

        if bFallo:
            dbr.append(customers_ini)
            db_conn.execute(q3)
            dbr.append(customers_end)
            dbr.append(orders_ini)
            db_conn.execute(q2)
            dbr.append(orders_end)
        else:
            dbr.append("Durmiendo")
            db_conn.execute("SELECT pg_sleep({});".format(duerme))
            dbr.append(orders_ini)
            db_conn.execute(q2)
            dbr.append(orders_end)
            dbr.append(customers_ini)
            db_conn.execute(q3)
            dbr.append(customers_end)

    except OperationalError as e:
        print(e)
        if bSQL:
            db_conn.execute("ROLLBACK;")
        else:
            transaction.rollback()
        dbr.append("Deadlock detectado")

    except Exception as e:
        print(e)
        dbr.append(error_ini)
        if bSQL:
            db_conn.execute("ROLLBACK;")
        else:
            transaction.rollback()

        dbr.append(error_end)
    else:
        dbr.append(ok_ini)
        if bSQL:
            db_conn.execute("COMMIT;")
        else:
            transaction.commit()
        dbr.append(ok_end)

    db_conn.close()
    return dbr
