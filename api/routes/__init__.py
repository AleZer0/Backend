from .user_detail import user_detail_dp
from .access import access_dp


def register_routes(app):
    app.register_blueprint(user_detail_dp)
    app.register_blueprint(access_dp)
