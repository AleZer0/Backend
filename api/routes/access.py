from flask import Blueprint, jsonify
from db import mysql
from utils import separar_timestamp

access_dp = Blueprint("access", __name__)


# EndPoint para obtener todos los accesos de usuarios
@access_dp.route("/user_access", methods=["GET"])
def get_all_user_access():
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    ud.idUser,
                    a.fecha,
                    a.tipoAcceso
                FROM `user_detail` ud
                JOIN `user` u ON ud.idUser = u.idUser
                JOIN `access` a ON ud.idUser = a.idUser
                ORDER BY ud.idUser, a.fecha;
                """
            )
            data: tuple = cursor.fetchall()

            access: dict | list = {}
            for record in data:
                idUser: str = str(record[0])
                if idUser not in access:
                    access[idUser] = {}

                fecha, hora = separar_timestamp(record[1])
                if fecha not in access[idUser]:
                    access[idUser][fecha] = {}

                acces_type = record[2]
                access[idUser][fecha][acces_type] = hora

            access = [{user_id: data} for user_id, data in access.items()]
            return (
                jsonify(
                    {
                        "accesos": access,
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
