from db import db


class User(db.Model):
    __tablename__ = "user"

    idUser = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(45), nullable=True)
    apellido = db.Column(db.String(45), nullable=True)
    huella = db.Column(db.LargeBinary, nullable=True)

    def __init__(self, nombre, apellido, huella=None):
        self.nombre = nombre
        self.apellido = apellido
        self.huella = huella

    def to_json(self):
        # * Convierte el modelo en un diccionario JSON.
        return {
            "idUser": self.idUser,
            "nombre": self.nombre,
            "apellido": self.apellido,
            # "huella": self.huella.hex() if self.huella else None,
        }
