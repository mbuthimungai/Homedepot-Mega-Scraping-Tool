import json
import asyncio

class Categories:
    def __init__(self) -> None:
        pass
    
    async def read_categories(self, category_path: str) -> dict:
        """Read categories and save them a dict"""
        
        categories = []
        with open(category_path, "r") as file:
            categories = json.load(file)
            
        categories = [{"category": category.strip().split("/")[-1],
                       "is_complete": False} for category in categories]
            
        return categories
    

