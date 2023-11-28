from enum import Enum

class Interaction(Enum):
    ADD_SCHEDULE = "add_schedule"
    CHOOSE_FACULTY_TO_ADD = "choose_faculty_to_add"
    CHOOSE_FACULTY_TO_EDIT = "choose_faculty_to_edit"
    MANAGE_FACULTY = "manage_faculty"
    ADD_COURSE = "add_course"
    EDIT_COURSE = "edit_course"
    MANAGE_COURSE = "manage_course"
    ADD_COURSE_UNIT = "add_course_unit"
    EDIT_COURSE_UNIT = "edit_course_unit"
    MANAGE_COURSE_UNIT = "manage_course_unit"
    ADD_CLASS = "add_class"
    VIEW_CLASS = "edit_class"
    REMOVE_CLASS = "remove_class"
