from discord.ui import Button, View,Select
from API.dependencies import discord,timedelta,datetime,redis,json,aiohttp
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
        
class TopicDropdown(Select):
    def __init__(self, topics, messages, thread):
        self.messages = messages
        self.thread = thread
        
        options = [
            discord.SelectOption(label=topic["title"], value=topic["id"])
            for topic in topics
        ]
        
        super().__init__(placeholder="Select a topic...", options=options)

    async def callback(self, interaction: discord.Interaction):
        topic_id = self.values[0]
        await interaction.response.defer(ephemeral=True)

        async with interaction.channel.typing():
            ticket = await new_ticket(self.messages, self.thread.id)

        if ticket['status'] == 200:
            summary = json.loads(ticket['content'])
            title = summary.get('title', 'No Title')
            description = summary.get('description', 'No Description')
            
            async with aiohttp.ClientSession() as session: 
                async with session.post(f"http://localhost:3001/backend/v1/ticket/createTicket",json = {'thread_id' : int(ticket['thread_id']),'title' : title, 'description' : description, 'topic_id' : int(topic_id)}) as resp:
                    
                    if resp.status == 201:  
                        await interaction.followup.send(f"✅ Ticket created", ephemeral=True)
                    else:
                        await interaction.followup.send("❌ Failed to create ticket.", ephemeral=True)
        else:
            await interaction.followup.send("❌ Failed to create ticket.", ephemeral=True)


class TicketDropdownView(View):
    def __init__(self, topics, messages, thread):
        super().__init__(timeout=60)
        self.add_item(TopicDropdown(topics, messages, thread))


class TicketButton(discord.ui.View):
    def __init__(self, thread_creator_id: int, course_id: int):
        super().__init__(timeout=None)
        self.thread_creator_id = thread_creator_id
        self.course_id = course_id 

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

        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://localhost:3001/backend/v1/topic/getTopics?courseID={self.course_id}") as resp:
                if resp.status != 200:
                    await interaction.followup.send("❌ Failed to fetch topics.", ephemeral=True)
                    return

                response = await resp.json()
                topics = response['response']

            if not topics:
                await interaction.followup.send("❌ No topics available.", ephemeral=True)
                return

            messages = []
            async for msg in thread.history(limit=None, oldest_first=True):
                if not msg.author.bot:
                    messages.append({"user": msg.author.display_name, "content": msg.content})

            await interaction.followup.send("Select a topic for your ticket:", view=TicketDropdownView(topics, messages, thread), ephemeral=True)
        return