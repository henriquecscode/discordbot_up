from enum import Enum

class Interaction(Enum):
    ADD_SCHEDULE = "add_schedule"
    CHOOSE_FACULTY_TO_ADD = "choose_faculty_to_add"
    CHOOSE_FACULTY_TO_EDIT = "choose_faculty_to_edit"
    ADD_SCHEDULE_FACULTY = "add_schedule_faculty"