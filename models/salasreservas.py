from utils.db import db

class ReservaSalas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    solicitante = db.Column(db.String(50), nullable=False)
    idSala = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.String(20), nullable=False)
    horaInicio = db.Column(db.String(20), nullable=False)
    horaFinal = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(10), nullable = False)
    
    
    
    def __init__(self, solicitante, idSala, fecha, horaInicio, horaFinal, estado = 'Pendiente') -> None:
        self.solicitante = solicitante
        self.idSala = idSala
        self.fecha = fecha
        self.horaInicio = horaInicio
        self.horaFinal = horaFinal
        self.estado = estado
 
    def __repr__(self):
        return f"Reserva({self.id}, '{self.solicitante}', '{self.idSala}', '{self.fecha}', '{self.horaInicio}', '{self.horaFinal}', '{self.estado}')"
