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

    @abstractmethod
    def get_update_query(self) -> str:
        """Return SQL query to update existing item."""
        pass

    @abstractmethod
    def extract_update_values(self, item: Dict[str, Any]) -> Tuple:
        """Extract values for update query from item."""
        pass

    def save_items(self, items: List[Dict[str, Any]]) -> int:
        """Generic save method with upsert capability."""
        conn = self.db_manager.get_connection()
        count = 0

        with conn.cursor() as cur:
            items_to_insert = []
            items_to_update = []

            for item in items:
                item_id = self.get_item_id(item)
                if not item_id:
                    continue

                try:
                    cur.execute(self.get_check_query(), (item_id,))
                    existing = cur.fetchone()

                    if not existing:
                        items_to_insert.append(self.extract_insert_values(item))
                    else:
                        items_to_update.append(self.extract_update_values(item))
                        print(f'{self.get_item_name(item)} updated with id {item_id}.')

                    count += 1
                except Exception as e:
                    print(f"Error processing {self.get_item_name(item)}: {e}")

            # Batch operations
            if items_to_insert:
                cur.executemany(self.get_insert_query(), items_to_insert)
            if items_to_update:
                cur.executemany(self.get_update_query(), items_to_update)

            conn.commit()
        return count
