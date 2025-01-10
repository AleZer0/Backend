from flask import Blueprint, jsonify, request
from db import mysql

user_detail_dp = Blueprint("user_detail", __name__)


# EndPoint para obtener todos los usuarios
@user_detail_dp.route("/user_detail", methods=["GET"])
def get_all_user():
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM `user_detail`")
            data = cursor.fetchall()
            users = [
                {
                    "idUser": record[0],
                    "foto": str(record[1]),
                    "nacimiento": record[2],
                    "hora_entrada": record[3],
                    "hora_salida": record[4],
                    "tiempo_almuerzo": record[5],
                    "puesto": record[6],
                }
                for record in data
            ]
            return jsonify(users), 200
    except Exception as ex:
        return jsonify({"error": "An error occurred", "message": str(ex)}), 500
