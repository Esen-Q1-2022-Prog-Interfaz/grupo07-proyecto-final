from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, TimeField
from wtforms.validators import InputRequired, Length
from models.salasreservas import ReservaSalas
from models.salas import Sala
from wtforms_sqlalchemy.fields import   QuerySelectField
from models.usuarios import User

def choice_query():
    return Sala.query

def choice_users():
    return User.query
class ReservaSalaFormAdmin(FlaskForm):
    solicitante = QuerySelectField("Solicitante",
        query_factory=choice_users,
        validators=[
            InputRequired()
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
    
    fecha = DateField("Fecha",
        validators=[
            InputRequired(),
        ],
        render_kw={"placeholder": "Fecha..."}
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