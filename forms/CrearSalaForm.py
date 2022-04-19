from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length

class CrearSalasForm(FlaskForm):
    sala = StringField( "Sala",
        validators=[
            InputRequired(),
            Length(min=2, max=20),
        ],
        render_kw={"placeholder": "sala..."},
    )
    
    submit = SubmitField("Crear")