from flask import Blueprint, jsonify
from db import mysql
from utils import separar_timestamp

access_dp = Blueprint("access", __name__)


# EndPoint para obtener todos los accesos de usuarios
@access_dp.route("/user_access", methods=["GET"])
def get_all_user_access():
    try:
        query = """
            SELECT
                ud.idUser,
                u.nombre,
                u.apellido,
                ud.foto,
                a.fecha,
                a.tipoAcceso,
                WEEK(a.fecha, 1) AS semana
            FROM `user_detail` ud
            JOIN `user` u ON ud.idUser = u.idUser
            JOIN `access` a ON ud.idUser = a.idUser
            ORDER BY ud.idUser, a.fecha;
        """
        with mysql.connection.cursor() as cursor:
            cursor.execute(query)
            data: list = cursor.fetchall()

            users_access = {}
            for record in data:
                idUser, nombre, apellidos, foto, fecha_hora, tipoAcceso, semana = record
                fecha, hora = separar_timestamp(fecha_hora)

                users_access.setdefault(
                    idUser,
                    {
                        "user": {
                            "idUser": idUser,
                            "nombre": nombre,
                            "apellidos": apellidos,
                            "foto": str(foto),
                        },
                        "accesos": [],
                    },
                )

                acceso_existente = next(
                    (
                        acceso
                        for acceso in users_access[idUser]["accesos"]
                        if acceso["fecha"] == fecha
                    ),
                    None,
                )
                print(acceso_existente)

                if acceso_existente:
                    acceso_existente["horarios"][tipoAcceso] = hora
                else:
                    users_access[idUser]["accesos"].append(
                        {
                            "fecha": fecha,
                            "semana": semana,
                            "horarios": {tipoAcceso: tipoAcceso},
                        }
                    )
            response = list(users_access.values())

            return (
                jsonify(
                    {
                        "usuarios": response,
                        "mensaje": "Todos los accesos de los usuarios filtrados por fecha.",
                        "success": True,
                    }
                ),
                200,
            )
    except Exception as ex:
        return (
            jsonify({"mensaje": str(ex), "success": False}),
            500,
        )
