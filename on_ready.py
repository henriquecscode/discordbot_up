from client import client

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')