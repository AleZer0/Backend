from datetime import datetime
import base64, re
from db import mysql


def separar_timestamp(fecha_hora: str) -> str:
    return str(fecha_hora.date()), str(fecha_hora.time())


def decode_image(longblob_data: bytes) -> bytes:
    return base64.b64encode(longblob_data).decode("utf-8")


def get_one(table: str, name_id: str, id: int) -> dict | None:
    query_columns = """
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'cheacdor-xrom'
            AND TABLE_NAME = %s;
        """
    query_data = f"SELECT * FROM `{table}` WHERE `{name_id}` = %s"

    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute(query_columns, (table,))
            columns = [column[0] for column in cursor.fetchall()]

            cursor.execute(query_data, (id,))
            row = cursor.fetchone()

            if row is None:
                return None

            data = dict(zip(columns, row))
            return data
    except Exception as e:
        print(f"Error en get_one: {e}")
        return None
