import math
import asyncio
from scrapers.scrapers import HomeDepot
from utils.product_formatter import format_product_data
from senders.discord_sender import DiscordSender

PAGE_SIZE = 24
CONCURRENT_REQUESTS = 30

class ProductScraper:
    
    def __init__(self) -> None:
        pass
    
    async def products_scraper(self, category_codes: str, base_url: str,
                               is_special_buy: bool = False) -> None:
        home_depot = HomeDepot()
        discord_sender = DiscordSender()
        
        start_index = 0        
        semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

        async def fetch_page_data(category_code, start_index):
            async with semaphore:
                return await home_depot.get_products(category_code=category_code,
                                                     start_index=start_index,
                                                     page_size=PAGE_SIZE,
                                                     base_url=base_url)

        for category_code in category_codes:
            product_data = await fetch_page_data(category_code, start_index)
                                    
            if not product_data:
                return None
            
            total_products = (
                product_data
                .get('data', {})
                .get('searchModel', {})
                .get('searchReport', {})
                .get('totalProducts', 0)
            )

            if not total_products:
                return None
            
            number_of_pages = math.ceil(total_products / PAGE_SIZE)
            tasks = []

            for page in range(number_of_pages):                
                if page > 29:
                    break
                                
                start_index = page * PAGE_SIZE
                tasks.append(fetch_page_data(category_code, start_index))

            # Fetch all pages concurrently
            all_product_data = await asyncio.gather(*tasks)

            for product_data in all_product_data:
                
                if not product_data:
                    continue
                
                for product in product_data['data']['searchModel']['products']:                                    
                    formatted_data = await format_product_data(product_data=product)
                    await discord_sender.send_product_data_to_discord(
                        product_info=formatted_data, is_special_buy=is_special_buy
                    )