# app.py

from collections import Counter
from models import Gasto
from flask import Flask, flash, request, redirect, url_for, render_template
from models import db, Gasto, Pago, CuentaBancaria
from datetime import datetime
from flask_migrate import Migrate
from collections import defaultdict
from datetime import datetime

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
            return redirect(url_for('ver_pagos'))
        else:
            flash('Fondos insuficientes en la cuenta seleccionada',
                  'danger')  # Mensaje flash con categoría 'danger'
            return redirect(url_for('efectuar_pago', pago_id=pago.id))

    return redirect(url_for('ver_pagos'))


@app.route('/cuentas')
def ver_cuentas():
    cuentas = CuentaBancaria.query.all()
    return render_template('cuentas.html', cuentas=cuentas)


@app.route('/cuenta/<int:cuenta_id>')
def detalles_cuenta(cuenta_id):
    cuenta = CuentaBancaria.query.get_or_404(cuenta_id)
    pagos = Pago.query.filter_by(cuenta_bancaria_id=cuenta_id).all()
    return render_template('detalle_cuenta.html', cuenta=cuenta, pagos=pagos)

# Dashboard
@app.route('/dashboard')
def dashboard():
    # gastos-grafico-1: grafica de barras de gastos por estatus
    gastos_estatus = Counter(gasto.estado for gasto in Gasto.query.all())
    # gastos-grafico-2: grafica con nombres de los gastos en el eje x y montos en el eje
    nombres_gastos = [gasto.descripcion for gasto in Gasto.query.all()]
    montos_gastos = [gasto.monto for gasto in Gasto.query.all()]

    # TODO:
    # pagos-grafico-1: histograma de pagos a lo largo del tiempo
    # pagos-grafico-2:
    # cuentas-grafico-1:
    # cuentas-grafico-2:

    return render_template('dashboard.html', gastos_estatus=gastos_estatus, gastos=Gasto.query.all(), nombres_gastos=nombres_gastos, montos_gastos=montos_gastos)


if __name__ == '__main__':
    app.run(debug=True)
