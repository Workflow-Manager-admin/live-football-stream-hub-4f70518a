from flask import Flask
from flask_cors import CORS
from .routes.health import blp as health_blp
from .routes.auth import blp as auth_blp
from .routes.match import blp as match_blp
from .routes.stream import blp as stream_blp
from .routes.chat import blp as chat_blp

from flask_smorest import Api

# Ensure demo data is created at app load time
from . import models  # noqa

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["API_TITLE"] = "Football Live Stream API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = '/docs'
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
api.register_blueprint(health_blp)
api.register_blueprint(auth_blp)
api.register_blueprint(match_blp)
api.register_blueprint(stream_blp)
api.register_blueprint(chat_blp)
