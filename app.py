# app.py

from collections import Counter
from models import Gasto
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from models import db, Gasto, Pago, CuentaBancaria
from datetime import datetime
from flask_migrate import Migrate
from collections import defaultdict
from datetime import datetime
from sqlalchemy import func, extract
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
app.secret_key = 'helloworld'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///empresa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gasto/nuevo', methods=['POST'])
def nuevo_gasto():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        monto = float(request.form['monto'])
        nuevo_gasto = Gasto(descripcion=descripcion,
                            monto=monto, estado='pendiente')
        db.session.add(nuevo_gasto)
        db.session.commit()
        return redirect(url_for('ver_gastos'))


@app.route('/gastos')
def ver_gastos():
    gastos = Gasto.query.all()
    return render_template('gastos.html', gastos=gastos)


@app.route('/gasto/aprobar/<int:id>')
def aprobar_gasto(id):
    gasto = Gasto.query.get(id)
    if gasto:
        gasto.estado = 'aprobado'
        db.session.commit()
    return redirect(url_for('ver_gastos'))


@app.route('/gasto/cancelar/<int:id>')
def cancelar_gasto(id):
    gasto = Gasto.query.get(id)
    if gasto:
        gasto.estado = 'cancelado'
        db.session.commit()
    return redirect(url_for('ver_gastos'))


@app.route('/pagos')
def ver_pagos():
    pagos = Pago.query.all()
    return render_template('pagos.html', pagos=pagos)

# Ruta para registrar un nuevo pago


@app.route('/pago/nuevo/<int:gasto_id>', methods=['POST'])
def nuevo_pago(gasto_id):
    gasto = Gasto.query.get(gasto_id)
    if gasto and gasto.estado == 'aprobado':
        nuevo_pago = Pago(monto=gasto.monto, fecha=datetime.now(
        ), estado='pendiente', cuenta_bancaria_id=1)
        db.session.add(nuevo_pago)
        db.session.commit()
    return redirect(url_for('ver_pagos'))

# Ruta para aprobar un pago


# Ruta para aprobar un pago
@app.route('/pago/aprobar/<int:id>')
def aprobar_pago(id):
    pago = Pago.query.get(id)
    if pago:
        pago.estado = 'aprobado'
        db.session.commit()
    return redirect(url_for('ver_pagos'))

# Ruta para cancelar un pago


@app.route('/pago/cancelar/<int:id>')
def cancelar_pago(id):
    pago = Pago.query.get(id)
    if pago:
        pago.estado = 'cancelado'
        db.session.commit()
    return redirect(url_for('ver_pagos'))


@app.route('/pago/generar/<int:gasto_id>', methods=['GET', 'POST'])
def generar_pago(gasto_id):
    gasto = Gasto.query.get(gasto_id)
    if gasto and gasto.estado == 'aprobado' and not gasto.pago_generado:
        nuevo_pago = Pago(monto=gasto.monto, fecha=datetime.now(),
                          estado='pendiente', cuenta_bancaria_id=1)
        db.session.add(nuevo_pago)
        gasto.pago_generado = True
        db.session.commit()
    return redirect(url_for('ver_pagos'))


@app.route('/pago/efectuar/<int:pago_id>')
def efectuar_pago(pago_id):
    pago = Pago.query.get(pago_id)
    cuentas = CuentaBancaria.query.all()
    if not pago or pago.estado != 'aprobado':
        return redirect(url_for('ver_pagos'))
    return render_template('efectuar_pago.html', pago=pago, cuentas=cuentas)


# Ruta para procesar y efectuar un pago
@app.route('/pago/procesar/<int:pago_id>', methods=['POST'])
def procesar_pago(pago_id):
    pago = Pago.query.get(pago_id)
    cuenta_id = request.form.get('cuenta_id')
    cuenta = CuentaBancaria.query.get(cuenta_id)

    if pago and cuenta and pago.estado == 'aprobado':
        if cuenta.saldo >= pago.monto:
            cuenta.saldo -= pago.monto
            pago.estado = 'efectuado'
            pago.cuenta_bancaria_id = cuenta.id
            db.session.commit()
            flash('Pago efectuado exitosamente', 'success')
            return redirect(url_for('ver_pagos'))
        else:
            flash('Fondos insuficientes en la cuenta seleccionada', 'danger')
            return redirect(url_for('efectuar_pago', pago_id=pago.id))

    return redirect(url_for('ver_pagos'))


@app.route('/cuentas')
def ver_cuentas():
    cuentas = CuentaBancaria.query.all()
    return render_template('cuentas.html', cuentas=cuentas)

@app.route('/cuenta/<int:cuenta_id>')
def detalles_cuenta(cuenta_id):
    cuenta = CuentaBancaria.query.get_or_404(cuenta_id)
    # Filtrar pagos que están en estado 'efectuado'
    pagos = Pago.query.filter_by(cuenta_bancaria_id=cuenta_id, estado='efectuado').all()
    return render_template('detalle_cuenta.html', cuenta=cuenta, pagos=pagos)

# Dashboard


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/api/gastos-estatus')
def gastos_estatus_data():
    gastos_estatus = Counter(gasto.estado for gasto in Gasto.query.all())
    return jsonify(dict(gastos_estatus))


@app.route('/api/gastos-montos')
def gastos_montos_data():
    nombres_gastos = [gasto.descripcion for gasto in Gasto.query.all()]
    montos_gastos = [gasto.monto for gasto in Gasto.query.all()]
    return jsonify({'nombres_gastos': nombres_gastos, 'montos_gastos': montos_gastos})


@app.route('/api/pagos-estatus')
def pagos_estatus_data():
    pagos_estatus = Counter(pago.estado for pago in Pago.query.all())
    return jsonify(dict(pagos_estatus))


@app.route('/api/pagos-totales')
def pagos_totales_data():
    datos = db.session.query(
        CuentaBancaria.nombre_banco.label('cuenta'),
        func.strftime('%Y-%m-%d', Pago.fecha).label('dia'),
        func.sum(Pago.monto).label('total')
    ).join(CuentaBancaria).group_by(CuentaBancaria.nombre_banco, 'dia').order_by('dia').all()

    # Preparar los datos para el frontend
    resultados = {}
    for cuenta, dia, total in datos:
        if cuenta not in resultados:
            resultados[cuenta] = {'fechas': [], 'totales': []}
        resultados[cuenta]['fechas'].append(dia)
        resultados[cuenta]['totales'].append(total)

    return jsonify(resultados)


@app.route('/api/cuentas-disponibilidad')
def cuentas_disponibilidad_data():
    cuentas = CuentaBancaria.query.all()
    datos = [{'nombre': cuenta.nombre_banco, 'disponible': cuenta.saldo}
             for cuenta in cuentas]
    return jsonify(datos)


@app.route('/api/pagos-estadisticas')
def pagos_estadisticas_data():
    datos = db.session.query(
        extract('month', Pago.fecha).label('mes'),
        func.sum(Pago.monto).label('total'),
        func.avg(Pago.monto).label('promedio')
    ).group_by('mes').order_by('mes').all()

    meses = [d[0] for d in datos]
    totales = [d[1] for d in datos]
    promedios = [d[2] for d in datos]

    return jsonify({'meses': meses, 'totales': totales, 'promedios': promedios})


@app.route('/api/gastos-por-cuenta')
def gastos_por_cuenta_data():
    datos = db.session.query(
        CuentaBancaria.nombre_banco.label('cuenta'),
        extract('month', Pago.fecha).label('mes'),
        func.sum(Pago.monto).label('total')
    ).join(Pago).group_by(CuentaBancaria.nombre_banco, 'mes').order_by('mes').all()

    resultados = {}
    for cuenta, mes, total in datos:
        if cuenta not in resultados:
            resultados[cuenta] = {'meses': [], 'totales': [], 'tendencia': []}
        resultados[cuenta]['meses'].append(mes)
        resultados[cuenta]['totales'].append(total)

        # Calcular la línea de tendencia
        if len(resultados[cuenta]['meses']) > 1:
            x = np.array(resultados[cuenta]['meses']).reshape(-1, 1)
            y = np.array(resultados[cuenta]['totales'])
            modelo = LinearRegression().fit(x, y)
            tendencia = modelo.predict(x)
            resultados[cuenta]['tendencia'] = tendencia.tolist()

    return jsonify(resultados)


if __name__ == '__main__':
    app.run(debug=True)
