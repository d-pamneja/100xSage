from discord.ui import Button, View
from API.dependencies import discord,timedelta,datetime,redis

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