from flask_smorest import Blueprint
from flask.views import MethodView
from marshmallow import Schema, fields
from flask import request

from ..auth_utils import validate_token
from ..models import CHAT_MESSAGES
import time

blp = Blueprint("Chat", "chat", url_prefix="/api", description="Live chat endpoints")

class ChatMessageSchema(Schema):
    username = fields.Str()
    message = fields.Str()
    timestamp = fields.Float()
    match_id = fields.Str()

class ChatMessageInSchema(Schema):
    message = fields.Str(required=True)

class ChatMessagesListSchema(Schema):
    messages = fields.List(fields.Nested(ChatMessageSchema))

class ErrorSchema(Schema):
    message = fields.Str()

def require_auth():
    token = request.headers.get("Authorization")
    if not token:
        blp.abort(401, message="Missing Authorization header.")
    user = validate_token(token)
    if not user:
        blp.abort(401, message="Invalid or expired token.")
    return user

# PUBLIC_INTERFACE
@blp.route("/chat/<match_id>")
class ChatMessages(MethodView):
    """Get and post chat messages for a match."""
    @blp.response(200, ChatMessagesListSchema)
    def get(self, match_id):
        """
        Get all chat messages for the match.
        """
        msgs = CHAT_MESSAGES.get(match_id, [])
        return {"messages": msgs}

    @blp.arguments(ChatMessageInSchema)
    @blp.response(201, ChatMessageSchema)
    @blp.alt_response(401, ErrorSchema)
    def post(self, input_data, match_id):
        """
        Post a new chat message for the match.
        Requires auth token in 'Authorization' header.
        """
        user = require_auth()
        entry = {
            "username": user["username"],
            "message": input_data["message"],
            "timestamp": time.time(),
            "match_id": match_id
        }
        CHAT_MESSAGES.setdefault(match_id, []).append(entry)
        return entry
