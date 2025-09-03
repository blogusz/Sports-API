from typing import List, Dict, Any, Optional, Tuple
from sports_api.database.dao.base_dao import BaseDAO


class VenuesDAO(BaseDAO):
    """Data Access Object for venues table."""

    def get_item_id(self, item: Dict[str, Any]) -> Optional[str]:
        return item.get('idVenue')

    def get_check_query(self) -> str:
        return "SELECT id FROM venues WHERE id = %s"

    def get_insert_query(self) -> str:
        return """
            INSERT INTO venues (id, name, alternate_names, sport, capacity, country_name, location, foundation_year)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

    def extract_insert_values(self, item: Dict[str, Any]) -> Tuple:
        return (
            item.get('idVenue'),
            item.get('strVenue'),
            item.get('strVenueAlternate'),
            item.get('strSport'),
            item.get('intCapacity'),
            item.get('strCountry'),
            item.get('strLocation'),
            item.get('intFormedYear')
        )

    def get_item_name(self, item: Dict[str, Any]) -> str:
        return f"Venue {item.get('strVenue')}"

    def save_venues(self, venues: List[Dict[str, Any]]) -> int:
        """Save venues to database."""
        return self.save_items(venues)
