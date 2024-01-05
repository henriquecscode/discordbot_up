import os
from database.database import Database, Param
from database.dbs.schema import *
from typing import List, Tuple, Any
from dotenv import load_dotenv
load_dotenv()
FACULTY_ID = 'acronym'
COURSE_ID = 'id'
COURSE_UNIT_ID = 'id'
class Database_API:   
    def __init__(self, db: Database):
        self.db =  db

    def _get_faculties(self):
        return self.db.get_all('faculty')
    
    def get_faculties(self) -> List[Faculty]:
        faculties = self._get_faculties()
        faculty_objects = [Faculty(faculty) for faculty in faculties]
        return faculty_objects

    def _get_faculty(self, id):
        return self.db.get_by_param('faculty', Param(FACULTY_ID, id))

    def _get_courses(self):
        return self.db.get_all('course')

    def _get_faculty_courses(self, faculty_id):
        return self.db.get_join_all_by_param('faculty', 'course', 'acronym', 'faculty_id', Param(f"faculty.{FACULTY_ID}", faculty_id)) #TODO Check
    
    def get_faculty_courses(self, faculty_id) -> List[Course]:
        faculty_courses = self._get_faculty_courses(faculty_id)
        faculty_courses_objects = Database_API.get_objects([Faculty, Course], faculty_courses)
        course_objects = [object.Course for object in faculty_courses_objects]
        return course_objects
    
    def _get_course_course_units_year(self, course_id):
        return self.db.get_join_all_by_param('course', 'course_metadata', 'id', 'course_id', Param(f"course.{COURSE_ID}", course_id))
    
    def _get_course_course_unit(self, course_id):
        course_units = self.db.n_join_by_params(["course", "course_metadata", "course_unit"], [["id", "course_id"], ["course_unit_id", "id"]], [Param(f"course.{COURSE_ID}", course_id)], ["course_metadata", "course_unit"])
        return course_units
    
    def get_course_course_units(self, course_id) -> List[Object]:
        course_units = self._get_course_course_unit(course_id)
        course_units_objects = Database_API.get_objects([CourseUnitYear, CourseUnit], course_units)
        return course_units_objects
    
    def _get_course_unit_schedules(self, course_unit_id):
        return self.db.get_join_all_by_param('course_unit', 'schedule', 'id', 'course_unit_id', Param(f"course_unit.{COURSE_UNIT_ID}", course_unit_id))
    
    def get_course_unit_schedules(self, course_unit_id) -> List[Schedule]:
        course_unit_schedules = self._get_course_unit_schedules(course_unit_id)
        course_unit_schedules_objects = Database_API.get_objects([CourseUnit, Schedule], course_unit_schedules)
        schedule_objects = [object.Schedule for object in course_unit_schedules_objects]
        return schedule_objects
    
    @staticmethod
    def get_objects(classes: List[Table], data: List[Tuple[Any]]) -> List[Object]:
        objects = [Object(classes, args) for args in data]
        return objects
    

db_path = os.getenv("DB_PATH")
print(f"DB_PATH: {db_path}")
db = Database(db_path)
api = Database_API(db)
