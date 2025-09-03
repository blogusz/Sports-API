from typing import List, Dict, Any, Optional, Tuple
from sports_api.database.dao.base_dao import BaseDAO


class LeaguesDAO(BaseDAO):
    """Data Access Object for leagues table."""

    def get_item_id(self, item: Dict[str, Any]) -> Optional[str]:
        return item.get('idLeague')

    def get_check_query(self) -> str:
        return "SELECT id FROM leagues WHERE id = %s"

    def get_insert_query(self) -> str:
        return "INSERT INTO leagues (id, name, sport, alternate_name) VALUES (%s, %s, %s, %s)"

    def extract_insert_values(self, item: Dict[str, Any]) -> Tuple:
        league_id = item.get('idLeague')
        league_name = item.get('strLeague')
        sport = item.get('strSport')
        alternate_names = item.get('strLeagueAlternate')
        return (league_id, league_name, sport, alternate_names)

    def get_item_name(self, item: Dict[str, Any]) -> str:
        return f"League {item.get('strLeague')}"

    def get_update_query(self) -> str:
        return """
            UPDATE leagues SET name = %s, sport = %s, alternate_name = %s WHERE id = %s
        """

    def extract_update_values(self, item: Dict[str, Any]) -> Tuple:
        return (
            item.get('strLeague'),
            item.get('strSport'),
            item.get('strLeagueAlternate'),
            item.get('idLeague')  # WHERE clause - ID goes last
        )

    def save_leagues(self, leagues: List[Dict[str, Any]]) -> int:
        """Save leagues to database."""
        return self.save_items(leagues)
