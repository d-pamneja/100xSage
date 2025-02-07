from API.dependencies import websockets, asyncio,json, DISCORD_GATEWAY_URL, DISCORD_AUTH_TOKEN, DISCORD_GUILD_ID, DISCORD_PARENT_ID
from src.dependencies import logging, CustomException
from API.utils import resolve_query
from API.discord.bot import DiscordMessageSender
from src.workers.resolver.utils import get_new_thread_summary


class DiscordWebSocket:
    def __init__(self):
        self.ws = None
        self.heartbeat_interval = None
        self.threads = []
        self.message_sender = DiscordMessageSender(token=DISCORD_AUTH_TOKEN)
        
    async def connect(self):
        try:
            self.ws = await websockets.connect(DISCORD_GATEWAY_URL)
            
            hello_event = await self.receive_json_response()
            if hello_event["op"] != 10:
                raise CustomException("Expected HELLO event from Discord")
                
            self.heartbeat_interval = hello_event['d']['heartbeat_interval'] / 1000
            
            identify_payload = {
                "op": 2,
                "d": {
                    "token": DISCORD_AUTH_TOKEN,
                    "intents": 3276799,
                    "properties": {
                        "$os": "linux",
                        "$browser": "sage_resolver_discord_bot",
                        "$device": "cloud_server"
                    }
                }
            }
            
            await self.send_json_request(identify_payload)
            
            asyncio.create_task(self.heartbeat_loop())
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to connect to Discord: {str(e)}")
            return False

    async def heartbeat_loop(self):
        """Maintains the connection by sending periodic heartbeats"""
        try:
            while True:
                await asyncio.sleep(self.heartbeat_interval)
                await self.send_json_request({"op": 1, "d": None})
                logging.info("Heartbeat sent!")
                
        except Exception as e:
            logging.error(f"Heartbeat loop failed: {str(e)}")
            await self.connect()

    async def send_json_request(self, payload):
        """Send JSON data to Discord"""
        if not self.ws:
            raise CustomException("WebSocket not connected")
        try:
            await self.ws.send(json.dumps(payload))
        except Exception as e:
            logging.error(f"Failed to send message: {str(e)}")
            raise

    async def receive_json_response(self):
        """Receive and parse JSON response"""
        if not self.ws:
            raise CustomException("WebSocket not connected")
        try:
            response = await self.ws.recv()
            return json.loads(response)
        except Exception as e:
            logging.error(f"Failed to receive message: {str(e)}")
            raise
        
    async def send_ai_response_to_thread(self,thread_id, ai_response):
        """
        Utility function to send AI response to a Discord thread
        
            :param thread_id: ID of the thread
            :param ai_response: AI-generated response to send
        """
        
        
        
        success = await self.message_sender.send_thread_message(thread_id, ai_response)
        
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
                        # summarised_thread = get_new_thread_summary(self.threads[-1])
                        summarised_thread = "HAAN MEIN HOON"
                        if summarised_thread:
                            # response = resolve_query(summarised_thread)
                            # logging.info(f"Resolver Response: {response}")
                            
                            response = {
                                "status" : 200,
                                "solution" : "dummy test"
                            }
                            
                            if(response['status']==200):
                                print("THIS FEATURE IS STILL IN WORKS!!")
                                # await self.send_ai_response_to_thread(
                                #     thread_id=self.threads[-1]['id'], 
                                #     ai_response=response['solution']
                                # )
                            
                            self.threads.clear()
                    except Exception as e:
                        logging.error(f"Error processing thread: {str(e)}")    

    async def listen(self):
        """Main event loop for receiving Discord events"""
        try:
            while True:
                event = await self.receive_json_response()
                
                if event['t'] == 'THREAD_CREATE':
                    await self.handle_thread_create(event)
                elif event['t'] == 'MESSAGE_CREATE':
                    await self.handle_message_create(event)
                
                await asyncio.sleep(5)
                    
        except Exception as e:
            logging.error(f"Event loop failed: {str(e)}")
            await self.connect()

async def persist_discord_connection():
    """Main connection handler"""
    discord_ws = DiscordWebSocket()
    
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