from typing import List, Dict, Any, Optional, Tuple
from sports_api.database.dao.base_dao import BaseDAO


class PlayersDAO(BaseDAO):
    """Data Access Object for players table."""

    def get_item_id(self, item: Dict[str, Any]) -> Optional[str]:
        return item.get('idPlayer')

    def get_check_query(self) -> str:
        return "SELECT id FROM players WHERE id = %s"

    def get_insert_query(self) -> str:
        return """
            INSERT INTO players (id, name, team_id, nationality, date_born, position, height, weight, jersey_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

    def extract_insert_values(self, item: Dict[str, Any]) -> Tuple:
        return (
            item.get('idPlayer'),
            item.get('strPlayer'),
            item.get('idTeam'),
            item.get('strNationality'),
            item.get('dateBorn'),
            item.get('strPosition'),
            item.get('strHeight'),
            item.get('strWeight'),
            item.get('strNumber')
        )

    def get_item_name(self, item: Dict[str, Any]) -> str:
        return f"Player {item.get('strPlayer')}"

    def get_update_query(self) -> str:
        return """
            UPDATE players SET name = %s, team_id = %s, nationality = %s, 
                   date_born = %s, position = %s, height = %s, weight = %s, 
                   jersey_number = %s WHERE id = %s
        """

    def extract_update_values(self, item: Dict[str, Any]) -> Tuple:
        return (
            item.get('strPlayer'),
            item.get('idTeam'),
            item.get('strNationality'),
            item.get('dateBorn'),
            item.get('strPosition'),
            item.get('strHeight'),
            item.get('strWeight'),
            item.get('strNumber'),
            item.get('idPlayer')  # WHERE clause - ID goes last
        )

    def save_players(self, players: List[Dict[str, Any]]) -> int:
        """Save players to database."""
        return self.save_items(players)
