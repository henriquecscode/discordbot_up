import discord

client = None
def create_client():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    return client

def define_events():
    import events.on_ready
    import events.on_message

def get_client():
    global client
    if client is None:
        client = create_client()
        define_events()

    return client

