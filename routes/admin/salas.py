from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from forms.CrearSalaForm import CrearSalasForm
from utils.db import db
from utils.bcryptService import bcrypt
from models.salas import Sala
from flask_login import login_required, current_user


salas = Blueprint("salas", __name__, url_prefix="/admin/salas")


@salas.route("/", methods=["POST", "GET"])
@login_required
def home():
    if current_user.rank == "admin":
        form = CrearSalasForm()
        if form.validate_on_submit():
            sala = form.sala.data
            nuevaSala = Sala(sala)
            db.session.add(nuevaSala)
            db.session.commit()
            return redirect(url_for("salas.home"))
        salasLista = Sala.query.all()
        return render_template("admin/salasexistentes.html", items = salasLista, form = form)
    else:
        return render_template("error.html")

@salas.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    currentSala = Sala.query.get(id)
    form = CrearSalasForm(
        sala = currentSala.sala
    )
    if form.validate_on_submit():
        currentSala.sala = form.sala.data
        db.session.add(currentSala)
        db.session.commit()
        return redirect(url_for("salas.home"))
    return """render_template("admin/updatesala.html", form=form, id=id)"""
    


@salas.route("/delete/<int:id>")
def delete(id):
    if current_user.rank == "admin":
        currentSala = Sala.query.get(id)
        db.session.delete(currentSala)
        db.session.commit()
        return redirect(url_for("salas.home"))
    else:
        return render_template("error.html")
