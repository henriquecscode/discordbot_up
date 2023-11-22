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
            public = False
        elif isinstance(message.channel, discord.TextChannel):
            print(f"Received a message in {message.channel.name} on {message.guild.name} from {message.author}: {message.content}")
            public = True
        result = input.process_input(message, public)
        answer = result[0]
        is_sensitive = result[1]
        await message.channel.send(answer)
        if public:
            if is_sensitive:
                await message.delete()