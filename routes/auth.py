from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from forms.loginForm import LoginForm
from utils.bcryptService import bcrypt
from models.usuarios import User

auth = Blueprint("auth", __name__)
 
@auth.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        currentUser = User.query.filter_by(username=username).first()
        if currentUser:
            if bcrypt.check_password_hash(currentUser.password, password):
                if currentUser.rank == "admin":
                    login_user(currentUser)
                    return redirect(url_for("admin.dashboard"))
                else:
                    login_user(currentUser)
                    return redirect(url_for("usuarios.home"))
    return render_template("login.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))