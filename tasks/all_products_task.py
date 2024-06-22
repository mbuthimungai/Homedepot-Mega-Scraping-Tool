# import json
# import math
# import asyncio
# from scrapers.scrapers import HomeDepot

# PAGE_SIZE = 24

# class AllProducts:
    
#     def __init__(self) -> None:
#         pass
    
#     async def read_categories(self, ) -> list:
#         category_links = []
        
#         with open('./data/categories.json', 'r') as file:
#             category_links = json.load(file)
        
#         category_codes = [category_link.strip().split("/")[-1] for category_link in category_links]
        
#         return category_codes
            
#     async def all_products_scraper(self):
#         home_depot = HomeDepot()
#         start_index = 0        
#         category_codes = await self.read_categories()
        
#         async def fetch_page_data(category_code, start_index):
#             return await home_depot.get_products(category_code=category_code,
#                                                  start_index=start_index,
#                                                  page_size=PAGE_SIZE)

#         for category_code in category_codes:
#             product_data = await fetch_page_data(category_code, start_index)
                                    
#             if not product_data:
#                 return None
            
#             total_products = (
#                 product_data
#                 .get('data', {})
#                 .get('searchModel', {})
#                 .get('searchReport', {})
#                 .get('totalProducts', 0)
#             )

#             if not total_products:
#                 return None
            
#             number_of_pages = math.ceil(total_products / PAGE_SIZE)
#             tasks = []

#             for page in range(number_of_pages):
#                 start_index = page * PAGE_SIZE
#                 tasks.append(fetch_page_data(category_code, start_index))

#             # Fetch all pages concurrently
#             all_product_data = await asyncio.gather(*tasks)

#             for product_data in all_product_data:
                
#                 if not product_data:
#                     continue
                
#                 for product in product_data['data']['searchModel']['products']:                                    
#                     formatted_data = await self.format_product_data(
#                         product_data=product)
                    
                
                
                
            
#     async def format_product_data(self, product_data: dict) -> dict:
#         product_info = {
#             "product_name": "",
#             "value": 0,
#             "original": 0,
#             "product_id": "",
#             "product_image_url": "",
#             "product_link": "",
#             "is_in_stock": True,
#             "is_limited_quantity": False,
#             "service_type": ""
#         }

#         # Get image sizes safely
#         image_sizes = product_data.get('media', {}).get('images', [{}])[0].get('sizes', [])

#         # Populate product_info with values using .get() method
#         product_info['product_name'] = product_data.get('identifiers', {}).get('productLabel', '')
#         product_info['product_link'] = 'https://www.homedepot.com' + product_data.get('identifiers', {}).get('canonicalUrl', '')
#         product_info['product_id'] = product_data.get('itemId', '')
#         product_info['product_image_url'] = product_data.get('media', {}).get('images', [{}])[0].get('url', '').replace("<SIZE>", image_sizes[-1] if image_sizes else '')
#         product_info['value'] = product_data.get('pricing', {}).get('value', 0)
#         product_info['original'] = product_data.get('pricing', {}).get('original', 0)
#         product_info['service_type'] = product_data.get('fulfillment', {}).get('fulfillmentOptions', [{}])[0].get('services', [{}])[0].get('type', '')
#         product_info['is_in_stock'] = product_data.get('fulfillment', {}).get('fulfillmentOptions', [{}])[0].get('services', [{}])[0].get('locations', [{}])[0].get('inventory', {}).get('isInStock', True)
#         product_info['is_limited_quantity'] = product_data.get('fulfillment', {}).get('fulfillmentOptions', [{}])[0].get('services', [{}])[0].get('locations', [{}])[0].get('inventory', {}).get('isLimitedQuantity', False)

#         return product_info

            
            
import json
import math
import asyncio
from scrapers.scrapers import HomeDepot
from utils.discount_handler import DiscountHandler
from senders.discord_sender import DiscordSender

PAGE_SIZE = 24
CONCURRENT_REQUESTS = 30

class AllProducts:
    
    def __init__(self) -> None:
        pass
    
    async def read_categories(self) -> list:
        category_links = []
        
        with open('./data/categories.json', 'r') as file:
            category_links = json.load(file)
        
        category_codes = [category_link.strip().split("/")[-1] for category_link in category_links]
        
        return category_codes
            
    async def all_products_scraper(self):
        home_depot = HomeDepot()
        discord_sender = DiscordSender()
        
        start_index = 0        
        category_codes = await self.read_categories()
        semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

        async def fetch_page_data(category_code, start_index):
            async with semaphore:
                return await home_depot.get_products(category_code=category_code,
                                                     start_index=start_index,
                                                     page_size=PAGE_SIZE)

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
                    formatted_data = await self.format_product_data(product_data=product)
                    await discord_sender.send_product_data_to_discord(
                        product_info=formatted_data
                    )
                    
                    
    async def format_product_data(self, product_data: dict) -> dict:
        discount_handler = DiscountHandler()
        product_info = {
            "product_name": "",
            "value": 0,
            "original": 0,
            "product_id": "",
            "product_image_url": "",
            "product_link": "",
            "is_in_stock": True,
            "is_limited_quantity": False,
            "service_type": "",
            "discount": 0
        }

        # Get image sizes safely
        image_sizes = product_data.get('media', {}).get('images', [{}])[0].get('sizes', [])

        # Populate product_info with values using .get() method
        product_info['product_name'] = product_data.get('identifiers', {}).get('productLabel', '')
        product_info['product_link'] = 'https://www.homedepot.com' + product_data.get('identifiers', {}).get('canonicalUrl', '')
        product_info['product_id'] = product_data.get('itemId', '')
        product_info['product_image_url'] = product_data.get('media', {}).get('images', [{}])[0].get('url', '').replace("<SIZE>", image_sizes[-1] if image_sizes else '')
        product_info['value'] = product_data.get('pricing', {}).get('value', 0)
        product_info['original'] = product_data.get('pricing', {}).get('original', 0)
        product_info['service_type'] = product_data.get('fulfillment', {}).get('fulfillmentOptions', [{}])[0].get('services', [{}])[0].get('type', '')
        product_info['is_in_stock'] = product_data.get('fulfillment', {}).get('fulfillmentOptions', [{}])[0].get('services', [{}])[0].get('locations', [{}])[0].get('inventory', {}).get('isInStock', True)
        product_info['is_limited_quantity'] = product_data.get('fulfillment', {}).get('fulfillmentOptions', [{}])[0].get('services', [{}])[0].get('locations', [{}])[0].get('inventory', {}).get('isLimitedQuantity', False)
        product_info['discount'] = await discount_handler.find_product_discount(
            prev_price=product_info['original'], curr_price=product_info['value']
        )
        return product_info
