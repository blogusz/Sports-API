import uuid
from typing import List, Dict, Any, Optional, Tuple
from sports_api.database.dao.base_dao import BaseDAO


class CountriesDAO(BaseDAO):
    """Data Access Object for countries table."""

    def get_item_id(self, item: Dict[str, Any]) -> Optional[str]:
        return item.get('name_en')

    def get_check_query(self) -> str:
        return "SELECT id FROM countries WHERE name = %s"

    def get_insert_query(self) -> str:
        return "INSERT INTO countries (id, name) VALUES (%s, %s)"

    def extract_insert_values(self, item: Dict[str, Any]) -> Tuple:
        country_id = str(uuid.uuid4())
        country_name = item.get('name_en')
        return (country_id, country_name)

    def get_item_name(self, item: Dict[str, Any]) -> str:
        return f"Country {item.get('name_en')}"

    def get_update_query(self) -> str:
        raise NotImplementedError("Countries do not support updates")

    def extract_update_values(self, item: Dict[str, Any]) -> Tuple:
        raise NotImplementedError("Countries do not support updates")

    def save_countries(self, countries: List[Dict[str, Any]]) -> int:
        """Save countries to database."""
        return self.save_items(countries)
