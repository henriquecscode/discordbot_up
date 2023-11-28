import os
import requests
from src.services.login import *
from src.services.schedules.get_schedule import get_schedule_from_cookie, get_schedule_from_session

def test(token, username, password):

    session = create_session(username, password, None)
    session2 = create_session_from_previous(None, session)
    # session2 = continue_session("284544009", "181980375", "IGxeWDxmSFZBeFFoUkpCZURsciludkhyOSdsfjh3WjYiQCFTNUlkTUxBSSBiWlNhbWh2PCFKZTp0S1hUDun4RCm4/jVEvAdn6CIY9u68ThrV5jCgmJ51j2B9J4DL7Ecr644uPjUgQZRiXioCFQo6BR4Gw3lZs5jb")
    # get_schedule_from_session(session2)



    session_cookie = login_credentials(username, password, None)
    get_schedule_from_cookie(session_cookie)


if __name__=="__main__":
    
    my_token = os.getenv('TOKEN')
    my_username = os.getenv('USER')
    my_password = os.getenv('PASSWORD')
    test(my_token, my_username, my_password)
