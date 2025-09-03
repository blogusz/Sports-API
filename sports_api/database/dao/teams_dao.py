from typing import List, Dict, Any, Optional, Tuple
from sports_api.database.dao.base_dao import BaseDAO


class TeamsDAO(BaseDAO):
    """Data Access Object for teams table."""

    def get_item_id(self, item: Dict[str, Any]) -> Optional[str]:
        return item.get('idTeam')

    def get_check_query(self) -> str:
        return "SELECT id FROM teams WHERE id = %s"

    def get_insert_query(self) -> str:
        return """
            INSERT INTO teams (id, name, alternate_names, short_name, foundation_year, sport, league_id, venue_id, location, country_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

    def extract_insert_values(self, item: Dict[str, Any]) -> Tuple:
        return (
            item.get('idTeam'),
            item.get('strTeam'),
            item.get('strTeamAlternate'),
            item.get('strTeamShort'),
            item.get('intFormedYear'),
            item.get('strSport'),
            item.get('idLeague'),
            item.get('idVenue'),
            item.get('strLocation'),
            item.get('strCountry')
        )

    def get_item_name(self, item: Dict[str, Any]) -> str:
        return f"Team {item.get('strTeam')}"

    def save_teams(self, teams: List[Dict[str, Any]]) -> int:
        """Save teams to database."""
        return self.save_items(teams)
