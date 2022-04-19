import email
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from models.usuarios import User
from wtforms.fields import EmailField

class createUserForm(FlaskForm):
    username = StringField( "Nombre de usuario",
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "usuario"},
    )

    password = PasswordField( "Contraseña",
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "contraseña"},
    )

    email = EmailField( "Email",
        validators=[InputRequired(), Length(min=5, max=100), Email()],
        render_kw={"placeholder": "email"},
    )

    rank = StringField( "Rango", 
        validators=[InputRequired(), Length(min=1, max=100)],
        render_kw={"placeholder": "admin o usuario"},
    )

    submit = SubmitField("Registrar")

    def validate_username(self, username):
        currentUser = User.query.filter_by(username=username).first()
        if currentUser:
            raise ValidationError("El usuario ya existe")
