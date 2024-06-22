import discord, json, os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

MY_TOKEN = os.getenv("MY_TOKEN")
intents = discord.Intents.default()
intents.members = True
intents.presences = True  # If you need Presence Intent
intents.message_content = True
client = discord.Client(intents = intents)


CHANNEL_IDS_MAPPING = {
    "90_100_HD_ZIP": "1225561503147622612",
    "80_89_HD_ZIP": "1225561473426653295",
    "70_79_HD_ZIP": "1225561424303231060",
    "1_69_HD_ZIP": "1225561328140423250",
    "90_100_HD_IN_STORE": "1253735628177408101",
    "80_89_HD_IN_STORE": "1253735724998463588",
    "70_79_HD_IN_STORE": "1253735755222745170",
    "1_69_HD_IN_STORE": "1253735800617566330",
    "90_100_HD_ONLINE": "1253735931807141970",
    "80_89_HD_ONLINE": "1253735967211262053",
    "70_79_HD_ONLINE": "1253735999499141262",
    "1_69_HD_ONLINE": "1253736044839309455"
}
    
    
class DiscordSender:
    def __init__(self) -> None:
        pass

    # Bot event on ready
    @client.event
    async def on_ready(self):
        print(f'Logged in as {client.user.name}')
                
    async def run_discord_bot(self):
        # Run the bot
        client.start(os.getenv('DISCORD_TOKEN'))
        
    
    # async def find_discount_channel(self, product_info: dict, is_special_buy: bool) -> discord.channel.TextChannel:
    #     channel = ""
    #     if is_special_buy:
    #         if 90 <= product_info['discount'] <= 100:
    #             channel = client.get_channel(int(CHANNEL_IDS_MAPPING['90_100_HD_ONLINE']))
    #         if 80 <= product_info['discount'] <= 89:
    #             channel = client.get_channel(int(CHANNEL_IDS_MAPPING['80_89_HD_ONLINE']))
    #         if 70 <= product_info['discount'] <= 79:
    #             channel = client.get_channel(int(CHANNEL_IDS_MAPPING['70_79_HD_ONLINE']))
    #         if 0 <= product_info['discount'] <= 69:
    #             channel = client.get_channel(int(CHANNEL_IDS_MAPPING['1_69_HD_ONLINE']))
    #     elif product_info['service_type'] == "bopis":
    #         if 90 <= product_info['discount'] <= 100:
    #             channel = client.get_channel(int(CHANNEL_IDS_MAPPING['90_100_HD_IN_STORE']))
    #         if 80 <= product_info['discount'] <= 89:
    #             channel = client.get_channel(int(CHANNEL_IDS_MAPPING['80_89_HD_IN_STORE']))
    #         if 70 <= product_info['discount'] <= 79:
    #             channel = client.get_channel(int(CHANNEL_IDS_MAPPING['70_79_HD_IN_STORE']))
    #         if 0 <= product_info['discount'] <= 69:
    #             channel = client.get_channel(int(CHANNEL_IDS_MAPPING['1_69_HD_IN_STORE']))
    #     elif product_info['service_type'] == "boss":
    #         if 90 <= product_info['discount'] <= 100:
    #             channel = client.get_channel(int(CHANNEL_IDS_MAPPING['90_100_HD_ZIP']))
    #         if 80 <= product_info['discount'] <= 89:
    #             channel = client.get_channel(int(CHANNEL_IDS_MAPPING['80_89_HD_ZIP']))
    #         if 70 <= product_info['discount'] <= 79:
    #             channel = client.get_channel(int(CHANNEL_IDS_MAPPING['70_79_HD_ZIP']))            
    #         if 0 <= product_info['discount'] <= 69:
    #             channel = client.get_channel(int(CHANNEL_IDS_MAPPING['1_69_HD_ZIP']))
    #     return channel
    
    async def find_discount_channel(self, product_info: dict, is_special_buy: bool) -> discord.channel.TextChannel:
        # Define channel ID mappings for each service type and discount range
        discount_channels = {
            "special_buy": {
                (90, 100): '90_100_HD_ONLINE',
                (80, 89): '80_89_HD_ONLINE',
                (70, 79): '70_79_HD_ONLINE',
                (0, 69): '1_69_HD_ONLINE',
            },
            "bopis": {
                (90, 100): '90_100_HD_IN_STORE',
                (80, 89): '80_89_HD_IN_STORE',
                (70, 79): '70_79_HD_IN_STORE',
                (0, 69): '1_69_HD_IN_STORE',
            },
            "boss": {
                (90, 100): '90_100_HD_ZIP',
                (80, 89): '80_89_HD_ZIP',
                (70, 79): '70_79_HD_ZIP',
                (0, 69): '1_69_HD_ZIP',
            }
        }
        
        # Determine the appropriate discount channel mapping based on service type
        service_type = 'special_buy' if is_special_buy else product_info.get('service_type')
        discount = product_info.get('discount')
        
        # Find the appropriate channel ID based on the discount range
        channel_id = None
        for discount_range, channel_key in discount_channels.get(service_type, {}).items():
            if discount_range[0] <= discount <= discount_range[1]:
                channel_id = CHANNEL_IDS_MAPPING.get(channel_key)
                break
    
        # Return the corresponding Discord channel or None if not found
        if channel_id:
            return client.get_channel(int(channel_id))
        return None

    
    async def create_embed(self, product_info: dict) -> discord.Embed:
        embed = discord.Embed(
            title=product_info['product_name'],
            url=product_info['product_link'],
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url=product_info['product_image_url'])        
        embed.add_field(name="New Price", value=f"${product_info['value']:.2f}", inline=True)
        embed.add_field(name="Retail Price", value=f"${product_info['original']:.2f}", inline=True)
        embed.add_field(name="Discount", value=f"{product_info['discount']}%", inline=True)
        # embed.add_field(name="Service Type", value=product_info['service_type'], inline=False)
        embed.add_field(name="Product ID", value=product_info['product_id'], inline=False)
        
        return embed

        # embed.add_field(name="In Stock", value=str(product_info['is_in_stock']), inline=True)
        # embed.add_field(name="Limited Quantity", value=str(product_info['is_limited_quantity']), inline=True)
        
        
    async def send_product_data_to_discord(self, product_info: dict, is_special_buy: bool = False) -> None:
        channel = await self.find_discount_channel(
            product_info=product_info)
        if channel:
            embed = await self.create_embed(product_info=product_info)            
            channel.send(embed=embed)
        

        