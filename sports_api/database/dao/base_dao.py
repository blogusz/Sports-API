from typing import List, Dict, Any, Tuple, Optional
from abc import ABC, abstractmethod
from sports_api.database.db_manager import DatabaseManager


class BaseDAO(ABC):
    """Base DAO class with common database operations."""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    @abstractmethod
    def get_item_id(self, item: Dict[str, Any]) -> Optional[str]:
        """Extract the ID from an item. Return None if invalid."""
        pass

    @abstractmethod
    def get_check_query(self) -> str:
        """Return SQL query to check if item exists."""
        pass

    @abstractmethod
    def get_insert_query(self) -> str:
        """Return SQL query to insert new item."""
        pass

    @abstractmethod
    def extract_insert_values(self, item: Dict[str, Any]) -> Tuple:
        """Extract values for insert query from item."""
        pass

    @abstractmethod
    def get_item_name(self, item: Dict[str, Any]) -> str:
        """Get item name for logging purposes."""
        pass

    def save_items(self, items: List[Dict[str, Any]]) -> int:
        """Generic save method for all DAOs."""
        conn = self.db_manager.get_connection()
        count = 0

        with conn.cursor() as cur:
            for item in items:
                item_id = self.get_item_id(item)
                if not item_id:
                    continue

                try:
                    # Check if exists
                    cur.execute(self.get_check_query(), (item_id,))
                    existing = cur.fetchone()

                    if not existing:
                        values = self.extract_insert_values(item)
                        cur.execute(self.get_insert_query(), values)
                    else:
                        print(f'{self.get_item_name(item)} already exists with id {item_id}.')

                    count += 1
                except Exception as e:
                    print(f"Error saving {self.get_item_name(item)}: {e}")

            conn.commit()
        return count
