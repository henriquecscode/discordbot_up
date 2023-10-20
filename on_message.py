import discord
from client import client

PREFIX = '!'
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(PREFIX):
        await message.channel.send('hello')
    print(f"Received {message}")