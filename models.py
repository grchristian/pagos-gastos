# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Gasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    pago_id = db.Column(db.Integer, db.ForeignKey('pago.id'))
    pago_generado = db.Column(db.Boolean, default=False)


class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    cuenta_bancaria_id = db.Column(
        db.Integer, db.ForeignKey('cuenta_bancaria.id'))
    gastos = db.relationship('Gasto', backref='pago', lazy=True)


class CuentaBancaria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_banco = db.Column(db.String(80), nullable=False)
    numero_cuenta = db.Column(db.String(80), nullable=False)
    saldo = db.Column(db.Float, nullable=False)
    pagos = db.relationship('Pago', backref='cuenta_bancaria', lazy=True)
