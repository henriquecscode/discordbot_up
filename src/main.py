from dotenv import load_dotenv
load_dotenv()
import discord
import os
import user
from client import get_client

user.setup_data()




import threading
if __name__ == "__main__":    
    my_token = os.getenv('TOKEN')
    my_username = os.getenv('USER')
    my_password = os.getenv('PASSWORD')
    client = get_client()
    client.run(my_token)