from flask import Flask
from flask_cors import CORS
from config import config
from db import db
from routes import register_routes


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    CORS(app)

    db.init_app(app)
    register_routes(app)

    @app.errorhandler(404)
    def not_found(error):
        return {"success": False, "message": "Page not found"}, 404

    return app


if __name__ == "__main__":
    app = create_app("development")
    app.run(host="0.0.0.0", port=5000)
