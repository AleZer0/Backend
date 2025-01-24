from db import db
import base64


class UserDetail(db.Model):
    __tablename__ = "user_detail"

    idUser = db.Column(db.Integer, db.ForeignKey("user.idUser"), primary_key=True)
    foto = db.Column(db.LargeBinary, nullable=True)
    nacimiento = db.Column(db.DateTime, nullable=True, default=None)
    hora_entrada = db.Column(db.String(45), nullable=True)
    hora_salida = db.Column(db.String(45), nullable=True)
    tiempo_almuerzo = db.Column(db.String(45), nullable=True)
    puesto = db.Column(db.String(45), nullable=True)

    user = db.relationship("User", backref="details", lazy=True)

    def __init__(
        self,
        idUser,
        foto=None,
        nacimiento=None,
        hora_entrada=None,
        hora_salida=None,
        tiempo_almuerzo=None,
        puesto=None,
    ):
        self.idUser = idUser
        self.foto = foto
        self.nacimiento = nacimiento
        self.hora_entrada = hora_entrada
        self.hora_salida = hora_salida
        self.tiempo_almuerzo = tiempo_almuerzo
        self.puesto = puesto

    def to_json(self):
        # * Convierte el modelo en un diccionario JSON.
        return {
            "idUser": self.idUser,
            "foto": base64.b64encode(self.foto).decode("utf-8") if self.foto else None,
            "nacimiento": (
                self.nacimiento.strftime("%Y-%m-%d %H:%M:%S")
                if self.nacimiento
                else None
            ),
            "hora_entrada": self.hora_entrada,
            "hora_salida": self.hora_salida,
            "tiempo_almuerzo": self.tiempo_almuerzo,
            "puesto": self.puesto,
        }
