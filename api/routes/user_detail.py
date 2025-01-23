from flask import Blueprint, jsonify, request
from db import mysql
from utils import get_one, decode_image
import base64

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
                    "foto": decode_image(record[3]),
                    "puesto": record[4],
                }
                for record in data
            ]
            return (
                jsonify(
                    {
                        "usuarios": users,
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


import base64
from datetime import datetime


@user_detail_dp.route("/user_detail", methods=["POST"])
def post_user():
    response = {}

    # Validación inicial de datos
    data = request.get_json()
    if not data or not all(
        key in data for key in ["nombre", "apellido", "puesto", "foto", "nacimiento"]
    ):
        response["success"] = False
        response["mensaje"] = "Faltan datos."
        return jsonify(response), 400

    # Valida y convierte la fecha de nacimiento
    try:
        nacimiento = datetime.strptime(data["nacimiento"], "%Y-%m-%d").date()
    except ValueError:
        response["success"] = False
        response["mensaje"] = (
            "Formato de fecha incorrecto para 'nacimiento'. Debe ser YYYY-MM-DD."
        )
        return jsonify(response), 400

    # Decodifica la foto
    try:
        decoded_foto = base64.b64decode(
            data["foto"].split(",")[1]
        )  # Eliminar el encabezado Base64
    except Exception as e:
        response["success"] = False
        response["mensaje"] = f"Error al decodificar la foto: {e}"
        return jsonify(response), 400

    try:
        with mysql.connection.cursor() as cursor:
            # Inserta en la tabla "user"
            cursor.execute(
                "INSERT INTO `user` (`nombre`, `apellido`) VALUES (%s, %s)",
                (
                    data["nombre"],
                    data["apellido"],
                ),
            )
            mysql.connection.commit()

            # Obtén el ID recién creado
            cursor.execute("SELECT `idUser` FROM `user` ORDER BY `idUser` DESC LIMIT 1")
            new_idUser = cursor.fetchone()[0]

            # Inserta en la tabla "user_detail"
            cursor.execute(
                "INSERT INTO `user_detail` (`idUser`, `foto`, `nacimiento`, `puesto`) VALUES (%s, %s, %s, %s)",
                (
                    new_idUser,
                    decoded_foto,
                    nacimiento,
                    data["puesto"],
                ),
            )
            mysql.connection.commit()

        response["success"] = True
        response["mensaje"] = "El registro se guardó correctamente."
        return jsonify(response), 200

    except Exception as ex:
        response["success"] = False
        response["mensaje"] = f"Error: {ex}"
        return jsonify(response), 500


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
                "DELETE FROM `user_detail` WHERE `idUser` = %s",
                (idUser,),
            )
            cursor.execute(
                "DELETE FROM `user` WHERE `idUser` = %s",
                (idUser,),
            )
            mysql.connection.commit()
            return jsonify(
                {"mensaje": "El usuario se elimino correctamente.", "success": True}
            )
    except Exception as ex:
        return (
            jsonify({"mensaje": "Error?: " + ex, "success": False}),
            500,
        )
