import user
from events.interaction import Interaction
from services.office import get_office, cancel_office
from services.session import get_session
from typing import Dict, List


def get_office_reservations(username):
    return user.users(username)["data"]["office_reservations"]

def add_office_reservation(username, reservation):

    date = reservation["date"]
    start_time = reservation["start_time"]
    duration = reservation["duration"]
    motivation = reservation["motivation"]
    observation = reservation["observation"]
    number = user.get_number(username)

    session = get_session()
    did_reservation, reservation_feedback = get_office(session, number, date, start_time, duration, motivation, observation)

    if did_reservation:
        reservation_id = reservation_feedback
        reservation["id"] = reservation_id
        user.users_col.update_one({"id": username}, {"$push": {"data.office_reservations": reservation}})
        return True, "Successfully reserved office"
    else: 
        if reservation_feedback is not None:
            reservation_error_message = reservation_feedback
        else:
            reservation_error_message = "Unknown error"
        return False, reservation_error_message

def cancel_office_reservation(username, reservation: Dict):
    reservation_id = reservation["id"]
    
    session = get_session()
    did_cancel, cancel_feedback = cancel_office(session, reservation_id)
    if did_cancel:
        user.users_col.update_one({"id": username}, {"$pull": {"data.office_reservations": {"id": reservation_id}}})
        return True, "Successfully cancelled office reservation"
    else:
        if cancel_feedback is not None:
            cancel_error_message = cancel_feedback
        else:
            cancel_error_message = "Unknown error"
        return False, cancel_error_message


def add_reserve_office_interaction(username):
    user.user_interactions[username]["current_interaction"] = Interaction.RESERVE_OFFICE
    user.user_interactions[username]["current_interaction_data"] = {}

def add_confirm_reserve_office_interaction(username, data):
    user.user_interactions[username]["current_interaction"] = Interaction.CONFIRM_RESERVE_OFFICE
    user.user_interactions[username]["current_interaction_data"] = data

def add_cancel_office_interaction(username, reservations: List[Dict]):
    user.user_interactions[username]["current_interaction"] = Interaction.CANCEL_OFFICE
    user.user_interactions[username]["current_interaction_data"] = reservations
