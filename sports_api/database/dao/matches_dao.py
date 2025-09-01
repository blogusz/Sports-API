from typing import List, Dict, Any, Optional, Tuple
from sports_api.database.dao.base_dao import BaseDAO


class MatchesDAO(BaseDAO):
    """Data Access Object for matches table."""

    def get_item_id(self, item: Dict[str, Any]) -> Optional[str]:
        return item.get('idEvent')

    def get_check_query(self) -> str:
        return "SELECT id FROM matches WHERE id = %s"

    def get_insert_query(self) -> str:
        return """
            INSERT INTO matches (id, league_id, season, home_team_id, away_team_id, event_date, home_score, away_score, round_number, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

    def extract_insert_values(self, item: Dict[str, Any]) -> Tuple:
        return (
            item.get('idEvent'),
            item.get('idLeague'),
            item.get('strSeason'),
            item.get('idHomeTeam'),
            item.get('idAwayTeam'),
            item.get('strTimestamp'),
            item.get('intHomeScore'),
            item.get('intAwayScore'),
            item.get('intRound'),
            item.get('strStatus')
        )

    def get_item_name(self, item: Dict[str, Any]) -> str:
        return f"Match {item.get('idEvent')}"

    def save_matches(self, matches: List[Dict[str, Any]]) -> int:
        """Save matches to database."""
        return self.save_items(matches)
