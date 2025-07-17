from flask_smorest import Blueprint
from flask.views import MethodView

from ..auth_utils import register_user, authenticate_user
from marshmallow import Schema, fields

blp = Blueprint("Auth", "auth", url_prefix="/auth", description="User authentication and registration APIs")


class RegisterInputSchema(Schema):
    username = fields.Str(required=True, description="Desired username")
    password = fields.Str(required=True, description="Desired password")


class AuthSuccessSchema(Schema):
    user_id = fields.Str(description="ID of the registered user")
    token = fields.Str(description="Login/authentication token")
    message = fields.Str(description="Success message")


class LoginInputSchema(Schema):
    username = fields.Str(required=True, description="Username")
    password = fields.Str(required=True, description="Password")

class ErrorSchema(Schema):
    message = fields.Str(description="Error message")

# PUBLIC_INTERFACE
@blp.route("/register")
class Register(MethodView):
    """Register a new user."""
    @blp.arguments(RegisterInputSchema)
    @blp.response(201, AuthSuccessSchema)
    @blp.alt_response(400, ErrorSchema, description="User already exists")
    def post(self, input_data):
        """
        Register a new user.

        Returns the user_id if successful.
        """
        ok, result = register_user(input_data['username'], input_data['password'])
        if ok:
            # Auto-login after registration
            _, token = authenticate_user(input_data['username'], input_data['password'])
            return {"user_id": result, "token": token, "message": "User registered successfully."}
        else:
            blp.abort(400, message=result)

# PUBLIC_INTERFACE
@blp.route("/login")
class Login(MethodView):
    """Authenticate an existing user."""
    @blp.arguments(LoginInputSchema)
    @blp.response(200, AuthSuccessSchema)
    @blp.alt_response(401, ErrorSchema, description="Invalid credentials")
    def post(self, input_data):
        """
        Authenticate user and return an authentication token.
        """
        ok, token = authenticate_user(input_data['username'], input_data['password'])
        if ok:
            return {"user_id": input_data['username'], "token": token, "message": "Login successful."}
        else:
            blp.abort(401, message="Invalid username or password.")
