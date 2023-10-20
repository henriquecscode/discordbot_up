import discord
import os
from client import client

def define_events():
    import on_ready
    import on_message
if __name__ == "__main__":
    token = os.getenv('TOKEN')
    define_events()
    client.run(token)