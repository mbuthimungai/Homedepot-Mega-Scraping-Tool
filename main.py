import asyncio
from tasks.all_products_task import AllProducts
from senders.discord_sender import DiscordSender

all_products = AllProducts()

async def main():
    """This is the main entry point"""
        
    all_product_task = asyncio.create_task(all_products.all_products_scraper())
    
    asyncio.gather(all_product_task,
                   )
    