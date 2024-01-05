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
        await safe_send_message(message.channel, answer)
        if public:
            if is_sensitive:
                await message.delete()


async def safe_send_message(channel, message):
    if len(message) < 2000:
        await channel.send(message)
        return
    
    lines = message.split("\n")
    current_message = ""
    for line in lines:
        if len(current_message) + len(line) < 2000:
            current_message += line + "\n"
        else:
            await channel.send(current_message)
            current_message = line + "\n"
    await channel.send(current_message)