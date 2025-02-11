from discord.ui import Button, View
from API.dependencies import discord,timedelta,datetime,redis
from src.workers.tickets.utils import new_ticket

redisClient = redis.Redis(host = 'localhost',port = 6379, db = 0, decode_responses = True)
RATE_LIMIT = 120
MAX_DISCORD_MESSAGE_LENGTH = 2000

async def is_rate_limited(user_id : int) -> bool:
    """Function to check if a user is still under rate limit"""
    
    key = f"user_rate_limit:{user_id}"
    ttl = redisClient.ttl(key)
    
    if(ttl>0):
        return ttl

    return False

async def set_rate_limit(user_id: int):
    """Set a rate limit for the user with expiration"""
    key = f"user_rate_limit:{user_id}"
    redisClient.setex(key, RATE_LIMIT, datetime.now().isoformat())

class ThreadButton(View):
    def __init__(self, thread_link: str):
        super().__init__()
        self.add_item(Button(label="🔗 View Discussion", url=thread_link, style=discord.ButtonStyle.link))
        
class WebsiteButton(View):
    def __init__(self, website_link: str):
        super().__init__()
        self.add_item(Button(label="🌐 Visit 100xDevs", url=website_link, style=discord.ButtonStyle.link))
        
class TicketButton(discord.ui.View):
    def __init__(self, thread_creator_id: int):
        super().__init__(timeout=None)
        self.thread_creator_id = thread_creator_id  # Store thread creator's ID

    @discord.ui.button(label="Raise Ticket", style=discord.ButtonStyle.blurple, custom_id="raise_ticket_button")
    async def raise_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        thread = interaction.channel 

        if not isinstance(thread, discord.Thread):
            await interaction.response.send_message("This can only be used inside a thread.", ephemeral=True)
            return

        if interaction.user.id != self.thread_creator_id:
            await interaction.response.send_message("Only the thread creator can raise a ticket.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True) 

        messages = []
        async for msg in thread.history(limit=None, oldest_first=True):  
            if msg.author.bot == True :
                continue
            else :
                entry = {}
                entry["user"] = msg.author.display_name
                entry["content"] = msg.content
                
                messages.append(entry)

        async with interaction.channel.typing():
            thread_id = thread.id
            ticket = await new_ticket(messages,thread_id)
            await interaction.followup.send(f"✅ Ticket raised successfully! Expect a response soon...", ephemeral=True)