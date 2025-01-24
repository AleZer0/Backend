from flask import Blueprint, jsonify
from utils import separar_timestamp
from models import Access
from db import db

access_dp = Blueprint("access", __name__)


# * Endpoint para obtener todos los accesos de un usuario.
@access_dp.route("/access/iUser=<int:idUser>", methods=["GET"])
def get_user_access(idUser: int):
    try:
        accesses = Access.query.filter_by(idUser=idUser).order_by(Access.fecha).all()

        if not accesses:
            return (
                jsonify(
                    {
                        "mensaje": f"El usuario con ID {idUser} no tiene accesos.",
                        "success": False,
                    }
                ),
                404,
            )

        accesos = []
        for access in accesses:
            fecha, hora = separar_timestamp(access.fecha)
            semana = access.fecha.isocalendar()[1]

            acceso_existente = next(
                (acceso for acceso in accesos if acceso["fecha"] == fecha),
                None,
            )

            if acceso_existente:
                acceso_existente["horarios"][access.tipoAcceso] = hora
            else:
                accesos.append(
                    {
                        "fecha": fecha,
                        "semana": semana,
                        "horarios": {access.tipoAcceso: hora},
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
            jsonify({"mensaje": f"Error: {str(ex)}", "success": False}),
            500,
        )


# * Endpoint para obtener el número de acceso por tipos.
from flask import jsonify
from sqlalchemy import func, extract
from models import Access


@access_dp.route("/access/summary", methods=["GET"])
def get_access_summary():
    try:
        results = (
            db.session.query(
                func.year(
                    func.str_to_date(func.yearweek(Access.fecha, 1), "%X%V")
                ).label("año_iso"),
                func.week(Access.fecha, 1).label("semana_iso"),
                Access.tipoAcceso,
                func.count(Access.idAccess).label("total"),
            )
            .group_by("año_iso", "semana_iso", Access.tipoAcceso)
            .order_by("año_iso", "semana_iso")
            .all()
        )

        summary = []
        semanas = {}

        for año_iso, semana_iso, tipoAcceso, total in results:
            if semana_iso == 0:
                continue
            if semana_iso not in semanas:
                semanas[semana_iso] = {"semana": int(semana_iso), "tipoAccesos": {}}
            semanas[semana_iso]["tipoAccesos"][tipoAcceso] = total

        summary = list(semanas.values())

        return jsonify({"success": True, "summary": summary}), 200

    except Exception as ex:
        return jsonify({"success": False, "mensaje": f"Error: {str(ex)}"}), 500
