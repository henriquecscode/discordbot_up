# Open database

import sqlite3
from src.database.database_api import Database_API as DBAPI
from src.database.database import Database
from src.database.dbs.schema import *

db_path= './database/dbs/database.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


if __name__ == "__main__":
    db = Database(db_path)
    api = DBAPI(db)
    faculties = api.get_faculties()
    feup_courses = api.get_faculty_courses('feup')
    course = feup_courses[0]
    course_id = course[0]
    # course_units_year = api.get_course_course_units_year(course_id)
    get_course_course_unit = api.get_course_course_unit(course_id)
    get_course_unit_schedule = api.get_course_unit_schedule(get_course_course_unit[0][14])
    objects = DBAPI.get_objects([CourseUnit, Schedule], get_course_unit_schedule)
    print(objects)
    exit(0)


# -- select * from faculty join course on faculty.acronym=course.faculty_id where faculty.acronym="feup";
# -- select * from (select * from faculty join course  on faculty.acronym=course.faculty_id where faculty.acronym="feup") as feup_courses join course_metadata on feup_courses.id = course_metadata.course_id order by name
# select * from (
#     select * from (
#         select * from 
#         faculty join
#         course 
#         on faculty.acronym=course.faculty_id 
#         where faculty.acronym="feup"
#         ) as feup_courses
#     join course_metadata
#     on feup_courses.id = course_metadata.course_id
#     ) as feup_units
# join course_unit
# on feup_units.course_unit_id = course_unit.id 
# order by feup_units.course_id
