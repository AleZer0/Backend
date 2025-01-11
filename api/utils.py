from datetime import datetime
from db import mysql


def separar_timestamp(fecha_hora: datetime) -> str:
    return str(fecha_hora.date()), str(fecha_hora.time())


def get_one(table: str, name_id: str, id: int) -> dict | None:
    query_columns = """
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'accesos_xrom'
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
