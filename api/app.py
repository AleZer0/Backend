from flask import Flask
from flask_cors import CORS
from config import config
from db import db
from routes import register_routes


app = Flask(__name__)
CORS(app)

app.config.from_object(config["development"])
db.init_app(app)
register_routes(app)


@app.errorhandler(404)
def not_found(error):
    return {"success": False, "message": "Page not found"}, 404


if __name__ == "__main__":
    app.run(host="0.0.0.0")
