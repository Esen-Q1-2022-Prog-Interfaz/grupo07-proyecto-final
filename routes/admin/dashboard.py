from flask import Blueprint, render_template, redirect, url_for
from models.usuarios import User
from utils.db import db
from models.salasreservas import ReservaSalas
from forms.adminSalaReservaFormCalendar import ReservaSalaFormAdminC
from flask_login import login_required, current_user

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/")
@login_required
def dashboard():
    if current_user.rank == "admin":
        return render_template("admin/dashboard.html")
    else:
        return render_template("error.html")

@admin.route("/calendar/")
@login_required
def calendario():
    if current_user.rank == "admin":        
        return render_template("user/calendario.html")
    else:
        return render_template("error.html")

@admin.route("/calendar/dayview/<month>/<day>/<year>", methods=["GET", "POST"])
@login_required
def dayview(month, day, year): 
    if current_user.rank == "admin":
        if len(str(day)) ==1:
            day = str(0)+str(day)
        if len(str(month)) == 1:
            month = str(0)+str(month)
        fecha = str(year) + "-" + str(month) + "-" + str(day) 
        reservasLista = ReservaSalas.query.filter_by(fecha=fecha)
        form = ReservaSalaFormAdminC()
        if form.validate_on_submit():
            solicitante = form.solicitante.data
            idSala = form.idSala.data
            horaInicio = form.horaInicio.data
            horaFinal = form.horaFinal.data
            registro = ReservaSalas(solicitante, idSala, fecha, horaInicio, horaFinal)
            db.session.add(registro)
            db.session.commit()
            return redirect(url_for('admin.dayview', month = month, day = day, year = year))
        return render_template("admin/dayview.html", day = day, month = month, year = year, form = form, items = reservasLista)
    else:
        return render_template("error.html")

