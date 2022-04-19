from utils.db import db


class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sala = db.Column(db.String(20), nullable=False, unique=True)
    def __init__(self, sala) -> None:
        self.sala = sala
 
    def __repr__(self):
        return f"{self.sala}"
