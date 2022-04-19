from flask import Blueprint, redirect, render_template, url_for
from models.usuarios import User
from utils.db import db
from models.salasreservas import ReservaSalas
from forms.adminSalaReservaForm import ReservaSalaFormAdmin
from flask_login import login_required, current_user

solicitudes = Blueprint("solicitudes", __name__, url_prefix="/admin/solicitudes")


@solicitudes.route("/", methods=["GET", "POST"])
@login_required
def vista():
    if current_user.rank == "admin":
        form = ReservaSalaFormAdmin()
        reservasLista = ReservaSalas.query.all()
        if form.validate_on_submit():
            solicitante = form.solicitante.data
            idSala = form.idSala.data
            fecha = form.fecha.data
            horaInicio = form.horaInicio.data
            horaFinal = form.horaFinal.data
            registro = ReservaSalas(solicitante, idSala, fecha, horaInicio, horaFinal)
            db.session.add(registro)
            db.session.commit()
            return redirect(url_for('solicitudes.vista'))
        return render_template("admin/solicitudes.html", form = form, items = reservasLista)
    else:
        return render_template("error.html")

@solicitudes.route("/update/<int:id>")
def update(id):
    return f'modificar solicitud, {id}'

@solicitudes.route('/aprobar/<id>', methods = ["GET", "POST"])
def aprobar(id):
    solicitudActual = ReservaSalas.query.get(id)
    solicitudActual.estado = 'Aprobado'
    db.session.add(solicitudActual)
    db.session.commit()
    return redirect(url_for('mailCambiarEstado', newstatus = 'aprobado',id =id))

@solicitudes.route('/rechazar/<id>', methods = ["GET", "POST"])
def rechazar(id):
    solicitudActual = ReservaSalas.query.get(id)
    solicitudActual.estado = 'Rechazado'
    db.session.add(solicitudActual)
    db.session.commit()
    return redirect(url_for('mailCambiarEstado', newstatus = 'rechazado', id = id))

@solicitudes.route("/solicitudesusuario/<string:solicitante>", methods=["GET", "POST"])
@login_required
def vistaPorUser(solicitante):
    reservasLista = ReservaSalas.query.filter_by(solicitante=solicitante)
    return render_template("admin/solicitudesporuser.html", items = reservasLista)

@solicitudes.route("/imprimesolicitud/<int:id>", methods=["GET", "POST"])
def printSolicitud(id):
    solicitud = ReservaSalas.query.get(id)
    print(solicitud)
    return render_template("admin/printSolicitud.html", item = solicitud)