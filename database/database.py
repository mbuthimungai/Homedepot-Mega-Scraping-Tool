from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

from utils.logger import get_logger


logger = get_logger()

# Load environment variables from a .env file
load_dotenv()

# Retrieve the MongoDB connection string from the environment variable
MONGODB_URL_REMOTE = os.getenv("MONGODB_URL_REMOTE")

# Create the MongoDB client
client = AsyncIOMotorClient(MONGODB_URL_REMOTE)
db = client.homeDepotDb

store_clearance_collection = db.store_clearance
special_buy_collection = db.special_buy

class Database:
    def __init__(self) -> None:
        pass
    
    async def add_categories_zip_in_store(self, categories: dict) -> None:
        """
        Adds Zip Code: (Online Purchase) & In-store Clearance: (In-store purchaseable) links to the store_clearance collection.

        Args:
            categories (dict): A dictionary containing the categories and their respective links to be added to the store_clearance collection.

        This method inserts multiple documents into the store_clearance collection in a single operation. The `categories` dictionary
        should be structured such that each key-value pair represents a category and its corresponding link.
        """
        try:
            await store_clearance_collection.insert_many(categories)
            logger.info(f"Inserted {len(categories)} categories into store_clearance collection.")
        except Exception as e:
            logger.error(f"An error occurred while adding categories to store_clearance collection: {e}")

    async def add_special_buy(self, categories: dict) -> None:
        """
        Adds Online Clearance: Special Buys links to the special_buy collection.

        Args:
            categories (dict): A dictionary containing the categories and their respective links to be added to the special_buy collection.

        This method inserts multiple documents into the special_buy collection in a single operation. The `categories` dictionary
        should be structured such that each key-value pair represents a category and its corresponding link.
        """
        try:
            await special_buy_collection.insert_many(categories)
            logger.info(f"Inserted {len(categories)} categories into special_buy collection.")
        except Exception as e:
            logger.error(f"An error occurred while adding categories to special_buy collection: {e}")

    async def get_special_buy_category(self) -> list:
        """
        Retrieves all categories from the special_buy collection where 'is_complete' is False.

        Returns:
            list: A list of documents from the special_buy collection where the 'is_complete' field is False.

        This method queries the special_buy collection for documents where the 'is_complete' field is set to False,
        indicating that these tasks are not yet complete. It returns the resulting documents as a list.
        """
        try:
            cursor = special_buy_collection.find({"is_complete": False})
            documents = await cursor.to_list(length=None)
            logger.info(f"Retrieved {len(documents)} incomplete categories from special_buy collection.")
            return documents
        except Exception as e:
            logger.error(f"An error occurred while retrieving incomplete categories from special_buy collection: {e}")
            return []

    async def get_store_clearance_codes(self) -> list:
        """
        Retrieves all categories from the store_clearance collection where 'is_complete' is False.

        Returns:
            list: A list of documents from the store_clearance collection where the 'is_complete' field is False.

        This method queries the store_clearance collection for documents where the 'is_complete' field is set to False,
        indicating that these tasks are not yet complete. It returns the resulting documents as a list.
        """
        try:
            cursor = store_clearance_collection.find({"is_complete": False})
            documents = await cursor.to_list(length=None)
            logger.info(f"Retrieved {len(documents)} incomplete categories from store_clearance collection.")
            return documents
        except Exception as e:
            logger.error(f"An error occurred while retrieving incomplete categories from store_clearance collection: {e}")
            return []

    
    async def update_special_buy_category(self, task_id: str) -> None:
        """
        Mark a task in the special_buy collection as complete.

        Args:
            task_id (str): The ID of the task to update.

        This method sets the `is_complete` field to True for the specified task in the special_buy collection.
        """
        try:
            result = await self.special_buy_collection.update_one(
                {"_id": task_id},
                {"$set": {"is_complete": True}}
            )
            if result.matched_count:
                logger.info(f"Task with id {task_id} updated successfully in special_buy collection.")
            else:
                logger.warning(f"No task found with id {task_id} in special_buy collection.")
        except Exception as e:
            logger.error(f"An error occurred while updating the task with id {task_id} in special_buy collection: {e}")

    async def update_store_clearance_category(self, task_id: str) -> None:
        """
        Mark a task in the store_clearance collection as complete.

        Args:
            task_id (str): The ID of the task to update.

        This method sets the `is_complete` field to True for the specified task in the store_clearance collection.
        """
        try:
            result = await self.store_clearance_collection.update_one(
                {"_id": task_id},
                {"$set": {"is_complete": True}}
            )
            if result.matched_count:
                logger.info(f"Task with id {task_id} updated successfully in store_clearance collection.")
            else:
                logger.warning(f"No task found with id {task_id} in store_clearance collection.")
        except Exception as e:
            logger.error(f"An error occurred while updating the task with id {task_id} in store_clearance collection: {e}")

    async def update_store_clearance_category_page(self, task_id: str, page_num: int) -> None:
        """
        Update the page number for a task in the store_clearance collection.

        Args:
            task_id (str): The ID of the task to update.
            page_num (int): The page number to set.

        This method sets the `page` field to the specified page number for the specified task in the store_clearance collection.
        """
        try:
            result = await self.store_clearance_collection.update_one(
                {"_id": task_id},
                {"$set": {"page": page_num}}
            )
            if result.matched_count:
                logger.info(f"Task with id {task_id} updated successfully in store_clearance collection with page number {page_num}.")
            else:
                logger.warning(f"No task found with id {task_id} in store_clearance collection.")
        except Exception as e:
            logger.error(f"An error occurred while updating the task with id {task_id} in store_clearance collection: {e}")

    async def update_special_buy_category_page(self, task_id: str, page_num: int) -> None:
        """
        Update the page number for a task in the special_buy collection.

        Args:
            task_id (str): The ID of the task to update.
            page_num (int): The page number to set.

        This method sets the `page` field to the specified page number for the specified task in the special_buy collection.
        """
        try:
            result = await self.special_buy_collection.update_one(
                {"_id": task_id},
                {"$set": {"page": page_num}}
            )
            if result.matched_count:
                logger.info(f"Task with id {task_id} updated successfully in special_buy collection with page number {page_num}.")
            else:
                logger.warning(f"No task found with id {task_id} in special_buy collection.")
        except Exception as e:
            logger.error(f"An error occurred while updating the task with id {task_id} in special_buy collection: {e}")
