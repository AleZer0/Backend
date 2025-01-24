from flask import Blueprint, jsonify, request
from sqlalchemy.orm import joinedload
from db import db
from models import User, UserDetail
from datetime import datetime
import base64

user_detail_dp = Blueprint("user_detail", __name__)


# * Endpoint para obtener todos los usuarios.
@user_detail_dp.route("/user_detail", methods=["GET"])
def get_all_user_details():
    try:
        users_with_details = (
            UserDetail.query.join(User, UserDetail.idUser == User.idUser)
            .options(joinedload(UserDetail.user))
            .order_by(UserDetail.idUser)
            .all()
        )
        users = [
            {
                "idUser": detail.idUser,
                "nombre": detail.user.nombre,
                "apellido": detail.user.apellido,
                "foto": (
                    base64.b64encode(detail.foto).decode("utf-8")
                    if detail.foto
                    else None
                ),
                "puesto": detail.puesto,
            }
            for detail in users_with_details
        ]

        return (
            jsonify(
                {
                    "usuarios": users,
                    "mensaje": "Todos los usuarios con sus detalles obtenidos correctamente.",
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


# * Endpoint para crear un nuevo usuario.
@user_detail_dp.route("/user_detail", methods=["POST"])
def post_user():
    data = request.get_json()
    if not data or not all(
        key in data for key in ["nombre", "apellido", "puesto", "foto", "nacimiento"]
    ):
        return jsonify({"success": False, "mensaje": "Faltan datos."}), 400

    try:
        nacimiento = datetime.strptime(data["nacimiento"], "%Y-%m-%d").date()
    except ValueError:
        return (
            jsonify(
                {
                    "success": False,
                    "mensaje": "Formato de fecha incorrecto para 'nacimiento'. Debe ser YYYY-MM-DD.",
                }
            ),
            400,
        )

    try:
        decoded_foto = base64.b64decode(data["foto"].split(",")[1])
    except Exception as e:
        return (
            jsonify(
                {"success": False, "mensaje": f"Error al decodificar la foto: {e}"}
            ),
            400,
        )

    try:
        with db.session.begin():
            new_user = User(nombre=data["nombre"], apellido=data["apellido"])
            db.session.add(new_user)
            db.session.flush()

            new_user_detail = UserDetail(
                idUser=new_user.idUser,
                foto=decoded_foto,
                nacimiento=nacimiento,
                puesto=data["puesto"],
            )
            db.session.add(new_user_detail)

        return (
            jsonify(
                {"success": True, "mensaje": "El registro se guardó correctamente."}
            ),
            200,
        )
    except Exception as ex:
        db.session.rollback()
        return jsonify({"success": False, "mesnaje": f"Error: {ex}"}), 500


from flask import jsonify, request
from db import db
from models import User, UserDetail


# * Endpoint para eliminar un usuario.
@user_detail_dp.route("/user_detail/<int:idUser>", methods=["DELETE"])
def delete_user(idUser: int):
    try:
        user = User.query.get(idUser)
        if not user:
            return (
                jsonify(
                    {"mensaje": f"El usuario '{idUser}' no existe.", "success": False}
                ),
                404,
            )

        user_detail = UserDetail.query.filter_by(idUser=idUser).first()
        if user_detail:
            db.session.delete(user_detail)
        db.session.delete(user)
        db.session.commit()

        return (
            jsonify(
                {"mensaje": "El usuario se eliminó correctamente.", "success": True}
            ),
            200,
        )
    except Exception as ex:
        db.session.rollback()
        return (
            jsonify({"mensaje": f"Error: {str(ex)}", "success": False}),
            500,
        )
