from app import app, db
from flask_migrate import upgrade as _upgrade
from models import Gasto, Pago, CuentaBancaria
from datetime import datetime

with app.app_context():
    # Inicializar y Migrar la Base de Datos
    _upgrade()

    # Borrar datos existentes
    db.session.query(Gasto).delete()
    db.session.query(Pago).delete()
    db.session.query(CuentaBancaria).delete()
    db.session.commit()

    # Crear instancias de CuentaBancaria
    cuenta1 = CuentaBancaria(
        nombre_banco='Deutsche Bank AG', numero_cuenta='78236192', saldo=30000)
    cuenta2 = CuentaBancaria(
        nombre_banco='Mizuho Bank Ltd', numero_cuenta='18650231', saldo=10000)
    cuenta3 = CuentaBancaria(
        nombre_banco='Wells Fargo', numero_cuenta='41890242', saldo=500)

    # Agregar cuentas a la sesión de la base de datos
    db.session.add(cuenta1)
    db.session.add(cuenta2)
    db.session.add(cuenta3)

    # Crear instancias de Gasto
    gasto1 = Gasto(descripcion='Rentas de oficina', monto=5900,
                   estado='pendiente', pago_id=None, pago_generado=False)
    gasto2 = Gasto(descripcion='Factura de electricidad', monto=3500,
                   estado='pendiente', pago_id=None, pago_generado=False)
    gasto3 = Gasto(descripcion='Servicio de internet', monto=2000,
                   estado='pendiente', pago_id=None, pago_generado=False)
    gasto4 = Gasto(descripcion='Licencias de software', monto=1700,
                   estado='pendiente', pago_id=None, pago_generado=False)
    gasto5 = Gasto(descripcion='Material de papelería', monto=5400,
                   estado='pendiente', pago_id=None, pago_generado=False)
    gasto6 = Gasto(descripcion='Gastos de limpieza', monto=3400,
                   estado='pendiente', pago_id=None, pago_generado=False)
    gasto7 = Gasto(descripcion='Mantenimiento de equipos', monto=2800,
                   estado='pendiente', pago_id=None, pago_generado=False)
    gasto8 = Gasto(descripcion='Seguro de responsabilidad civil', monto=4100,
                   estado='pendiente', pago_id=None, pago_generado=False)
    gasto9 = Gasto(descripcion='Gastos de transporte público', monto=2600,
                   estado='pendiente', pago_id=None, pago_generado=False)
    gasto10 = Gasto(descripcion='Hosting de sitio web', monto=3600,
                    estado='pendiente', pago_id=None, pago_generado=False)
    gasto11 = Gasto(descripcion='Servicios de contabilidad externa', monto=1950,
                    estado='pendiente', pago_id=None, pago_generado=False)
    gasto12 = Gasto(descripcion='Gastos de envío y mensajería', monto=2450,
                    estado='pendiente', pago_id=None, pago_generado=False)
    gasto13 = Gasto(descripcion='Asesoría legal', monto=4450,
                    estado='pendiente', pago_id=None, pago_generado=False)
    gasto14 = Gasto(descripcion='Honorarios por consultoría de marketing', monto=3400,
                    estado='pendiente', pago_id=None, pago_generado=False)
    db.session.add(gasto1)
    db.session.add(gasto2)
    db.session.add(gasto3)
    db.session.add(gasto4)
    db.session.add(gasto5)
    db.session.add(gasto6)
    db.session.add(gasto7)
    db.session.add(gasto8)
    db.session.add(gasto9)
    db.session.add(gasto10)
    db.session.add(gasto11)
    db.session.add(gasto12)
    db.session.add(gasto13)
    db.session.add(gasto14)

    # Guardar los cambios en la base de datos
    db.session.commit()

    print("La base de datos ha sido inicializada y poblada con datos de muestra.")
