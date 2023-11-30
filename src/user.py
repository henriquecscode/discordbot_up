import json
import re
import os
from events.interaction import Interaction
from database.dbs.schema import *
from datetime import datetime, timedelta

users = {}
user_interactions = {}
filename = "users.json"

def setup_data():
    global users
    if not os.path.exists(filename):
        users = {}
    else:
        with open(filename, "r") as json_file:
            users = json.load(json_file)

    for user in users:
        create_user_interaction(user)

def store_data():
    with open(filename, "w") as json_file:
        json.dump(users, json_file, indent=4)

def create_user(user):
    new_user = {
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
    users[user] = new_user
    create_user_interaction(user)
    store_data()

def create_user_interaction(user):
    user_interactions[user] = {
        "current_interaction": None,
        "current_interaction_data": None
    }

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

def add_cookie(user, cookie):
    users[user]["session_cookie"] = cookie
    store_data()
    return "Session cookie saved"

def add_username(user, username):
    pattern = r'^up\d{9}(@up.pt)?(@fe.up.pt)?$'
    if re.match(pattern, username):
        users[user]["username"] = username
        store_data()
        return "Username saved"
    else:
        return "Wrong username format, available formats: \nupXXXXXXXXX \nupXXXXXXXXX@up.pt \nupXXXXXXXXX@fe.up.pt"

def add_password(user, password):
    users[user]["password"] = password
    store_data()
    return "Password saved"

def add_faculty(user, faculty: Faculty):
    for user_faculty in users[user]["faculties"]:
        if user_faculty["name"] == faculty.acronym:
            return False
    
    faculty_data = {
        "name": faculty.acronym,
        "full_name": faculty.name,
        "courses": []
    }
    users[user]["faculties"].append(faculty_data)
    store_data()
    return True

def get_faculties(user) -> List[dict]:
    return users[user]["faculties"]

def add_course(user, faculty: dict, course: Course):
    for user_faculty in users[user]["faculties"]:
        if user_faculty["name"] == faculty['name']:
            for user_course in user_faculty["courses"]:
                if user_course["name"] == course.name:
                    return False
            course_data = {
                "name": course.acronym,
                "full_name": course.name,
                "id": course.id,
                "course_units": []
            }
            user_faculty["courses"].append(course_data)
            store_data()
            return True
    return False

def get_faculty_courses(user, faculty: dict) -> List[dict]:
    for user_faculty in users[user]["faculties"]:
        if user_faculty["name"] == faculty['name']:
            return user_faculty["courses"]
    return []

def add_course_unit(user, faculty: dict, course: dict, course_unit: CourseUnit):
    for user_faculty in users[user]["faculties"]:
        if user_faculty["name"] == faculty['name']:
            for user_course in user_faculty["courses"]:
                if user_course["name"] == course['name']:
                    for user_course_unit in user_course["course_units"]:
                        if user_course_unit["name"] == course_unit.name:
                            return False
                    course_unit_data = {
                        "name": course_unit.name,
                        "acronym": course_unit.acronym,
                        "id": course_unit.id,
                        "year": course_unit.year,
                        "semester": course_unit.semester,
                        "classes": [],
                        "schedule": []
                    }
                    user_course["course_units"].append(course_unit_data)
                    store_data()
                    return True
    return False

def has_current_interaction(user):
    return bool(user_interactions[user]['current_interaction'])

def add_current_schedule_interaction(user):
    user_interactions[user]['current_interaction'] = Interaction.ADD_SCHEDULE
    user_interactions[user]['current_interaction_data'] = None

def add_choose_faculty_to_add_schedule_interaction(user, faculties):
    user_interactions[user]['current_interaction'] = Interaction.CHOOSE_FACULTY_TO_ADD
    user_interactions[user]['current_interaction_data'] = faculties

def add_choose_faculty_to_edit_schedule_interaction(user, faculties):
    user_interactions[user]['current_interaction'] = Interaction.CHOOSE_FACULTY_TO_EDIT
    user_interactions[user]['current_interaction_data'] = faculties

def add_current_faculty_course_interaction(user, faculty):
    user_interactions[user]['current_interaction'] = Interaction.MANAGE_FACULTY
    user_interactions[user]['current_interaction_data'] = faculty

def add_course_interaction(user, faculty: dict, courses: List[Course]):
    user_interactions[user]['current_interaction'] = Interaction.ADD_COURSE
    user_interactions[user]['current_interaction_data'] = {
        "faculty": faculty,
        "courses": courses
    }

def add_course_edit_schedule_interaction(user, faculty: dict, courses: List[Course]):
    user_interactions[user]['current_interaction'] = Interaction.EDIT_COURSE
    user_interactions[user]['current_interaction_data'] = {
        "faculty": faculty,
        "courses": courses
    }

def add_current_course_class_interaction(user, faculty: dict, course: dict):
    user_interactions[user]['current_interaction'] = Interaction.MANAGE_COURSE
    user_interactions[user]['current_interaction_data'] = {
        "faculty": faculty,
        "course": course
    }

def add_class_interaction(user, faculty: dict, course: dict, classes: List[CourseUnit]):
    user_interactions[user]['current_interaction'] = Interaction.ADD_CLASS
    user_interactions[user]['current_interaction_data'] = {
        "faculty": faculty,
        "course": course,
        "classes": classes
    }

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
        users[user]["data"]["events"].append(event)
        store_data()
        return "Event '" + name + "' at " + str(event_time.strftime('%d-%m-%Y %H:%M')) + " saved to your events. Do !events to check your future events"

def delete_event(user, event):
    if event > len(users[user]["data"]["events"]) or event < 0:
        return "That event doesn't exist"
    event_name = users[user]["data"]["events"][event][0]
    users[user]["data"]["events"].pop(event)
    store_data()
    return "Event " + event_name + " deleted"

def get_events_list(user):
    events_list =[]
    for event in users[user]["data"]["events"]:
        events_list.append(event[0] + " at " + str(datetime.utcfromtimestamp(event[1]).strftime('%d-%m-%Y %H:%M')))
    return sorted(events_list, key=lambda x: x[1])


def update_events(user):
    now = datetime.now().timestamp()
    week = 604800
    for index, event_time in enumerate(users[user]["data"]["events"]):
        if now >= event_time[1] + week:
            delete_event(user, index)
    return
