from app import app, db
from flask_migrate import upgrade as _upgrade
from models import Gasto, Pago, CuentaBancaria
from datetime import datetime

with app.app_context():
    # Inicializar y Migrar la Base de Datos
    _upgrade()

    # Crear instancias de CuentaBancaria
    cuenta1 = CuentaBancaria(
        nombre_banco='Deutsche Bank AG', numero_cuenta='78236192', saldo=50000)
    cuenta2 = CuentaBancaria(
        nombre_banco='Mizuho Bank Ltd', numero_cuenta='18650231', saldo=25000)

    # Agregar cuentas a la sesión de la base de datos
    db.session.add(cuenta1)
    db.session.add(cuenta2)

    # Crear instancias de Pago
    pago1 = Pago(monto=2000, fecha=datetime(2023, 7, 1, 10, 0, 0),
                 estado='pendiente', cuenta_bancaria_id=cuenta1.id)
    pago2 = Pago(monto=3500, fecha=datetime(2023, 7, 2, 11, 0, 0),
                 estado='aprobado', cuenta_bancaria_id=cuenta2.id)

    # Agregar pagos a la sesión de la base de datos
    db.session.add(pago1)
    db.session.add(pago2)

    # Crear instancias de Gasto
    gasto1 = Gasto(descripcion='Material de oficina', monto=2000,
                   estado='pendiente', pago_id=None, pago_generado=False)
    gasto2 = Gasto(descripcion='Servicios de internet', monto=3500,
                   estado='aprobado', pago_id=pago1.id, pago_generado=True)

    # Agregar gastos a la sesión de la base de datos
    db.session.add(gasto1)
    db.session.add(gasto2)

    # Guardar los cambios en la base de datos
    db.session.commit()

    print("La base de datos ha sido inicializada y poblada con datos de muestra.")
