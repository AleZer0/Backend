import datetime


def date_fromating(response: dict, fecha):
    try:
        return datetime.strptime(fecha, "%Y-%m-%d").date()
    except ValueError:
        response["success"] = False
        response["mensaje"] = (
            "Formato de fecha incorrecto para 'nacimiento'. Debe ser YYYY-MM-DD."
        )
        return response


def separar_timestamp(fecha_hora: str) -> str:
    return str(fecha_hora.date()), str(fecha_hora.time())
