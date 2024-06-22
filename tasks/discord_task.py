from senders.discord_sender import DiscordSender


discord_sender = DiscordSender()

async def run_discord_task():
    await discord_sender.run_discord_bot()