import json
import re
import os
from events.interaction import Interaction
from database.dbs.schema import *
from datetime import datetime, timedelta
from pymongo import MongoClient
from slot_types import  EVENT
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
        "number": None,
        "name": None,
        "data": {
            "schedule": [],
            "joint_schedule": [],
            "incoming_friend_invites": [],
            "friends": [],
            "events": [],
            "ucs": [],
            "office_reservations": []
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

def add_number(user, number):
    users_col.find_one_and_update({"id": user}, {"$set": {"number": number}})

def get_number(user):
    return users(user)["number"]

def add_name(user, name):
    users_col.find_one_and_update({"id": user}, {"$set": {"name": name}})

def get_name(user):
    return users(user)["name"]

def send_friend_request(user1, user1name, user2, user2_name):
    if user1 == user2:
        return "You can't friend request yourself"
    friends = users(user1)["data"]["friends"]
    incoming = users(user2)["data"]["incoming_friend_invites"]

    if any(user2_name in sublist[0] for sublist in friends):
        return f"{user2_name} is already on your friends list"

    if any(user1name in sublist[0] for sublist in incoming):
        return f"You already sent a friend request to {user2_name}"

    user = [user1name, user1]
    users_col.find_one_and_update({"id": user2}, {"$push": {"data.incoming_friend_invites": user}})
    return f"Friend request sent to {user2_name}"

def check_friend_requests(user):
    if len(users(user)["data"]["incoming_friend_invites"]) == 0:
        return "You have no incoming friend requests!"
    return "\n".join([f"{index}. {name[0]}" for index, name in enumerate(users(user)["data"]["incoming_friend_invites"], start=1)])

def accept_friend_request(user_id, user_name, index):
    if len(users(user_id)["data"]["incoming_friend_invites"]) == 0:
        return "You have no incoming friend requests!"
    if index > len(users(user_id)["data"]["incoming_friend_invites"]):
        return f"Friend request not found, you only have {len(users(user_id)['data']['incoming_friend_invites'])} friend requests!"
    
    user2 = users(user_id)["data"]["incoming_friend_invites"][index - 1]
    user1 = [user_name, user_id]
    user2_name = user2[0]
    user2_id = user2[1]

    users_col.update_one({"id": user_id}, {"$push": {"data.friends": user2}, "$pull": {"data.incoming_friend_invites": index - 1}})
    users_col.update_one({"id": user2_id}, {"$push": {"data.friends": user1}})
    return f"Friend request from {user2_name} accepted!"

def remove_friend(user1, user2, user2_name):
    user1_friends = users(user1)["data"]["friends"]
    if any(user2 == sublist[1] for sublist in user1_friends) == False:
        return f"{user2_name} is not on your friends list"
    
    user2_friends = users(user2)["data"]["friends"]

    user1_friends = [sublist for sublist in user1_friends if sublist[1] != user2]
    user2_friends = [sublist for sublist in user2_friends if sublist[1] != user1]

    users_col.update_one({"id": user1}, {"$set": {"data.friends": user1_friends}})
    users_col.update_one({"id": user2}, {"$set": {"data.friends": user2_friends}})

    return f"{user2_name} has been removed from your friends list"

def show_friends_list(user):
    if len(users(user)["data"]["friends"]) == 0:
        return "You have no friends :("
    list = users(user)["data"]["friends"]
    return "\n".join(str(sublist[0]) for sublist in list)

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
        users_col.find_one_and_update(
            {"id": user}, {"$push": {"data.events": event}})

        if (hour or minute):
            duration = 60
        else:
            duration = 60 * 24
        event_object = {
            "type": EVENT,
            "class": {
                "name": name,
                "date": event_time,
                "duration": duration
            }
        }

        users_col.find_one_and_update({"id": user}, {"$push": {"data.joint_schedule": event_object}})

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

current_event = [["", sys.maxsize, 0]]
timer = None
import threading
import asyncio
from client import get_client
next_event = []
notification_condition = threading.Condition()
notification_thread = None
notified = True


def send_notification():
    global current_event
    for event in current_event:
        message = "Event " + event[0] + " is now!"
        user_id = event[2]
        next_event.append([user_id, message])
        notification_condition.acquire()
        notification_condition.notify()
        notification_condition.release()
    current_event = [["", sys.maxsize, 0]]
    setup_event_notifications()

async def send_message():
    global next_event
    event = next_event[0]
    user_id, message = event[0], event[1]
    next_event = next_event[1:]
    user = await get_client().fetch_user(user_id)
    await user.send(message)
    return None

async def notification_loop():
    global next_event, notification_thread
    while True:
        if len(next_event) == 0:
            await asyncio.sleep(1)
            continue
        else:
            await send_message()

def setup_event_notifications(): #Sets the next event as current_event, defaulting the timer
    global current_event, timer, notified
    current_event = [["", sys.maxsize, 0]]
    temp = current_event.copy()
    all_users = users_col.find()
    for user in all_users:
        next_event = None
        events = []
        user_event_data = users(user["id"])["data"]["events"]
        for event in user_event_data:
            if event[1] > int(time.time()):
                next_event = event
                next_event.append(user["id"]) #Nearest future event for this user
                if len(events) > 0:
                    if events[0][1] < next_event[1]:
                        break
                events.append(next_event)
        if len(events) != 0:
            if events[0][1] < current_event[0][1]:
                current_event = events
            elif events[0][1] == current_event[0][1]:
                current_event = current_event + events

    #Defaults timer
    if temp != current_event and notified:
        notified = False
        if timer != None:
            timer.cancel()
        increment = current_event[0][1] - int(time.time())
        if increment > 0:        
            timer = threading.Timer(increment, send_notification)
            timer.start()
    return

def are_friends(user_id, user2_name):
    user_friends = users(user_id)["data"]["friends"]
    for friend in user_friends:
        if friend[0] == user2_name:
            return True
    return False