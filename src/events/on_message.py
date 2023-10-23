import discord
from client import client
import input

PREFIX = '!'
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(PREFIX):
        if isinstance(message.channel, discord.DMChannel):
            print(f"Received a DM from {message.author}: {message.content}")
        elif isinstance(message.channel, discord.TextChannel):
            print(f"Received a message in {message.channel.name} on {message.guild.name} from {message.author}: {message.content}")

        await message.channel.send(input.process_input(message))