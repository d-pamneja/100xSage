from discord.ui import Button, View
from API.dependencies import discord

class ThreadButton(View):
    def __init__(self, thread_link: str):
        super().__init__()
        self.add_item(Button(label="🔗 View Discussion", url=thread_link, style=discord.ButtonStyle.link))
