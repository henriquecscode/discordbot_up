from typing import List, Any
import datetime
strptime = datetime.datetime.strptime
str_format = '%Y-%m-%d %H:%M:%S.%f'

class Table:
    num_columns: int = None
class Faculty(Table):
    num_columns = 3
    def __init__(self, args) -> None:
        self.acronym: str = args[0]
        self.name: str = args[1]
        self.date = strptime(args[2], str_format)
        self.key = self.acronym

class Course(Table):
    num_columns = 10
    def __init__(self, args) -> None:
        self.id: int = args[0]
        self.faculty_id: str = args[1]
        self.sigarra_id: str = args[2]
        self.name: str = args[3]
        self.acronym: str = args[4]
        self.course_type: str = args[5]
        self.year: str = args[6]
        self.url: str  = args[7]
        self.plan = args[8]
        self.date = strptime(args[9], str_format)
        self.key = self.id


class CourseUnitYear(Table):
    num_columns = 4
    def __init__(self, args) -> None:
        self.course_id: int = args[0]
        self.course_unit_id: int = args[1]
        self.course_unit_year:int = args[2]
        self.ects:int = args[3]

        self.key = (self.course_id, self.course_unit_id, self.course_unit_year)

class CourseUnit(Table):
    num_columns = 10
    def __init__(self, args) -> None:
        self.id: int = args[0]
        self.sigarra_id: str = args[1]
        self.course_id: int = args[2]
        self.name: str = args[3]
        self.acronym: str = args[4]
        self.url: str = args[5]
        self.semester: str = args[6]
        self.year: str = args[7]
        self.schedule: str = args[8]
        self.last_updated = strptime(args[9], str_format)
        self.key = self.id

class Schedule(Table):
    num_columns=12
    def __init__(self, args) -> None:
        self.id: int = args[0]
        self.day: int = args[1]
        self.duration: int= args[2]*60 # Minutes
        self.start_time: int = args[3]*60 # Minutes in the day
        self.location: str = args[4]
        self.less_type: str = args[5]
        self.is_composed: bool = args[6]
        self.professor_sigarra_id: str = args[7]
        self.course_unit_id: int = args[8]
        self.last_updated = strptime(args[9], str_format)
        self.class_name = args[10]
        self.composed_class_name = args[11]
        self.key = self.id

class Object:
    def __init__(self, classes: List[Table], args):
        self.classes = classes
        column = 0
        for i, class_ in enumerate(classes):
            setattr(self, class_.__name__, class_(args[column:column+class_.num_columns]))
            column += class_.num_columns




