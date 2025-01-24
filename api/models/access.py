from db import db
from datetime import datetime


class Access(db.Model):
    __tablename__ = "access"

    idAccess = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUser = db.Column(db.Integer, db.ForeignKey("user.idUser"), nullable=True)
    fecha = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    tipoAcceso = db.Column(db.String(45), nullable=True)

    user = db.relationship("User", backref="accesses", lazy=True)

    def __init__(self, idUser, tipoAcceso, fecha=None):
        self.idUser = idUser
        self.tipoAcceso = tipoAcceso
        self.fecha = fecha or datetime.utcnow()

    def to_json(self):
        # * Convierte el modelo en un diccionario JSON.
        return {
            "idAccess": self.idAccess,
            "idUser": self.idUser,
            "fecha": self.fecha.strftime("%Y-%m-%d %H:%M:%S") if self.fecha else None,
            "tipoAcceso": self.tipoAcceso,
        }
