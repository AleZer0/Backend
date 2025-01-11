from flask import Blueprint, jsonify
from db import mysql
from utils import get_one

user_detail_dp = Blueprint("user_detail", __name__)


# EndPoint para obtener todos los usuarios
@user_detail_dp.route("/user_detail", methods=["GET"])
def get_all_users():
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    ud.idUser,
                    u.nombre,
                    u.apellido,
                    ud.foto,
                    ud.puesto
                FROM `user_detail` ud
                JOIN `user` u ON ud.idUser = u.idUser
                ORDER BY ud.idUser;
                """
            )
            data = cursor.fetchall()
            users = [
                {
                    "idUser": record[0],
                    "nombre": record[1],
                    "apellido": record[2],
                    # "foto": str(record[3]),
                    "puesto": record[4],
                }
                for record in data
            ]
            return jsonify({"usuarios": users, "success": True}), 200
    except Exception as ex:
        return (
            jsonify({"mensaje": str(ex), "success": False}),
            500,
        )


# EndPoint para eliminar un nusuario
@user_detail_dp.route("/user_detail/<int:idUser>", methods=["DELETE"])
def delete_user(idUser: int):
    if get_one("user", "idUser", idUser) is None:
        return (
            jsonify({"mensaje": f"El usuario '{idUser}' no existe.", "success": False}),
            404,
        )

    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE ud, u
                FROM `user_detail` ud
                JOIN `user` u ON ud.idUser = u.idUser
                WHERE ud.idUser = %s;
                """,
                (idUser,),
            )
            mysql.connection.commit()
            return jsonify(
                {"mensaje": "El usuario se elimino correctamente.", "success": True}
            )
    except Exception as ex:
        return (
            jsonify({"mensaje": str(ex), "success": False}),
            500,
        )
