from flask_smorest import Blueprint
from flask.views import MethodView
from marshmallow import Schema, fields

from ..models import MATCHES

blp = Blueprint("Stream", "stream", url_prefix="/api", description="Live stream management/check APIs")

class StreamUrlSchema(Schema):
    stream_url = fields.Str(description="Live stream URL for the match")

class StreamStatusSchema(Schema):
    match_id = fields.Str()
    status = fields.Str()

class ErrorSchema(Schema):
    message = fields.Str()

# PUBLIC_INTERFACE
@blp.route("/stream/<match_id>")
class StreamUrl(MethodView):
    """Retrieve live stream URL for a match."""
    @blp.response(200, StreamUrlSchema)
    @blp.alt_response(404, ErrorSchema)
    def get(self, match_id):
        """
        Get the streaming URL for a given match ID.
        """
        match = MATCHES.get(match_id)
        if not match:
            blp.abort(404, message="No such match")
        return {"stream_url": match.get("stream_url")}

# PUBLIC_INTERFACE
@blp.route("/stream/status/<match_id>")
class StreamStatus(MethodView):
    """Check status ('scheduled', 'live', 'ended') for any match."""
    @blp.response(200, StreamStatusSchema)
    @blp.alt_response(404, ErrorSchema)
    def get(self, match_id):
        """
        Get the live/ended/scheduled status for a given match ID.
        """
        match = MATCHES.get(match_id)
        if not match:
            blp.abort(404, message="Match not found")
        return {"match_id": match_id, "status": match.get("status")}
