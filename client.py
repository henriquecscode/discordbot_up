import discord

def create_client():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    return client

client = create_client()