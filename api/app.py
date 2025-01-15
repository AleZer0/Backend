from flask import Flask
from flask_cors import CORS
from config import config
from db import mysql

# ? Importación de todos los bluprints
from routes.user_detail import user_detail_dp
from routes.access import access_dp

app = Flask(__name__)
CORS(app)
mysql.init_app(app)

# * Registrar todos los Bluprints (rutas)
app.register_blueprint(user_detail_dp)
app.register_blueprint(access_dp)


def not_found(error):
    return "<h1>La página no existe...<h1>", 404


if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.register_error_handler(404, not_found)
    app.run(host="0.0.0.0", port=5000)
