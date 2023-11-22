from dotenv import load_dotenv
load_dotenv()
import discord
import os
import user
from client import client


user.setup_data()

if __name__ == "__main__":
    my_token = os.getenv('TOKEN')
    my_username = os.getenv('USER')
    my_password = os.getenv('PASSWORD')
    client.run(my_token)