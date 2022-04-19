from flask import Blueprint, render_template, redirect, url_for, Flask
from utils.db import db
from flask_login import login_required
from models.salasreservas import ReservaSalas
from forms.SalaReservaForm import ReservaSalaForm

usuarios = Blueprint("usuarios", __name__, url_prefix="/usuarios")

@usuarios.route("/")
@login_required
def home():
    return render_template("user/dashboard.html")