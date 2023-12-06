import json
import re
import os
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['up']
users_col = db.users
users_col.create_index("id", unique=True)
user_interactions = {}

filename = None
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
            "incoming_friend_invites": [],
            "friends": [],
            "events": [],
            "ucs": []
        },
    }
    users_col.insert_one(new_user)
    create_user_interaction(user)

def create_user_interaction(user):
    user_interactions[user] = {
        "current_interaction": None,
        "current_interaction_data": None
    }

def account_checker(user):
    # Check if {"name" : user} exists in the database
    if users_col.find_one({"id": user}) is None:
        create_user(user)

def send_friend_request(user1, user2):
    if user1 == user2:
        return "You can't friend request yourself"
    if user2 in users(user1)["data"]["friends"]:     
        return user2 + " is already on your friends list"
    
    if user1 in users(user2)["data"]["incoming_friend_invites"]:     
        return "You already sent a friend request to " + user2
    
    users_col.find_one_and_update({"id": user2}, {"$push": {"data.incoming_friend_invites": user1}})
    store_data()
    return "Friend request sent to " + user2

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

def remove_friend(user1, user2):
    user1_friends = users(user1)["data"]["friends"]
    if user2 not in user1_friends:
        return user2 + " is not on your friends list"
    
    user2_friends = users(user2)["data"]["friends"]

    user1_friends.remove(user2)
    user2_friends.remove(user1)

    users_col.update_one({"id": user1}, {"$set": {"data.friends": user1_friends}})
    users_col.update_one({"id": user2}, {"$set": {"data.friends": user2_friends}})

    return user2 + " has been removed from your friends list"

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
        store_data()
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