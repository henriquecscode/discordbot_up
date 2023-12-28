from dotenv import load_dotenv
load_dotenv()
import discord
import os
import user
from client import client

user.setup_data()

if __name__ == "__main__":
    my_token = os.getenv('TOKEN')
    client.run(my_token)