from flask import Blueprint, jsonify
from db import mysql
from utils import separar_timestamp

access_dp = Blueprint("access", __name__)


# EndPoint para obtener todos los accesos de usuarios
@access_dp.route("/user_access_semana=<int:semana>", methods=["GET"])
def get_all_user_access(semana: int):
    try:
        query = """
        SELECT
            ud.idUser,
            u.nombre,
            u.apellido,
            ud.puesto,
            ud.foto,
            a.fecha,
            a.tipoAcceso,
            WEEK(a.fecha, 1) AS semana
        FROM `user_detail` ud
        JOIN `user` u ON ud.idUser = u.idUser
        JOIN `access` a ON ud.idUser = a.idUser
        WHERE WEEK(a.fecha, 1) = %s
        ORDER BY ud.idUser, a.fecha;
        """
        with mysql.connection.cursor() as cursor:
            cursor.execute(query, (semana,))
            data: list = cursor.fetchall()

        users_access = {}
        for record in data:
            idUser, nombre, apellido, puesto, foto, fecha_hora, tipoAcceso, semana = (
                record
            )
            fecha, hora = separar_timestamp(fecha_hora)

            users_access.setdefault(
                idUser,
                {
                    "usuario": {
                        "idUser": idUser,
                        "nombre": nombre,
                        "apellido": apellido,
                        "puesto": puesto,
                        # "foto": str(foto).replace("b'", "").replace("'", ""),
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

            if acceso_existente:
                acceso_existente["horarios"][tipoAcceso] = hora
            else:
                users_access[idUser]["accesos"].append(
                    {
                        "fecha": fecha,
                        "semana": semana,
                        "horarios": {tipoAcceso: hora},
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


@access_dp.route("/access/iUser=<int:idUser>/semana=<int:semana>", methods=["GET"])
def get_user_accees(idUser: int, semana: int):
    try:
        query = """
        SELECT
            `idUser`,
            `fecha`,
            `tipoAcceso`,
            WEEK(`fecha`, 1) AS semana
        FROM `access` WHERE `idUser` = %s AND WEEK(`fecha`, 1) = %s;
        """
        with mysql.connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    idUser,
                    semana,
                ),
            )
            data: list = cursor.fetchall()

        accesos = []
        for record in data:
            fecha, hora = separar_timestamp(record[1])
            acceso_existente = next(
                (acceso for acceso in accesos if acceso["fecha"] == fecha),
                None,
            )

            if acceso_existente:
                acceso_existente["horarios"][record[2]] = hora
            else:
                accesos.append(
                    {
                        "fecha": fecha,
                        "semana": record[3],
                        "horarios": {record[2]: hora},
                    }
                )

        return (
            jsonify(
                {
                    "accesos": accesos,
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


@access_dp.route("/access/summary/semana=<int:semana>", methods=["GET"])
def sumary(semana: int):
    return jsonify(
        {
            "success": True,
            "accesosPorTipo": [
                {"tipo": "Entrada", "cantidad": 45},
                {"tipo": "Almuerzo", "cantidad": 30},
                {"tipo": "Regreso Almuerzo", "cantidad": 28},
                {"tipo": "Salida", "cantidad": 40},
            ],
        }
    )
