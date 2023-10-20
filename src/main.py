import discord
import os
from dotenv import load_dotenv
from client import client

load_dotenv()

if __name__ == "__main__":
    my_token = os.getenv('TOKEN')
    my_username = os.getenv('USER')
    my_password = os.getenv('PASSWORD')
    client.run(my_token)