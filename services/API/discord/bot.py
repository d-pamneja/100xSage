from API.dependencies import sys,asyncio, discord, commands, DISCORD_BOT_TOKEN
from src.dependencies import logging

class DiscordBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def on_ready(self):
        print(f"Logged in as {self.user.name}")

    async def send_thread_message(self, thread_id: int, message: str = None, embed: discord.Embed = None, view: discord.ui.View = None):
        """Safely send a message, embed, or button to a Discord thread."""
        try:
            thread = self.get_channel(thread_id)
            if not thread:
                thread = await self.fetch_channel(thread_id)

            if thread and isinstance(thread, discord.Thread):
                if not thread.archived:
                    await thread.send(content=message, embed=embed, view=view)
                    logging.info(f"Message sent to thread {thread_id}")
                    return True
                else:
                    logging.warning(f"Thread {thread_id} is archived, cannot send message.")
                    return False
            else:
                logging.error(f"Thread {thread_id} not found or invalid.")
                return False

        except discord.HTTPException as e:
            logging.error(f"HTTP Error sending message: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        return False


intents = discord.Intents.all()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = DiscordBot(command_prefix="!", intents=intents)

@bot.event
async def on_error(event, *args, **kwargs):
    logging.error(f"Discord event error in {event}: {sys.exc_info()}")

async def run_discord_bot():
    """Main bot run handler"""
    try:
        await bot.start(DISCORD_BOT_TOKEN)
    except Exception as e:
        logging.error(f"Connection failed: {str(e)}")
        await asyncio.sleep(5)