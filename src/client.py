import discord

def create_client():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    return client

def define_events():
    import events.on_ready
    import events.on_message

client = create_client()
define_events()
