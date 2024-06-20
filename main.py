import asyncio
from scrapers.scrapers import HomeDepot


home_depot = HomeDepot()

async def main():
    await home_depot.extract_user_agents("https://www.useragents.me/")


asyncio.run(main())