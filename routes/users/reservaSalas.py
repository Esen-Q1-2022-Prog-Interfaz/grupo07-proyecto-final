from flask import Blueprint, render_template, redirect, url_for, Flask
from utils.db import db
from flask_login import current_user, login_required
from models.salasreservas import ReservaSalas
from forms.SalaReservaFormUser import ReservaSalaFormUser
from datetime import datetime

usersalas = Blueprint("usersalas", __name__, url_prefix="/usuarios/salas")

 
@usersalas.route("/calendar/")
@login_required
def calendario():        
    return render_template("user/calendario.html")
 
@usersalas.route("/calendar/reservaSala/<month>/<day>/<year>", methods=["GET", "POST"])
@login_required
def createSalaReserve(month, day, year): 
    if len(str(day)) ==1:
        day = str(0)+str(day)
    if len(str(month)) == 1:
        month = str(0)+str(month)
    fecha = str(year) + "-" + str(month) + "-" + str(day)  
    form = ReservaSalaFormUser()
    solicitante=current_user.username
    if form.validate_on_submit():
        idSala = form.idSala.data
        horaInicio = form.horaInicio.data
        horaFinal = form.horaFinal.data
        if comparar(fecha, horaInicio, idSala, horaFinal):
            registro = ReservaSalas(solicitante, idSala, fecha, horaInicio, horaFinal)
            db.session.add(registro)
            db.session.commit()
            return redirect(url_for('reservationhasbeencreated', mes = month, dia = day, year = year))
        else:
            return render_template('user/errorCreacionSolicitud.html')
    return render_template("user/salas.html", solicitante = solicitante, form = form, month=month, day = day, year = year)

def comparar(fecha, horaInicio, idSala, horaFinal):
    reservasExistentes = ReservaSalas.query.all()
    counter = 0
    for reserva in reservasExistentes:
        mismaFecha = str(reserva.fecha) == fecha
        mismoMomentoInicio = str(reserva.horaInicio) == str(horaInicio)
        mismoInicio = mismaFecha and mismoMomentoInicio
        #misma sala -- siempre se verifica
        mismaSala = str(reserva.idSala)==str(idSala)

        fechaHoraInicioCreandoStr = str(fecha).rstrip().lstrip()+" "+str(horaInicio).rstrip().lstrip()
        fechaHoraInicioCreando = datetime.strptime(fechaHoraInicioCreandoStr, '%Y-%m-%d %H:%M:%S')

        fechaHoraInicioTablaStr = str(reserva.fecha).rstrip().lstrip()+" "+str(reserva.horaInicio).rstrip().lstrip()
        fechaHoraInicioTabla = datetime.strptime(fechaHoraInicioTablaStr, '%Y-%m-%d %H:%M:%S')

        fechaHoraFinCreandoStr=str(fecha).rstrip().lstrip()+" "+str(horaFinal).rstrip().lstrip()
        fechaHoraFinCreando = datetime.strptime(fechaHoraFinCreandoStr, '%Y-%m-%d %H:%M:%S')

        fechaHoraFinTablaStr = str(reserva.fecha).rstrip().lstrip()+" "+str(reserva.horaFinal).rstrip().lstrip()
        fechaHoraFinTabla = datetime.strptime(fechaHoraFinTablaStr, '%Y-%m-%d %H:%M:%S')

        horaInicioCreandoEnMedioDeReserva = (fechaHoraInicioCreando >= fechaHoraInicioTabla and fechaHoraInicioCreando <= fechaHoraFinTabla)
        horaFinCreandoEnMedioDeReserva = (fechaHoraFinCreando >= fechaHoraInicioTabla and fechaHoraFinCreando <= fechaHoraFinTabla)
        
        reservaTablaEncasillada = ( fechaHoraInicioCreando <= fechaHoraInicioTabla and  fechaHoraFinCreando >= fechaHoraFinTabla)
        if mismaSala and ( (horaInicioCreandoEnMedioDeReserva) or (horaFinCreandoEnMedioDeReserva) or (reservaTablaEncasillada) ) and str(reserva.estado)=="Aprobado":
            counter+=1
    if counter != 0:
        return False
    else:
        return True
    
@usersalas.route("/calendar/<string:Id>")
@login_required
def misReservas(Id):
    reservasLista = ReservaSalas.query.filter_by(solicitante=Id)
    return render_template("user/solicitudes.html", items = reservasLista) 
 