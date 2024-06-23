import asyncio
from tasks.all_products_task import AllProducts
from tasks.discord_task import run_discord_task
from tasks.online_clearance_task import OnlineClearance
from utils.run_once import Categories

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

# categ = Categories()
# from database.database import Database
# async def main():
#     database = Database()
    
#     category_paths = ["./data/categories.json", "./data/category_special_buy.json"]
    
    
#     ct_1 = await categ.read_categories(
#         category_path=category_paths[0]
#     )
#     await database.add_categories_zip_in_store(ct_1)
    
#     ct_2 = await categ.read_categories(
#         category_path=category_paths[1]
#     )
#     await database.add_special_buy(ct_2)
    
# if __name__ == "__main__":
#     asyncio.run(main())
    