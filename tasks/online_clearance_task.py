import json
from utils.product_scraper import ProductScraper

BASE_URL = "https://www.homedepot.com/federation-gateway/graphql?opname=searchModel"

class OnlineClearance:
    def __init__(self) -> None:
        pass
    
    async def read_categories(self) -> list:
        category_links = []
        
        with open('./data/category_special_buy.json', 'r') as file:
            category_links = json.load(file)
        
        category_codes = [category_link.strip().split("/")[-1] for category_link in category_links]
        
        return category_codes
    
    async def get_online_clearance_products(self, ):
        product_scraper = ProductScraper()
        
        category_codes = await self.read_categories()
        await product_scraper.products_scraper(
            category_codes=category_codes, base_url=BASE_URL,
            is_special_buy=True)
        