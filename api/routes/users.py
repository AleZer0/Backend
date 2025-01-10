from flask import Blueprint, jsonify, request
from db import mysql

user_dp = Blueprint("user", __name__)


# EndPoint para obtener todos los usuarios
@user_dp.route("/user", methods=["GET"])
def get_all_user():
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM `user`")
            data = cursor.fetchall()
            users = [
                {"idUser": record[0], "nombre": record[1], "apellido": record[2]}
                for record in data
            ]
            return jsonify(users), 200
    except Exception as ex:
        return jsonify({"error": "An error occurred", "message": str(ex)}), 500
