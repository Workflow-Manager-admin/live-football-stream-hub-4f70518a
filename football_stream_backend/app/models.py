"""
Contains data models for users, matches, teams, players, and messages.
(Data is currently in-memory for demonstration. Replace with DB-integration as needed.)
"""

import datetime

# --- In-memory Database Substitute ---
USERS = {}
MATCHES = {}
TEAMS = {}
PLAYERS = {}
CHAT_MESSAGES = {}

def create_demo_data():
    # Demo teams and players
    TEAMS['team1'] = {"id": "team1", "name": "Red United"}
    TEAMS['team2'] = {"id": "team2", "name": "Blue City"}
    PLAYERS['player1'] = {"id": "player1", "name": "Alex Star", "team_id": "team1", "goals": 5}
    PLAYERS['player2'] = {"id": "player2", "name": "Ben Quick", "team_id": "team2", "goals": 3}
    # Demo matches
    MATCHES['match1'] = {
        "id": "match1", "home_team": TEAMS['team1'], "away_team": TEAMS['team2'],
        "start_time": (datetime.datetime.now() + datetime.timedelta(minutes=30)).isoformat(),
        "status": "scheduled",  # (scheduled, live, ended)
        "stream_url": "https://example.com/live/stream1"
    }

create_demo_data()
