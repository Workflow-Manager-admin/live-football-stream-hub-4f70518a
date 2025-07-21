from flask_smorest import Blueprint
from flask.views import MethodView
from marshmallow import Schema, fields

from ..models import MATCHES, TEAMS, PLAYERS

blp = Blueprint("Matches", "matches", url_prefix="/api", description="Match schedule, teams, and player stats APIs")

class TeamSchema(Schema):
    id = fields.Str()
    name = fields.Str()

class PlayerSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    goals = fields.Int()
    team_id = fields.Str()

class MatchSchema(Schema):
    id = fields.Str()
    home_team = fields.Nested(TeamSchema)
    away_team = fields.Nested(TeamSchema)
    start_time = fields.Str()
    status = fields.Str() # scheduled, live, ended
    stream_url = fields.Str()

class MatchListSchema(Schema):
    matches = fields.List(fields.Nested(MatchSchema))

class ErrorSchema(Schema):
    message = fields.Str()

# PUBLIC_INTERFACE
@blp.route("/matches")
class MatchList(MethodView):
    """List all scheduled and live matches."""
    @blp.response(200, MatchListSchema)
    def get(self):
        """
        Get list of scheduled/live matches.
        """
        return {"matches": list(MATCHES.values())}

# PUBLIC_INTERFACE
@blp.route("/matches/<match_id>")
class MatchInfo(MethodView):
    """Get details for a specific match."""
    @blp.response(200, MatchSchema)
    @blp.alt_response(404, ErrorSchema, description="Not found")
    def get(self, match_id):
        """
        Get details for a specific match by ID.
        """
        match = MATCHES.get(match_id)
        if not match:
            blp.abort(404, message="Match not found")
        return match

# PUBLIC_INTERFACE
@blp.route("/teams")
class TeamList(MethodView):
    """List all teams."""

    class TeamsListSchema(Schema):
        teams = fields.List(fields.Nested(TeamSchema))

    @blp.response(200, TeamsListSchema)
    def get(self):
        """
        List all teams and their IDs.
        """
        return {"teams": list(TEAMS.values())}

# PUBLIC_INTERFACE
@blp.route("/players")
class PlayerList(MethodView):
    """List all players."""

    class PlayersListSchema(Schema):
        players = fields.List(fields.Nested(PlayerSchema))

    @blp.response(200, PlayersListSchema)
    def get(self):
        """
        List all players and their stats.
        """
        return {"players": list(PLAYERS.values())}
