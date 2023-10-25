from src.database.database import Database, Param
from src.database.dbs.schema import *
from typing import List, Tuple, Any

FACULTY_ID = 'acronym'
COURSE_ID = 'id'
COURSE_UNIT_ID = 'id'
class Database_API(Database):   
    def __init__(self, db: Database):
        self.db =  db

    def get_faculties(self):
        return self.db.get_all('faculty')

    def get_faculty(self, id):
        return self.db.get_by_param('faculty', Param(FACULTY_ID, id))

    def get_courses(self):
        return self.db.get_all('course')

    def get_faculty_courses(self, faculty_id):
        return self.db.get_join_all_by_param('course', 'faculty', 'faculty_id', 'acronym', Param(f"faculty.{FACULTY_ID}", faculty_id)) #TODO Check
    
    def get_course_course_units_year(self, course_id):
        return self.db.get_join_all_by_param('course', 'course_metadata', 'id', 'course_id', Param(f"course.{COURSE_ID}", course_id))
    
    def get_course_course_unit(self, course_id):
        course_units = self.db.n_join_by_params(["course", "course_metadata", "course_unit"], [["id", "course_id"], ["course_unit_id", "id"]], [Param(f"course.{COURSE_ID}", course_id)])
        return course_units
    
    def get_course_unit_schedule(self, course_unit_id):
        return self.db.get_join_all_by_param('course_unit', 'schedule', 'id', 'id', Param(f"course_unit.{COURSE_UNIT_ID}", course_unit_id))
    
    @staticmethod
    def get_objects(classes: List[Table], data: List[Tuple[Any]]):
        objects = [Object(classes, args) for args in data]
        return objects
