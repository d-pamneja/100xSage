from API.dependencies import sys,asyncio,discord, commands, DISCORD_BOT_TOKEN,DISCORD_GUILD_ID
from API.utils import search_query
from API.discord.utils import WebsiteButton,is_rate_limited,set_rate_limit,MAX_DISCORD_MESSAGE_LENGTH
from src.dependencies import logging

class DiscordBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
          
    async def on_ready(self):        
        try:
            if not DISCORD_GUILD_ID:
                logging.error("DISCORD_GUILD_ID is not set!")
                return
            
            synced = await self.tree.sync(guild=discord.Object(id=DISCORD_GUILD_ID))
            print(f"Logged in as {self.user.name} with {len(synced)} commands synced to guild {DISCORD_GUILD_ID}")
        except Exception as e:
            logging.error(f"Unexpected error in on_ready: {e}")

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
    

@bot.tree.command(name="sage",description="Search answer from course documents",guild=discord.Object(id=DISCORD_GUILD_ID))
async def answer_query(interaction : discord.Interaction,query : str):
    """Safely send the answer to user question in Discord server"""
    user_id = interaction.user.id
    ttl = await is_rate_limited(user_id)
    
    if ttl:
        embed = discord.Embed(
            title="⏳ Rate Limit Reached!",
            description=f"Please wait {ttl} seconds before using this command again.",
            color=0xE74C3C
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    await set_rate_limit(user_id)
    
    try:
        await interaction.response.defer()
        
        if not query.strip():
            embed = discord.Embed(
                title="❌ Uh-oh! Kindly give a valid input",
                color=0xE74C3C
            )
            
            await interaction.followup.send(embed=embed)
            return True
        else:            
            response = await search_query(query)
            button_view = WebsiteButton("https://app.100xdevs.com")
            
            if(response['status']==200):
                embed = discord.Embed(
                    title = "🚀 All Systems Go: Here's What You Need",
                    description = f"\n\n{response['solution']}\n\n Document : {response['name']}\n\n Pages : {response['reference']}\n\n",
                    color=0x9B59B6
                )
                
                await interaction.followup.send(embed=embed, view=button_view)
                
            elif(response['status']==404):
                embed = discord.Embed(
                    title = "⚠️ Oops, Nothing in the Vault for That!",
                    description = f"\n\n{response['solution']}\n\n",
                    color=0xF1C40F
                )
                
                await interaction.followup.send(embed=embed, view=button_view)
                
            return True
    except discord.HTTPException as e:
        logging.error(f"HTTP Error sending message: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    return False


async def run_discord_bot():
    """Main bot run handler with auto-reconnect"""
    while True:
        try:
            await bot.start(DISCORD_BOT_TOKEN,reconnect=True)
        except discord.ConnectionClosed:
            print("Bot disconnected. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            logging.error(f"Connection failed: {str(e)}")
            await asyncio.sleep(5)
