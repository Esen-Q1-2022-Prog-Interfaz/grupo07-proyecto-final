from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from models.usuarios import User


class LoginForm(FlaskForm):
    username = StringField( "Usuario",
        validators=[
            InputRequired(),
            Length(min=4, max=20),
        ],
        render_kw={"placeholder": "Usuario..."},
    )

    password = PasswordField( "Contraseña",
        validators=[
            InputRequired(),
            Length(min=4, max=20),
        ],
        render_kw={"placeholder": "Contraseña..."},
    )

    submit = SubmitField("Ingresar")
