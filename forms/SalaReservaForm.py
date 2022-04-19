from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, TimeField
from wtforms.validators import InputRequired, Length
from models.salasreservas import ReservaSalas
from wtforms_sqlalchemy.fields import QuerySelectField
from models.salas import Sala

def choice_query():
    return Sala.query

class ReservaSalaForm(FlaskForm):
    solicitante = StringField( "Solicitante",
        validators=[
            InputRequired(),
            Length(min=3, max=20),
        ],
        render_kw={"placeholder": "Solicitante"},
    )

    idSala =QuerySelectField( "Sala",
        query_factory=choice_query,
        validators=[
            InputRequired(),
        ],
        render_kw={"placeholder": "Sala..."},
    )
    
    horaInicio = TimeField("Hora de inicio",
        validators=[
            InputRequired(),
        ],
        format="%H:%M",
        render_kw={"placeholder": "Hora Inicio..."}
    )
    
    horaFinal = TimeField("Hora de salida",
        validators=[
            InputRequired(),
        ],
        format="%H:%M",
        render_kw={"placeholder": "Hora Final..."}
    )
    submit = SubmitField("Reservar")