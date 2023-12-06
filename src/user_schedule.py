import user
from events.interaction import Interaction
from database.dbs.schema import *
from typing import List


def add_faculty(username, faculty: Faculty):
    for user_faculty in user.users(username)["faculties"]:
        if user_faculty["name"] == faculty.acronym:
            return False
    
    faculty_data = {
        "name": faculty.acronym,
        "full_name": faculty.name,
        "courses": []
    }
    user.users_col.update_one({"id": username}, {"$push": {"faculties": faculty_data}})
    return True

def get_faculties(username) -> List[dict]:
    return user.users(username)["faculties"]

def add_course(username, faculty: dict, course: Course):        
    if user.users_col.find_one({"id": username, "faculties.$[faculty].courses.$[course]": {"$in": course.name} }, array_filters=[{"faculty.name": faculty['name']}, {"course.id": course.id}]) is not None:
        return False
    
    course_data = {
    "id": course.id,
    "name": course.acronym,
    "full_name": course.name,
    "course_units": []
    }
    
    user.users_col.update_one({"id": username}, {"$push": {"faculties.$[faculty].courses": course_data}}, array_filters=[{"faculty.name": faculty['name']}])
    return True

def get_faculty_courses(username, faculty: dict) -> List[dict]:
    for user_faculty in user.users(username)["faculties"]:
        if user_faculty["name"] == faculty['name']:
            return user_faculty["courses"]
    return []

def add_course_unit(username, faculty: dict, course: dict, course_unit_course_unit_year: Object):
    course_unit: CourseUnit = course_unit_course_unit_year.CourseUnit
    course_unit_year: CourseUnitYear = course_unit_course_unit_year.CourseUnitYear
    for user_faculty in user.users(username)["faculties"]:
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
                    user.users_col.update_one({"id": username}, {"$push": {"faculties.$[faculty].courses.$[course].course_units": course_unit_data}}, array_filters=[{"faculty.name": faculty['name']}, {"course.name": course['name']}])
                    user_course["course_units"].append(course_unit_data)
                    user.store_data()
                    return True
    return False

def get_course_course_units(username, faculty: dict, course: dict) -> List[dict]:
    for user_faculty in user.users(username)["faculties"]:
        if user_faculty["name"] == faculty['name']:
            for user_course in user_faculty["courses"]:
                if user_course["name"] == course['name']:
                    return user_course["course_units"]
    return []

def add_class(username, faculty: dict, course: dict, course_unit: dict, schedule: Schedule):
    for user_faculty in user.users(username)["faculties"]:
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
                            user.store_data()
                            return True
    return False

def get_course_unit_classes(username, faculty: dict, course: dict, course_unit: dict) -> List[dict]:
    for user_faculty in user.users(username)["faculties"]:
        if user_faculty["name"] == faculty['name']:
            for user_course in user_faculty["courses"]:
                if user_course["name"] == course['name']:
                    for user_course_unit in user_course["course_units"]:
                        if user_course_unit["name"] == course_unit['name']:
                            return user_course_unit["classes"]
    return []

def remove_class(username, faculty: dict, course: dict, course_unit: dict, class_name: str):
    for user_faculty in user.users(username)["faculties"]:
        if user_faculty["name"] == faculty['name']:
            for user_course in user_faculty["courses"]:
                if user_course["name"] == course['name']:
                    for user_course_unit in user_course["course_units"]:
                        if user_course_unit["name"] == course_unit['name']:
                            for user_class in user_course_unit["classes"]:
                                if user_class["name"] == class_name:
                                    user_course_unit["classes"].remove(user_class)
                                    user.store_data()
                                    return True
    return False

def get_schedule(username) -> List[dict]:
    return {
        "faculties": user.users(username)["faculties"]
    }
    schedule: List[dict] = []
    user_data = user.users(username)
    for user_faculty in user_data["faculties"]:
        for user_course in user_faculty["courses"]:
            for user_course_unit in user_course["course_units"]:
                for user_class in user_course_unit["classes"]:
                    schedule.append(user_class)
    return schedule

def add_current_schedule_interaction(username):
    user.user_interactions[username]['current_interaction'] = Interaction.ADD_SCHEDULE
    user.user_interactions[username]['current_interaction_data'] = None

def add_choose_faculty_to_add_schedule_interaction(username, faculties):
    user.user_interactions[username]['current_interaction'] = Interaction.CHOOSE_FACULTY_TO_ADD
    user.user_interactions[username]['current_interaction_data'] = faculties

def add_choose_faculty_to_edit_schedule_interaction(username, faculties):
    user.user_interactions[username]['current_interaction'] = Interaction.CHOOSE_FACULTY_TO_EDIT
    user.user_interactions[username]['current_interaction_data'] = faculties

def add_current_faculty_course_interaction(username, faculty):
    user.user_interactions[username]['current_interaction'] = Interaction.MANAGE_FACULTY
    user.user_interactions[username]['current_interaction_data'] = faculty

def add_course_interaction(username, faculty: dict, courses: List[Course]):
    user.user_interactions[username]['current_interaction'] = Interaction.ADD_COURSE
    user.user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "courses": courses
    }

def add_course_edit_schedule_interaction(username, faculty: dict, courses: List[Course]):
    user.user_interactions[username]['current_interaction'] = Interaction.EDIT_COURSE
    user.user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "courses": courses
    }

def add_current_course_course_unit_interaction(username, faculty: dict, course: dict):
    user.user_interactions[username]['current_interaction'] = Interaction.MANAGE_COURSE
    user.user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "course": course
    }

def add_add_class_unit_interaction(username, faculty: dict, course: dict, course_units: List[CourseUnit]):
    user.user_interactions[username]['current_interaction'] = Interaction.ADD_COURSE_UNIT
    user.user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "course": course,
        "course_units": course_units
    }

def add_edit_class_unit_interaction(username, faculty: dict, course: dict, course_units: List[dict]):
    user.user_interactions[username]['current_interaction'] = Interaction.EDIT_COURSE_UNIT
    user.user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "course": course,
        "course_units": course_units
    }

def add_current_course_unit_class_interaction(username, faculty: dict, course: dict, course_unit: dict):
    user.user_interactions[username]['current_interaction'] = Interaction.MANAGE_COURSE_UNIT
    user.user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "course": course,
        "course_unit": course_unit
    }

def add_choose_class_to_add_interaction(username, faculty: dict, course: dict, course_unit: dict, classes: List[Schedule]):
    user.user_interactions[username]['current_interaction'] = Interaction.ADD_CLASS
    user.user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "course": course,
        "course_unit": course_unit,
        "classes": classes
    }

def add_choose_class_to_view_interaction(username, faculty: dict, course: dict, course_unit: dict, classes: List[dict]):
    user.user_interactions[username]['current_interaction'] = Interaction.VIEW_CLASS
    user.user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "course": course,
        "course_unit": course_unit,
        "classes": classes
    }

def add_choose_class_to_remove_interaction(username, faculty: dict, course: dict, course_unit: dict, classes: List[dict]):
    user.user_interactions[username]['current_interaction'] = Interaction.REMOVE_CLASS
    user.user_interactions[username]['current_interaction_data'] = {
        "faculty": faculty,
        "course": course,
        "course_unit": course_unit,
        "classes": classes
    }