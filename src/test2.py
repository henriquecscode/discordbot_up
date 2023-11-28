from dotenv import load_dotenv
load_dotenv()
from database.database_api import api

if __name__== "__main__":
    course_units = api.get_course_course_units(68)
    exit(0)