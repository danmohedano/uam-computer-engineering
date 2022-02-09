#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from app import database
from flask import render_template, request, url_for
import os
import sys
import time

@app.route('/borraCliente', methods=['POST','GET'])
def borraCliente():
    if 'customerid' in request.args:
        customerid = request.args["customerid"]
        bSQL       = request.args["txnSQL"]
        bCommit = "bCommit" in request.args
        bFallo  = "bFallo"  in request.args
        duerme  = request.args["duerme"]
        dbr = database.delCustomer(customerid, bFallo, bSQL=='1', int(duerme), bCommit)
        return render_template('borraCliente.html', dbr=dbr)
    else:
        return render_template('borraCliente.html')

    
@app.route('/listaClientesMes', methods=['GET', 'POST'])
def listaClientesMes():
    if 'fecha' in request.form:
        fecha  = request.form['fecha']
        mes    = request.form['mes']
        anio   = request.form['anio']
        umbral = request.form['minimo']
        intervalo = request.form['intervalo']
        use_prepare = 'prepare'  in request.form
        break0 = 'break0' in request.form
        niter  = request.form['iter']
        # connect fuera para comparar tiempos con más precisión
        db_conn = database.dbConnect()
        t0=round(time.time() * 1000)
        dbr = database.getListaCliMes(db_conn, mes, anio, int(umbral), int(intervalo), use_prepare, break0, int(niter))
        t1=round(time.time() * 1000)
        database.dbCloseConnect(db_conn)

        return render_template('listaClientesMes.html',
            fecha = fecha,
            mes   = mes,
            anio  = anio,
            umbral = int(umbral),
            intervalo = int(intervalo),
            use_prepare = use_prepare,
            break0 = break0,
            tiempo = str(int(t1-t0)),
            dbr=dbr
           )
    else:
        return render_template('listaClientesMes.html')
