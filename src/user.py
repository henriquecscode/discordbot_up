import json
import re
import os
from events.interaction import Interaction
from database.dbs.schema import *
from datetime import datetime, timedelta
from pymongo import MongoClient
import threading
import sys
import time
from notification import send_dm

client = MongoClient('localhost', 27017)

db = client['up']
users_col = db.users
users_col.create_index("id", unique=True)
user_interactions = {}

filename = "users.json"
def setup_data():
    users = list(users_col.find())
    for user in users:
        create_user_interaction(user)


def store_data():
    with open(filename, "w") as json_file:
        json.dump(users_col, json_file, indent=4)

def users(id) -> dict:
    return users_col.find_one({"id": id})

def create_user(user):
    new_user = {
        "id": user,
        "faculties": [],
        "session_cookie": None,
        "username": None,
        "password": None,
        "data": {
            "schedule": [],
            "joint_schedule": [],
            "incoming_friend_invites": [],
            "friends": [],
            "events": [],
            "ucs": []
        },
    }
    users_col.insert_one(new_user)
    create_user_interaction(new_user)

def create_user_interaction(user):
    user_interactions[user['id']] = {
        "current_interaction": None,
        "current_interaction_data": None
    }

def account_checker(user):
    # Check if {"name" : user} exists in the database
    if users_col.find_one({"id": user}) is None:
        create_user(user)

def send_friend_request(user1, user2, user2_name):
    if user1 == user2:
        return "You can't friend request yourself"
    if user2 in users(user1)["data"]["friends"]:
        return user2 + " is already on your friends list"
    
    if user1 in users(user2)["data"]["incoming_friend_invites"]:     
        return "You already sent a friend request to " + user2_name
    
    users_col.find_one_and_update({"id": user2}, {"$push": {"data.incoming_friend_invites": user1}})
    return "Friend request sent to " + user2_name

def check_friend_requests(user):
    if len(users(user)["data"]["incoming_friend_invites"]) == 0:
        return "You have no incoming friend requests!"
    return "\n".join([f"{index}. {name}" for index, name in enumerate(users(user)["data"]["incoming_friend_invites"], start=1)])

def accept_friend_request(user, index):
    if len(users(user)["data"]["incoming_friend_invites"]) == 0:
        return "You have no incoming friend requests!"
    if index > len(users(user)["data"]["incoming_friend_invites"]):
        return "Friend request not found, you only have " + len(users(user)["data"]["incoming_friend_invites"]) + " friend requests!"
    
    user2 = users(user)["data"]["incoming_friend_invites"][index - 1]
    users_col.update_one({"id": user}, {"$push": {"data.friends": user2}, "$pop": {"data.incoming_friend_invites": index - 1}})
    users_col.update_one({"id": user2}, {"$push": {"data.friends": user}})

    return "Friend request from " + user2 + " accepted!"

def remove_friend(user1, user2, user2_name):
    user1_friends = users(user1)["data"]["friends"]
    if user2 not in user1_friends:
        return user2 + " is not on your friends list"
    
    user2_friends = users(user2)["data"]["friends"]

    user1_friends.remove(user2)
    user2_friends.remove(user1)

    users_col.update_one({"id": user1}, {"$set": {"data.friends": user1_friends}})
    users_col.update_one({"id": user2}, {"$set": {"data.friends": user2_friends}})

    return user2_name + " has been removed from your friends list"

def show_friends_list(user):
    if len(users(user)["data"]["friends"]) == 0:
        return "You have no friends :("
    return "\n".join(map(str, users(user)["data"]["friends"]))

def add_cookie(user, cookie):
    users_col.update_one({"id": user}, {"$set": {"session_cookie": cookie}})
    return "Session cookie saved"

def add_username(user, username):
    pattern = r'^up\d{9}(@up.pt)?(@fe.up.pt)?$'
    if re.match(pattern, username):
        users(user)["username"] = username
        return "Username saved"
    else:
        return "Wrong username format, available formats: \nupXXXXXXXXX \nupXXXXXXXXX@up.pt \nupXXXXXXXXX@fe.up.pt"

def add_password(user, password):
    users_col.update_one({"id": user}, {"$set": {"password": password}})
    return "Password saved"


def has_current_interaction(user):
    return bool(user_interactions[user]['current_interaction'])

def get_current_interaction(user):
    return user_interactions[user]['current_interaction']

def get_current_interaction_data(user):
    return user_interactions[user]['current_interaction_data']

def cancel_current_interaction(user):
    user_interactions[user]['current_interaction'] = None
    user_interactions[user]['current_interaction_data'] = None

def create_event(user, date_obj, name, hour , minute):
    if (hour or minute):
        time_delta = timedelta(hours=int(hour), minutes=int(minute))
        event_time = date_obj + time_delta
    else:
        event_time = date_obj

    if event_time < datetime.now():
        return "This date is from the past, please only setup future events"
    else:
        event = [name, event_time.timestamp()]
        users_col.find_one_and_update({"id": user}, {"$push": {"data.events": event}})
        update_events(user)
        setup_event_notifications() 
        return "Event '" + name + "' at " + str(event_time.strftime('%d-%m-%Y %H:%M')) + " saved to your events. Do !events to check your future events"

def delete_event(user, event):
    if event > len(users(user)["data"]["events"]) or event < 0:
        return "That event doesn't exist"
    user_events = users(user)["data"]["events"]
    event_name = user_events[event][0]
    del user_events[event]

    users_col.update_one({"id": user}, {"$set": {"data.events": user_events}})
    update_events(user)
    setup_event_notifications()
    return "Event " + event_name + " deleted"

def get_events_list(user):
    events_list =[]
    user_data = users(user)["data"]["events"]
    for event in user_data:
        events_list.append(event[0] + " at " + str(datetime.utcfromtimestamp(event[1]).strftime('%d-%m-%Y %H:%M')))
    return events_list


def update_events(user):
    user_events = users(user)["data"]["events"]
    user_events = sorted(user_events, key=lambda x: x[1])
    users_col.update_one({"id": user}, {"$set": {"data.events": user_events}})
    now = datetime.now().timestamp()
    week = 604800
    for index, event_time in enumerate(user_events):
        if now >= event_time[1] + week:
            delete_event(user, index)
    return

current_event = ["", sys.maxsize, 0]
timer = None

def send_notification():
    global current_event
    print("Time to notificate " + str(current_event[2]) + " of event " + current_event[0])
    #send_dm(current_event)
    current_event = ["", sys.maxsize, 0]
    setup_event_notifications()

def setup_event_notifications(): #Sets the next event as current_event, defaulting the timer
    global current_event, timer
    current_event = ["", sys.maxsize, 0]
    temp = current_event.copy()
    all_users = users_col.find()
    for user in all_users:
        next_event = None
        user_event_data = users(user["id"])["data"]["events"]
        for event in user_event_data:
            if event[1] > int(time.time()):
                next_event = event
                next_event.append(user["id"]) #Nearest future event for this user
                break
        if next_event != None:
            if next_event[1] < current_event[1]:
                current_event = next_event

    #Defaults timer
    if temp != current_event:
        if timer != None:
            timer.cancel()
        increment = current_event[1] - int(time.time())
        if increment > 0:
            timer = threading.Timer(increment, send_notification)
            timer.start()
    return
