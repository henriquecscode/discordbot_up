from user import users, user_interactions, store_data
from events.interaction import Interaction
from database.dbs.schema import *

def add_faculty(username, faculty: Faculty):
    for user_faculty in users[username]["faculties"]:
        if user_faculty["name"] == faculty.acronym:
            return False
    
    faculty_data = {
        "name": faculty.acronym,
        "full_name": faculty.name,
        "courses": []
    }
    users[username]["faculties"].append(faculty_data)
    store_data()
    return True

def get_faculties(username) -> List[dict]:
    return users[username]["faculties"]

def add_course(username, faculty: dict, course: Course):
    for user_faculty in users[username]["faculties"]:
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

def get_faculty_courses(username, faculty: dict) -> List[dict]:
    for user_faculty in users[username]["faculties"]:
        if user_faculty["name"] == faculty['name']:
            return user_faculty["courses"]
    return []

def add_course_unit(username, faculty: dict, course: dict, course_unit_course_unit_year: Object):
    course_unit: CourseUnit = course_unit_course_unit_year.CourseUnit
    course_unit_year: CourseUnitYear = course_unit_course_unit_year.CourseUnitYear
    for user_faculty in users[username]["faculties"]:
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
                        "year": course_unit_year.course_unit_year,
                        "enroll_year": course_unit.year,
                        "semester": course_unit.semester,
                        "classes": [],
                        "schedule": []
                    }
                    user_course["course_units"].append(course_unit_data)
                    store_data()
                    return True
    return False

def get_course_course_units(username, faculty: dict, course: dict) -> List[dict]:
    for user_faculty in users[username]["faculties"]:
        if user_faculty["name"] == faculty['name']:
            for user_course in user_faculty["courses"]:
                if user_course["name"] == course['name']:
                    return user_course["course_units"]
    return []

def add_class(username, faculty: dict, course: dict, course_unit: dict, schedule: Schedule):
    for user_faculty in users[username]["faculties"]:
        if user_faculty["name"] == faculty['name']:
            for user_course in user_faculty["courses"]:
                if user_course["name"] == course['name']:
                    for user_course_unit in user_course["course_units"]:
                        if user_course_unit["name"] == course_unit['name']:
                            for user_class in user_course_unit["classes"]:
                                if user_class["name"] == schedule.class_name:
                                    return False
                            class_data = {
                                "name": schedule.class_name,
                                "lesson_type": schedule.lesson_type,
                                "id": schedule.id,
                                "location": schedule.location,
                                "day": schedule.day,
                                "start_time": schedule.start_time,
                                "duration": schedule.duration,
                                "professor": schedule.professor_sigarra_id,
                            }
                            user_course_unit["classes"].append(class_data)
                            store_data()
                            return True
    return False

def get_course_unit_classes(username, faculty: dict, course: dict, course_unit: dict) -> List[dict]:
    for user_faculty in users[username]["faculties"]:
        if user_faculty["name"] == faculty['name']:
            for user_course in user_faculty["courses"]:
                if user_course["name"] == course['name']:
                    for user_course_unit in user_course["course_units"]:
                        if user_course_unit["name"] == course_unit['name']:
                            return user_course_unit["classes"]
    return []

def remove_class(username, faculty: dict, course: dict, course_unit: dict, class_name: str):
    for user_faculty in users[username]["faculties"]:
        if user_faculty["name"] == faculty['name']:
            for user_course in user_faculty["courses"]:
                if user_course["name"] == course['name']:
                    for user_course_unit in user_course["course_units"]:
                        if user_course_unit["name"] == course_unit['name']:
                            for user_class in user_course_unit["classes"]:
                                if user_class["name"] == class_name:
                                    user_course_unit["classes"].remove(user_class)
                                    store_data()
                                    return True
    return False


def add_current_schedule_interaction(user):
    user_interactions[user]['current_interaction'] = Interaction.ADD_SCHEDULE
    user_interactions[user]['current_interaction_data'] = None

def add_choose_faculty_to_add_schedule_interaction(username, faculties):
    user_interactions[username]['current_interaction'] = Interaction.CHOOSE_FACULTY_TO_ADD
    user_interactions[username]['current_interaction_data'] = faculties

def add_choose_faculty_to_edit_schedule_interaction(username, faculties):
    user_interactions[username]['current_interaction'] = Interaction.CHOOSE_FACULTY_TO_EDIT
    user_interactions[username]['current_interaction_data'] = faculties

def add_current_faculty_course_interaction(username, faculty):
    user_interactions[username]['current_interaction'] = Interaction.MANAGE_FACULTY
    user_interactions[username]['current_interaction_data'] = faculty

def add_course_interaction(username, faculty: dict, courses: List[Course]):
    user_interactions[username]['current_interaction'] = Interaction.ADD_COURSE
    user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "courses": courses
    }

def add_course_edit_schedule_interaction(username, faculty: dict, courses: List[Course]):
    user_interactions[username]['current_interaction'] = Interaction.EDIT_COURSE
    user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "courses": courses
    }

def add_current_course_course_unit_interaction(username, faculty: dict, course: dict):
    user_interactions[username]['current_interaction'] = Interaction.MANAGE_COURSE
    user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "course": course
    }

def add_add_class_unit_interaction(username, faculty: dict, course: dict, course_units: List[CourseUnit]):
    user_interactions[username]['current_interaction'] = Interaction.ADD_COURSE_UNIT
    user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "course": course,
        "course_units": course_units
    }

def add_edit_class_unit_interaction(username, faculty: dict, course: dict, course_units: List[dict]):
    user_interactions[username]['current_interaction'] = Interaction.EDIT_COURSE_UNIT
    user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "course": course,
        "course_units": course_units
    }

def add_current_course_unit_class_interaction(username, faculty: dict, course: dict, course_unit: dict):
    user_interactions[username]['current_interaction'] = Interaction.MANAGE_COURSE_UNIT
    user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "course": course,
        "course_unit": course_unit
    }

def add_choose_class_to_add_interaction(username, faculty: dict, course: dict, course_unit: dict, classes: List[Schedule]):
    user_interactions[username]['current_interaction'] = Interaction.ADD_CLASS
    user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "course": course,
        "course_unit": course_unit,
        "classes": classes
    }

def add_choose_class_to_view_interaction(username, faculty: dict, course: dict, course_unit: dict, classes: List[dict]):
    user_interactions[username]['current_interaction'] = Interaction.VIEW_CLASS
    user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "course": course,
        "course_unit": course_unit,
        "classes": classes
    }

def add_choose_class_to_remove_interaction(username, faculty: dict, course: dict, course_unit: dict, classes: List[dict]):
    user_interactions[username]['current_interaction'] = Interaction.REMOVE_CLASS
    user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "course": course,
        "course_unit": course_unit,
        "classes": classes
    }