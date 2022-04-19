from flask import Flask, redirect, render_template, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from routes.admin.dashboard import admin
from routes.admin.salas import salas
from routes.admin.usuarios import users
from routes.admin.solicitudes import solicitudes
from routes.auth import auth
from routes.users.reservaSalas import usersalas
from routes.auth import auth
from routes.users.usuario import usuarios
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from utils.db import db
from utils.loginManagerService import login_manager
from models.usuarios import User
from models.salasreservas import ReservaSalas

app = Flask(__name__)

app.config.from_object("config.BaseConfig")
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'non.reply.fantel@gmail.com'
app.config['MAIL_PASSWORD'] = 'FlaskLogin'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


SQLAlchemy(app)
Bcrypt(app)
login_manager.init_app(app)
Migrate(app, db)
mail= Mail(app)

app.register_blueprint(admin)
app.register_blueprint(users)
app.register_blueprint(solicitudes)
app.register_blueprint(usersalas)
app.register_blueprint(auth)
app.register_blueprint(salas)
app.register_blueprint(usuarios)

def getadminmail():
    with app.app_context():
        db.create_all()
        theAdmins = User.query.filter_by(rank='admin')
        return theAdmins
    
@app.route("/reservationhasbeencreated/<mes>/<dia>/<year>")
def reservationhasbeencreated(mes, dia, year):
    theAdmins = getadminmail()
    with mail.connect() as conn:
        for user in theAdmins:
            message = f'Este mensaje ha sido generado automáticamente para notificar que {current_user.username} ha creado una nueva solicitud de reserva para la fecha {dia}/{mes}/{year}. Por favor, verifique en el dashboard.'
            subject = f"Nueva Reservación de {current_user.username} - {dia}/{mes}/{year}."
            msg = Message(recipients=[user.email],
                        body=message,
                        subject=subject,
                        sender='non.reply.fantel@gmail.com')
            
            conn.send(msg)
        
    usermsg = Message( subject=f'Solicitud de reservación para la fecha {dia}/{mes}/{year} enviada.', recipients = [f'{current_user.email}'], body=f'Este mensaje ha sido generado automáticamente para notificar que su solicitud de reserva para la fecha {dia}/{mes}/{year} ha sido enviada. Este correo no implica una aceptación ni un rechazo a su solicitud, ya que esta debe de ser procesada por un administrador. Una vez su solicitud sea procesada, recibirá un nuevo correo en el que se le indicará la respuesta obtenida.', sender='non.reply.fantel@gmail.com', )
    mail.send(usermsg)

    return render_template('user/confirmacion.html')

def correoUsuarioCambio(id):
    with app.app_context():
        db.create_all()
        solicitudActual = ReservaSalas.query.get(id)
        usuarioEnReserva = solicitudActual.solicitante
        usuario =  User.query.filter_by(username=usuarioEnReserva).first()
        return usuario
@app.route("/changestatus/<newstatus>/<id>")
def mailCambiarEstado(newstatus, id):
    usuario = correoUsuarioCambio(id)
    solicitudActual =ReservaSalas.query.get(id)
    updatestatusmsg = Message(
                subject=f'Nueva respuesta a solicitud de sala',
                recipients=[usuario.email],
                body=f'Este mensaje ha sido generado automáticamente para notificar que el estado de su solicitud para reservar la sala {solicitudActual.idSala}, ha cambiado a {newstatus}. Por favor, confirme revisando el dashboard.',
                sender='non.reply.fantel@gmail.com')
    mail.send(updatestatusmsg)
    return redirect(url_for('solicitudes.vista'))



