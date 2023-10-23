import json

users = {}
filename = "users.json"

def setup_data():
    global users
    with open(filename, "r") as json_file:
        users = json.load(json_file)

def store_data():
    with open(filename, "w") as json_file:
        json.dump(users, json_file, indent=4)

def create_user(user):
    new_user = {
        "faculdade": None,
        "session_cookie": None,
        "username": None,
        "password": None,
        "data": {
            "schedule": [],
            "incoming_friend_invites": [],
            "friends": [],
            "events": [],
            "ucs": []
        }
    }
    users[user] = new_user
    store_data()

def account_checker(user):
    if user not in users:
        create_user(user)

def send_friend_request(user1, user2):
    if user1 == user2:
        return "You can't friend request yourself"
    if user2 in users[user1]["data"]["friends"]:     
        return user2 + " is already on your friends list"
    
    if user1 in users[user2]["data"]["incoming_friend_invites"]:     
        return "You already sent a friend request to " + user2
    
    users[user2]["data"]["incoming_friend_invites"].append(user1)
    store_data()
    return "Friend request sent to " + user2

def check_friend_requests(user):
    if len(users[user]["data"]["incoming_friend_invites"]) == 0:
        return "You have no incoming friend requests!"
    return "\n".join([f"{index}. {name}" for index, name in enumerate(users[user]["data"]["incoming_friend_invites"], start=1)])

def accept_friend_request(user, index):
    if len(users[user]["data"]["incoming_friend_invites"]) == 0:
        return "You have no incoming friend requests!"
    if index > len(users[user]["data"]["incoming_friend_invites"]):
        return "Friend request not found, you only have " + len(users[user]["data"]["incoming_friend_invites"]) + " friend requests!"
    
    user2 = users[user]["data"]["incoming_friend_invites"][index - 1]
    users[user]["data"]["friends"].append(user2)
    users[user2]["data"]["friends"].append(user)

    users[user]["data"]["incoming_friend_invites"].pop(index-1)
    store_data()
    return "Friend request from " + user2 + " accepted!"

def remove_friend(user1, user2):
    if user2 not in users[user1]["data"]["friends"]:
        return user2 + " is not on your friends list"
    
    users[user1]["data"]["friends"].remove(user2)
    users[user2]["data"]["friends"].remove(user1)
    store_data()
    return user2 + " has been removed from your friends list"

def show_friends_list(user):
    if len(users[user]["data"]["friends"]) == 0:
        return "You have no friends :("
    return "\n".join(map(str, users[user]["data"]["friends"]))

