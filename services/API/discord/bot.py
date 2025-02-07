from API.dependencies import websockets, asyncio, discord,commands
from src.dependencies import logging

class DiscordMessageSender:
    def __init__(self, token, intents=None):
        """
        Initialize Discord bot for sending messages
        
            :param token: Discord bot token
            :param intents: Discord intents (optional)
        """
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.messages = True
            intents.guilds = True
            intents.members = True

        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.token = token
        self._ready = asyncio.Event()  # Add a ready event
        
        @self.bot.event
        async def on_ready():
            print(f'Logged in as {self.bot.user.name}')
            self._ready.set()  # Signal that the bot is ready
        

    async def send_thread_message(self, thread_id, message):
        """
        Send a message to a specific thread
        
        :param thread_id: ID of the thread to send message to
        :param message: Message content to send
        :return: True if message sent successfully, False otherwise
        """
        try:
            thread = await self.bot.fetch_channel(int(thread_id))
            
            if thread is None:
                logging.error(f"Could not find thread with ID: {thread_id}")
                return False
            
            await thread.send(message)
            logging.info(f"Message sent to thread {thread_id}")
            return True
        
        except discord.HTTPException as e:
            logging.error(f"Failed to send message to thread {thread_id}: {e}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error sending message: {e}")
            return False

    async def start_bot(self):
        """
        Start the Discord bot
        """
        try:
            await self.bot.start(self.token)
        except Exception as e:
            logging.error(f"Failed to start Discord bot: {e}")

    def run(self):
        """
        Run the bot synchronously
        """
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.start_bot())
        except Exception as e:
            logging.error(f"Bot run failed: {e}")
            
