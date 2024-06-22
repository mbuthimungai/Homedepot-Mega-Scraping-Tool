import asyncio
from tasks.all_products_task import AllProducts
from tasks.discord_task import run_discord_task
from tasks.online_clearance_task import OnlineClearance

all_products = AllProducts()
online_clearance = OnlineClearance()


async def main():
    """This is the main entry point"""
        
    all_product_task = asyncio.create_task(
        all_products.get_product_online_instore())
    discord_task = asyncio.create_task(
        run_discord_task())
    online_clearance_task = asyncio.create_task(
        online_clearance.get_online_clearance_products()
    )
    asyncio.gather(
        discord_task,
        all_product_task,
        online_clearance_task
        )
    