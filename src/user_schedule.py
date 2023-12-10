import pymongo
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
    user_course_cur = user.users_col.aggregate([
        {"$match": { "id": username }},
        {"$unwind": "$faculties"},
        {"$match": { "faculties.name": faculty['name'] }},
        {"$unwind": "$faculties.courses"},
        {"$match": { "faculties.courses.acronym": course.acronym }},
        {"$group": { "_id": "$faculties.courses" }}
        ])
    user_courses = list(user_course_cur)

    if len(user_courses) > 0:
        return False
    
    course_data = {
    "id": course.id,
    "acronym": course.acronym,
    "name": course.name,
    "course_units": []
    }
    
    user.users_col.update_one({"id": username}, {"$push": {"faculties.$[faculty].courses": course_data}}, array_filters=[{"faculty.name": faculty['name']}])
    return True

def get_faculty_courses(username, faculty: dict) -> List[dict]:
    # user_faculty = user.users_col.find_one({"id": username}, {"faculties.$[faculty].courses": 1}, array_filters=[{"faculty.name": faculty['name']}])
    # user_faculty = user.users_col.find_one({"id": username, "faculties.name": faculty['name']}, {"faculties.$.courses": 1})

    user_courses = user.users_col.aggregate([
        { "$match": { "id": username } },
        { "$unwind": "$faculties" },
        { "$match": { "faculties.name": faculty['name'] } },
        { "$unwind": "$faculties.courses" },
        { "$replaceRoot": { "newRoot": "$faculties.courses" } },
    ])  
    user_courses = list(user_courses)
    return user_courses

def add_course_unit(username, faculty: dict, course: dict, course_unit_course_unit_year: Object):
    course_unit: CourseUnit = course_unit_course_unit_year.CourseUnit
    course_unit_year: CourseUnitYear = course_unit_course_unit_year.CourseUnitYear
    user_course_unit_cur = user.users_col.aggregate([
        {"$match": { "id": username }},
        {"$unwind": "$faculties"},
        {"$match": { "faculties.name": faculty['name'] }},
        {"$unwind": "$faculties.courses"},
        {"$match": { "faculties.courses.name": course['name'] }},
        {"$unwind": "$faculties.courses.course_units"},
        {"$match": { "faculties.courses.course_units.id": course_unit.id, "faculties.courses.course_units.year": course_unit_year.course_unit_year }},
        {"$group": { "_id": "$faculties.courses.course_units" }}
    ])

    user_course_units = list(user_course_unit_cur)
    if len(user_course_units) > 0:
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
    user.users_col.update_one({"id": username}, {"$push": {"faculties.$[faculty].courses.$[course].course_units": course_unit_data}}, array_filters=[{"faculty.name": faculty['name']}, {"course.acronym": course['acronym']}])
    return True

def get_course_course_units(username, faculty: dict, course: dict) -> List[dict]:
    user_course_units = user.users_col.aggregate([

        { "$match": { "id": username } },
        { "$unwind": "$faculties" },
        { "$match": { "faculties.name": faculty['name'] } },
        { "$unwind": "$faculties.courses" },
        { "$match": { "faculties.courses.name": course['name'] } },
        { "$unwind": "$faculties.courses.course_units" },
        { "$replaceRoot": { "newRoot": "$faculties.courses.course_units" } },
    ])
    user_course_units = list(user_course_units)
    return user_course_units


def add_class(username, faculty: dict, course: dict, course_unit: dict, schedule: Schedule):
    user_class_cur = user.users_col.aggregate([
        {"$match": { "id": username }},
        {"$unwind": "$faculties"},
        {"$match": { "faculties.name": faculty['name'] }},
        {"$unwind": "$faculties.courses"},
        {"$match": { "faculties.courses.name": course['name'] }},
        {"$unwind": "$faculties.courses.course_units"},
        {"$match": { "faculties.courses.course_units.id": course_unit['id'], "faculties.courses.course_units.year": course_unit['year'] }},
        {"$unwind": "$faculties.courses.course_units.classes"},
        {"$match": { "faculties.courses.course_units.classes.id": schedule.id }},
        {"$group": { "_id": "$faculties.courses.course_units.classes" }}
    ])

    user_classes = list(user_class_cur)
    if len(user_classes) > 0:
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
    user.users_col.update_one({"id": username}, {"$push": {"faculties.$[faculty].courses.$[course].course_units.$[courseunit].classes": class_data}}, array_filters=[{"faculty.name": faculty['name']}, {"course.acronym": course['acronym']}, {"courseunit.id": course_unit['id'], "courseunit.year" : course_unit['year']}])
    return True

def get_course_unit_classes(username, faculty: dict, course: dict, course_unit: dict) -> List[dict]:
    user_classes = user.users_col.aggregate([
        { "$match": { "id": username } },
        { "$unwind": "$faculties" },
        { "$match": { "faculties.name": faculty['name'] } },
        { "$unwind": "$faculties.courses" },
        { "$match": { "faculties.courses.acronym": course['acronym'] } },
        { "$unwind": "$faculties.courses.course_units" },
        { "$match": {"$and": [
                     { "faculties.courses.course_units.id": course_unit['id'] }, 
                     {"faculties.courses.course_units.year": course_unit['year']} 
                     ]}},
        { "$unwind": "$faculties.courses.course_units.classes" },
        { "$replaceRoot": { "newRoot": "$faculties.courses.course_units.classes" } },
    ])

    user_classes = list(user_classes)
    return user_classes


def remove_class(username, faculty: dict, course: dict, course_unit: dict, class_: dict):
    a : pymongo.results.UpdateResult = user.users_col.update_one(
        {"id": username},
        {"$pull": {"faculties.$[faculty].courses.$[course].course_units.$[courseunit].classes": {"id": class_['id']}}},
        array_filters=[{"faculty.name": faculty['name']}, {"course.acronym": course['acronym']}, {"courseunit.name": course_unit['name'], "courseunit.year" : course_unit['year']}])
    
    if a.modified_count > 0:
        return True
    return False

def get_schedule(username) -> List[dict]:
    return  user.users_col.find_one({"id": username}, {"faculties": 1})
    schedule: List[dict] = []
    user_data = user.users(username)
    for user_faculty in user_data["faculties"]:
        for user_course in user_faculty["courses"]:
            for user_course_unit in user_course["course_units"]:
                for user_class in user_course_unit["classes"]:
                    schedule.append(user_class)
    return schedule

def add_manual_schedule(usernames, institution, course_unit, lesson_type, day, start_time, duration, location):
    class_data = {
        institution: institution,
        "name": course_unit,
        "lesson_type": lesson_type,
        "day": day,
        "start_time": start_time,
        "duration": duration,
        "location": location,
    }
    user.users_col.update_one({"id": usernames}, {"$push": {"data.schedule": class_data}})

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

def add_schedule_manually_interaction(username):
    user.user_interactions[username]['current_interaction'] = Interaction.ADD_SCHEDULE_MANUALLY
    user.user_interactions[username]['current_interaction_data'] = None

def add_confirm_add_class_interaction(username, institution, course_unit, lesson_type, day, start_time, duration, location):
    user.user_interactions[username]['current_interaction'] = Interaction.CONFIRM_ADD_CLASS
    user.user_interactions[username]['current_interaction_data'] = {
        "institution": institution,
        "course_unit": course_unit,
        "lesson_type": lesson_type,
        "day": day,
        "start_time": start_time,
        "duration": duration,
        "location": location
    }

