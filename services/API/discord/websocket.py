from API.dependencies import discord,random,websockets, asyncio,json, DISCORD_GATEWAY_URL, DISCORD_AUTH_TOKEN, DISCORD_GUILD_ID, DISCORD_PARENT_ID
from src.dependencies import logging, CustomException
from API.utils import resolve_query
from API.discord.utils import ThreadButton
from src.workers.resolver.utils import get_new_thread_summary


class DiscordWebSocket:
    def __init__(self, bot):
        self.ws = None
        self.heartbeat_interval = None
        self.threads = []
        self.bot = bot
        self.last_sequence = None
        self.heartbeat_ack_received = True
        self.reconnect_attempt = 0
        self.max_reconnect_delay = 60
        self.session_id = None
        self.heartbeat_task = None
        self.resume_gateway_url = None
        
    async def connect(self):
        try:
            if self.ws:
                await self.ws.close()
                
            self.ws = await websockets.connect(
                self.resume_gateway_url or DISCORD_GATEWAY_URL,
                ping_interval=None,
                ping_timeout=None
            )
            
            if self.session_id and self.last_sequence:
                await self.resume_session()
            else:
                await self.establish_new_session()
            
            self.reconnect_attempt = 0
            self.heartbeat_ack_received = True
            
            if self.heartbeat_task and not self.heartbeat_task.done():
                self.heartbeat_task.cancel()
            
            self.heartbeat_task = asyncio.create_task(self.heartbeat_loop())
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to connect to Discord: {str(e)}")
            return False

    async def establish_new_session(self):
        """Establish a new Discord session"""
        hello_event = await self.receive_json_response()
        if hello_event["op"] != 10:
            raise CustomException("Expected HELLO event from Discord")
            
        self.heartbeat_interval = hello_event['d']['heartbeat_interval'] / 1000
        
        await self.send_json_request({
            "op": 1,
            "d": self.last_sequence
        })
        
        response = await self.receive_json_response()
        if response['op'] != 11:
            raise CustomException("Expected HEARTBEAT_ACK after initial heartbeat")
        
        identify_payload = {
            "op": 2,
            "d": {
                "token": DISCORD_AUTH_TOKEN,
                "intents": 131071,
                "properties": {
                    "$os": "linux",
                    "$browser": "sage_resolver_discord_bot",
                    "$device": "cloud_server"
                }
            }
        }
        
        await self.send_json_request(identify_payload)
        
        while True:
            event = await self.receive_json_response()
            if event['op'] == 0 and event['t'] == 'READY':
                self.session_id = event['d']['session_id']
                self.resume_gateway_url = event['d'].get('resume_gateway_url')
                break

    async def resume_session(self):
        """Attempt to resume an existing session"""
        resume_payload = {
            "op": 6,
            "d": {
                "token": DISCORD_AUTH_TOKEN,
                "session_id": self.session_id,
                "seq": self.last_sequence
            }
        }
        await self.send_json_request(resume_payload)

    async def heartbeat_loop(self):
        """Maintains the connection by sending periodic heartbeats"""
        try:
            first_heartbeat = True
            while True:
                if first_heartbeat:
                    jitter = self.heartbeat_interval * random.random()
                    await asyncio.sleep(jitter)
                    first_heartbeat = False
                else:
                    await asyncio.sleep(self.heartbeat_interval)

                if not self.heartbeat_ack_received:
                    logging.warning("Previous heartbeat was not acknowledged, reconnecting...")
                    await self.reconnect()
                    return

                await self.send_json_request({
                    "op": 1,
                    "d": self.last_sequence
                })
                self.heartbeat_ack_received = False
                logging.debug("Heartbeat sent!")
                
        except asyncio.CancelledError:
            logging.info("Heartbeat loop cancelled")
        except Exception as e:
            logging.error(f"Heartbeat loop failed: {str(e)}")
            await self.reconnect()

    async def reconnect(self):
        """Handle reconnection with exponential backoff"""
        self.reconnect_attempt += 1
        delay = min(2 ** self.reconnect_attempt, self.max_reconnect_delay)
        
        logging.info(f"Attempting to reconnect in {delay} seconds (attempt {self.reconnect_attempt})")
        
        if self.ws:
            try:
                await self.ws.close()
            except:
                pass
                
        self.ws = None
        await asyncio.sleep(delay)
        
        connected = await self.connect()
        if not connected:
            await self.reconnect()
        
    async def send_json_request(self, payload):
        """Send JSON data to Discord"""
        if not self.ws:
            raise CustomException("WebSocket not connected")
        try:
            await self.ws.send(json.dumps(payload))
        except Exception as e:
            logging.error(f"Failed to send message: {str(e)}")
            await self.reconnect()
            raise

    async def receive_json_response(self):
        """Receive and parse JSON response"""
        if not self.ws:
            raise CustomException("WebSocket not connected")
        try:
            response = await self.ws.recv()
            data = json.loads(response)
            
            if 's' in data and data['s'] is not None:
                self.last_sequence = data['s']
                
            if data['op'] == 11: 
                self.heartbeat_ack_received = True
                logging.debug("Received heartbeat acknowledgment")
                
            return data
        except websockets.exceptions.ConnectionClosed as e:
            logging.info(f"WebSocket connection closed: {e.code} {e.reason}")
            await self.reconnect()
            raise
        except Exception as e:
            logging.error(f"Failed to receive message: {str(e)}")
            await self.reconnect()
            raise
        
    async def send_ai_response_to_thread(self, thread_id, ai_response, thread_link):
        """
        Utility function to send AI response as an embed with a button.
        """
        embed = discord.Embed(
            title="Hmmm, I think this may have been solved before 🤔",
            description=f"**──────────**\n\n{ai_response}\n\n",
            color=0x9B59B6
        )

        view = discord.ui.View()
        button_view = ThreadButton(thread_link)
        
        view.add_item(
            discord.ui.Button(
                label="🔗 View Discussion",
                style=discord.ButtonStyle.link,
                url=thread_link
            )
        )

        success = await self.bot.send_thread_message(
            thread_id, 
            embed=embed, 
            view=button_view 
        )

        if not success:
            logging.error(f"Failed to send AI response to thread {thread_id}")


    async def handle_thread_create(self, event):
        """Handle thread creation events"""
        guild_id = event['d']['guild_id']
        if guild_id == DISCORD_GUILD_ID:
            if event['d']['newly_created']:
                parent_id = event['d']['parent_id']
                if parent_id == DISCORD_PARENT_ID:
                    thread = {
                        "id": event['d']['id'],
                        "title": event['d']['name']
                    }
                    self.threads.append(thread)
                    logging.info(f"New thread created: {thread['title']}")

    async def handle_message_create(self, event):
        """Handle message creation events"""
        guild_id = event['d']['guild_id']
        if guild_id == DISCORD_GUILD_ID:
            message_channel_id = event['d']['channel_id']
            message_author = event['d']['author']['username']
            
            if len(self.threads) > 0:
                if message_channel_id == self.threads[-1]['id']:
                    description_timestamp = event['d']['timestamp']
                    description = event['d']['content']
                    self.threads[-1]['description'] = description
                    self.threads[-1]['timestamp'] = description_timestamp
                    self.threads[-1]['author'] = message_author
                    
                    try:
                        summarised_thread = get_new_thread_summary(self.threads[-1])
                        if summarised_thread:
                            response = await resolve_query(summarised_thread)
                            logging.info(f"Resolver Response: {response}")
                    
                            
                            if(response['status']==200):    
                                thread_id = int(self.threads[-1]['id'])
                                thread_link = f"discord://discord.com/channels/{DISCORD_GUILD_ID}/{DISCORD_PARENT_ID}/threads/1338090859278631004"
                                # thread_link = f"https://discord.com/channels/{DISCORD_GUILD_ID}/{DISCORD_PARENT_ID}/threads/{response['source']}"

                                await self.send_ai_response_to_thread(thread_id, response['solution'], thread_link)
                                 
                            
                            self.threads.clear()
                    except Exception as e:
                        logging.error(f"Error processing thread: {str(e)}")    

    async def listen(self):
        """Main event loop for receiving Discord events"""
        try:
            while True:
                event = await self.receive_json_response()
                
                if event['op'] == 7:  
                    logging.info("Received RECONNECT request from Discord")
                    await self.reconnect()
                    return
                elif event['op'] == 9:  
                    logging.warning("Received INVALID SESSION, clearing session data")
                    self.session_id = None
                    self.last_sequence = None
                    await asyncio.sleep(random.randint(1, 5))
                    await self.reconnect()
                    return
                elif event['t'] == 'THREAD_CREATE':
                    await self.handle_thread_create(event)
                elif event['t'] == 'MESSAGE_CREATE':
                    await self.handle_message_create(event)
                
        except Exception as e:
            logging.error(f"Event loop failed: {str(e)}")
            await self.reconnect()

async def persist_discord_connection(bot):
    """Main connection handler"""
    discord_ws = DiscordWebSocket(bot)
    
    while True:
        try:
            connected = await discord_ws.connect()
            if connected:
                await discord_ws.listen()
            else:
                await asyncio.sleep(5)
        except Exception as e:
            logging.error(f"Connection failed: {str(e)}")
            await asyncio.sleep(5)