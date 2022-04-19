from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from forms.CreateUserForm import createUserForm
from utils.db import db
from utils.bcryptService import bcrypt
from models.usuarios import User
from flask_login import login_required, current_user


users = Blueprint("users", __name__, url_prefix="/admin/usuarios")


@users.route("/", methods=["POST", "GET"])
@login_required
def home():
    if current_user.rank == "admin":
        userList = User.query.all()
        form = createUserForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            email = form.email.data 
            rank = form.rank.data
            hashed_passsword = bcrypt.generate_password_hash(password)
            newUser = User(username, hashed_passsword, email, rank)
            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for("users.home"))
        return render_template("admin/usuarios.html", items = userList, form = form)
    else:
        return render_template("error.html")


@users.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):
    currentUser = User.query.get(id)
    form = createUserForm(
        username = currentUser.username,
        password = currentUser.password,
        email = currentUser.email,
        rank = currentUser.rank,
    )
    if form.validate_on_submit():
        currentUser.username = form.username.data
        hashed_passsword = bcrypt.generate_password_hash(form.password.data)
        currentUser.password = hashed_passsword
        currentUser.email = form.email.data
        currentUser.rank = form.rank.data
        db.session.add(currentUser)
        db.session.commit()
        return redirect(url_for("users.home"))
    return render_template("admin/updateusuario.html", form=form, id=id)


@users.route("/delete/<int:id>")
def delete(id):
    currentUser = User.query.get(id)
    db.session.delete(currentUser)
    db.session.commit()
    return redirect(url_for("users.home"))


