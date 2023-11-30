import user
import user_schedule
from events.interaction import Interaction
from database.database_api import api
from typing import List
from database.dbs.schema import *

def process_input(message, public):
    #Create an account for the author of the message and all those mentioned, podemos ter de mudar quando formos buscar dados ao sigarra
    user.account_checker(message.author.name)
    for util in message.mentions:
        user.account_checker(util.name)

    command = message.content.split()[0]

    return_message = None
    new_interaction = False
         
    # Checking base interaction
    if command == "!add_friend":
        if len(message.mentions) != 1:
            return_message = ["You have to mention which friend you would like to add. Ex.: !add_friend @someone", False]
        return_message = [user.send_friend_request(message.author.name, message.mentions[0].name), False]

    elif command == "!friend_requests":
        return_message = [user.check_friend_requests(message.author.name), False]
    
    elif command == "!accept":
        if len(message.content.split()) < 2:
            return_message = ["You have to specify which friend request to accept. Ex.: !accept 1", False]
        return_message = [user.accept_friend_request(message.author.name, int(message.content.split()[1])), False]
    
    elif command == "!remove_friend":
        if len(message.content.split()) < 2:
            return_message = ["You have to specify which friend to remove. Ex.: !remove_friend @someone", False]
        if len(message.mentions) != 1:
            return_message = ["You have to mention which friend you would like to remove. Ex.: !remove_friend @someone", False]
        
        return_message = [user.remove_friend(message.author.name, message.mentions[0].name), False]
    
    elif command == "!friends_list":
        return_message = [user.show_friends_list(message.author.name), False]
    
    elif command == "!add_session_cookie":
        if public:
            return_message = ["This is sensitive private information! Please only use this command on private DM's!", True]
        if len(message.content.split()) < 2:
            return_message = ["You have to input your session cookie. Ex.: !add_session_cookie <cookie>", False]
        return_message = [user.add_cookie(message.author.name, int(message.content.split()[1])), True]
    
    elif command == "!add_username":
        if public:
            return_message = ["This is sensitive private information! Please only use this command on private DM's!", True]
        if len(message.content.split()) < 2:
                return_message = ["You have to input your username. Ex.: !add_username <username>", False]
        return_message = [user.add_username(message.author.name, message.content.split()[1]), True]

    elif command == "!add_password":
        if public:
            return_message = ["This is sensitive private information! Please only use this command on private DM's!", True]
        if len(message.content.split()) < 2:
                return_message = ["You have to input your password. Ex.: !add_password <password>", False]
        return_message = [user.add_password(message.author.name, message.content.split()[1]), True]

    elif command == "!help":
        return_message = ["Available commands:\n!add_friend\n!friend_requests\n!accept\n!friends_list\n!remove_friend\n!add_session_cookie", False]

    elif command == "!add_schedule":
        title = "Add schedule"
        options = ["Adicionar faculdade", "Escolher faculdade para editar horario", "Editar horario de curso"]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_schedule_interaction(message.author.name)
        new_interaction = True
        return_message = [formated_output, False]

    elif command == "!view_schedule":
        return_message = process_view_schedule(message)


    if return_message is not None:
        if not new_interaction:
            user.cancel_current_interaction(message.author.name)
        return return_message
    

    # Continuing interaction
    if user.has_current_interaction(message.author.name):        
        if command == "!cancel":
            user.cancel_current_interaction(message.author.name)
            return ["Canceled", False]
        
        interaction = user.get_current_interaction(message.author.name)
        if interaction == Interaction.ADD_SCHEDULE:
            return process_add_schedule(message, public, command)

        elif interaction == Interaction.CHOOSE_FACULTY_TO_ADD:
            return process_choose_faculty_to_add(message, public, command)

        elif interaction == Interaction.CHOOSE_FACULTY_TO_EDIT:
            return process_choose_faculty_to_edit(message, public, command)
        
        elif interaction == Interaction.MANAGE_FACULTY:
            return process_manage_faculty_courses(message, public, command)
        
        elif interaction == Interaction.ADD_COURSE:
            return process_add_course(message, public, command)
        
        elif interaction == Interaction.EDIT_COURSE:
            return process_edit_course(message, public, command)
        
        elif interaction == Interaction.MANAGE_COURSE:
            return process_manage_course_course_units(message, public, command)
        
        elif interaction == Interaction.ADD_COURSE_UNIT:
            return process_choose_course_unit_to_add(message, public, command)
        
        elif interaction == Interaction.EDIT_COURSE_UNIT:
            return process_choose_course_unit_to_edit(message, public, command)
        
        elif interaction == Interaction.MANAGE_COURSE_UNIT:
            return process_manage_course_unit_classes(message, public, command)
        
        elif interaction == Interaction.ADD_CLASS:
            return process_add_class(message, public, command)
        
        elif interaction == Interaction.VIEW_CLASS:
            return process_view_class(message, public, command)
        
        elif interaction == Interaction.REMOVE_CLASS:
            return process_remove_class(message, public, command)

    return ["Unknown command", False]

def process_view_schedule(message):
    schedule : List[dict] = user_schedule.get_schedule(message.author.name)
    has_faculties = False
    has_courses = False
    has_course_units = False
    has_classes = False

    faculties = schedule['faculties']
    schedules_classes = {}
    for faculty in faculties:
        faculty_string = f"{faculty['name']}"
        schedules_classes[faculty_string] = schedules_classes.get(faculty_string, {})
        schedules_faculty = schedules_classes[faculty_string]
        courses = faculty['courses']
        for course in courses:
            course_string = f"{course['name']}"
            schedules_faculty[course_string] = schedules_faculty.get(course_string, {})
            schedules_course = schedules_faculty[course_string]
            course_units = course['course_units']
            for course_unit in course_units:
                course_unit_string = f"{course_unit['name']}"
                schedules_course[course_unit_string] = schedules_course.get(course_unit_string, [])
                classes = course_unit['classes']
                for class_ in classes:
                    class_string = f"{class_['name']}({class_['lesson_type']}): {format_day(class_['day'])} {format_time(class_['start_time'])}-{format_time(class_['start_time'] + class_['duration'])} in {class_['location']}"
                    schedules_classes[faculty_string][course_string][course_unit_string].append(class_string)

                if len(schedules_classes[faculty_string][course_string][course_unit_string]) == 0:
                    del schedules_classes[faculty_string][course_string][course_unit_string]

            if len(schedules_classes[faculty_string][course_string]) == 0:
                del schedules_classes[faculty_string][course_string]

        if len(schedules_classes[faculty_string]) == 0:
            del schedules_classes[faculty_string]      
    if len(schedules_classes) == 0:
            del schedules_classes

    return_string = ""
    if schedules_classes is None:
        return_message = ["You have no schedule", False]
    else:
        for faculty in schedules_classes:
            return_string += f"{faculty} "
            if len(schedules_classes[faculty]) > 1:
                return_string += "\n"
                faculty_ident = "\t"
            else:
                faculty_ident = ""
            for course in schedules_classes[faculty]:
                return_string += f"{faculty_ident}{course} "
                if len(schedules_classes[faculty][course]) > 1:
                    return_string += f"\n"
                    course_ident = faculty_ident + "\t"
                else:
                    course_ident = faculty_ident
                for course_unit in schedules_classes[faculty][course]:
                    return_string += f"{course_ident}{course_unit}\n"
                    if len(schedules_classes[faculty][course][course_unit]) > 1:
                        course_unit_ident = course_ident + "\t"
                    else:
                        course_unit_ident = course_ident
                    for class_ in schedules_classes[faculty][course][course_unit]:
                        class_ident = course_unit_ident + "\t"
                        return_string += f"{class_ident}{class_}\n"
                


        return_message = [return_string, False]
    return return_message

def process_add_schedule(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    if option_chosen == 1:
        faculties: List[Faculty] = api.get_faculties()
        title = "Faculdades disponiveis"
        options = [f"{faculty.acronym}: {faculty.name.strip()}" for faculty in faculties]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_choose_faculty_to_add_schedule_interaction(message.author.name, faculties)
        return [formated_output, False]
    elif option_chosen == 2:
        faculties: List[dict] = user_schedule.get_faculties(message.author.name)
        title = "Inscrito em faculdades"
        options = [f"{faculty['name']}: {faculty['full_name'].strip()}" for faculty in faculties]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_choose_faculty_to_edit_schedule_interaction(message.author.name, faculties)
        return [formated_output, False]
    elif option_chosen == 0:
        user.cancel_current_interaction(message.author.name)
        return ["Canceled", False]
    return ["Option not recognized", False]

def process_choose_faculty_to_add(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    faculties = user.get_current_interaction_data(message.author.name)
    if option_chosen < 0 or option_chosen > len(faculties):
        return ["Option not recognized", False]
    faculty: List[Faculty] = faculties[option_chosen-1]
    added = user_schedule.add_faculty(message.author.name, faculty)

    if option_chosen != 0:
        if added:
            pre_title = f"Added {faculty.acronym}: {faculty.name.strip()}"
        else:
            pre_title = f"You already added {faculty.acronym}: {faculty.name.strip()}"
    else:
        pre_title = ""
    title = "Add schedule"
    options = ["Adicionar faculdade", "Escolher faculdade para editar horario", "Editar horario de curso"]
    formated_output = format_output_with_cancel(pre_title + '\n\n' + title, options)
    user_schedule.add_current_schedule_interaction(message.author.name)
    return [formated_output, False]

def process_choose_faculty_to_edit(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    faculties = user.get_current_interaction_data(message.author.name)
    if option_chosen < 0 or option_chosen > len(faculties):
        return ["Option not recognized", False]
    
    if option_chosen == 0:
        title = "Add schedule"
        options = ["Adicionar faculdade", "Escolher faculdade para editar horario", "Editar horario de curso"]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_schedule_interaction(message.author.name)
        return [formated_output, False]
    
    faculty: dict = faculties[option_chosen-1]
    title = f"Escolheste a faculdade {faculty['name']}: {faculty['full_name'].strip()}"
    options = ["Adicionar curso", "Editar horario de curso"]
    formated_output = format_output_with_cancel(title, options)
    user_schedule.add_current_faculty_course_interaction(message.author.name, faculty)
    return [formated_output, False]

def process_manage_faculty_courses(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    faculty: dict = user.get_current_interaction_data(message.author.name)
    if option_chosen == 1:
        courses: Course = api.get_faculty_courses(faculty['name'])
        title = f"Cursos disponiveis em {faculty['name']}: {faculty['full_name'].strip()}"
        options = [f"{course.name.strip()}" for course in courses]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_course_interaction(message.author.name, faculty, courses)
        return [formated_output, False]
    elif option_chosen == 2:
        # List current faculty courses
        courses = user_schedule.get_faculty_courses(message.author.name, faculty)
        title = f"Escolher curso de {faculty['name']} para editar horario"
        options = [f"{course['name']}: {course['full_name'].strip()}" for course in courses]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_course_edit_schedule_interaction(message.author.name, faculty, courses)
        return [formated_output, False]
    elif option_chosen == 0:
        title = "Add schedule"
        options = ["Adicionar faculdade", "Escolher faculdade para editar horario", "Editar horario de curso"]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_schedule_interaction(message.author.name)
        return [formated_output, False]
    return ["Option not recognized", False]

def process_add_course(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    data = user.get_current_interaction_data(message.author.name)
    faculty: dict = data['faculty']
    courses: List[Course] = data['courses']
    if option_chosen < 0 or option_chosen > len(courses):
        return ["Option not recognized", False]
    course: Course = courses[option_chosen-1]
    added = user_schedule.add_course(message.author.name, faculty, course)

    if option_chosen != 0:
        if added:
            pre_title = f"Added {course.acronym}: {course.name.strip()}"
        else:   
            pre_title = f"You already added {course.acronym}: {course.name.strip()}"
    else:
        pre_title = ""

    title = f"Escolheste a faculdade {faculty['name']}: {faculty['full_name'].strip()}"
    options = ["Adicionar curso", "Editar horario de curso"]
    formated_output = format_output_with_cancel(pre_title + '\n\n' + title, options)
    user_schedule.add_current_faculty_course_interaction(message.author.name, faculty)
    return [formated_output, False]

def process_edit_course(message, public, command):

    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    data = user.get_current_interaction_data(message.author.name)
    courses: List[dict] = data['courses']
    faculty: dict = data['faculty']
    if option_chosen < 0 or option_chosen > len(courses):
        return ["Option not recognized", False]
    
    if option_chosen == 0:
        title = f"Escolheste a faculdade {faculty['name']}: {faculty['full_name'].strip()}"
        options = ["Adicionar curso", "Editar horario de curso"]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_faculty_course_interaction(message.author.name, faculty)
        return [formated_output, False]

    course: dict = courses[option_chosen-1]
    title = f"Escolheste o curso {course['name']}: {course['full_name'].strip()}"
    options = ["Adicionar cadeira", "Editar horario de cadeira"]
    formated_output = format_output_with_cancel(title, options)
    user_schedule.add_current_course_course_unit_interaction(message.author.name, faculty, course)
    return [formated_output, False]

def process_manage_course_course_units(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    data = user.get_current_interaction_data(message.author.name)
    faculty: dict = data['faculty']
    course: dict = data['course']

    if option_chosen == 1:
        course_unit_year_course_units: List[Object] = api.get_course_course_units(course['id'])
        course_unit_years: List[CourseUnitYear] = [object_.CourseUnitYear for object_ in course_unit_year_course_units]
        course_units: List[CourseUnit] = [object_.CourseUnit for object_ in course_unit_year_course_units]
        title = f"Cadeiras disponiveis em {course['name']}: {course['full_name'].strip()}"
        options = [f"{course_unit.name.strip()}: {course_unit_year.course_unit_year} year;  {course_unit.semester} Semester ({course_unit.year})" for course_unit_year, course_unit in zip(course_unit_years, course_units)]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_add_class_unit_interaction(message.author.name, faculty, course, course_unit_year_course_units)
        return [formated_output, False]
    elif option_chosen == 2:
        course_unit_year_course_units: List[dict] = user_schedule.get_course_course_units(message.author.name, faculty, course)
        title = f"Escolher cadeira de {course['name']} para editar horario"
        options = [f"{course_unit['name'].strip()}: {course_unit['year']} year;  {course_unit['semester']} Semester" for course_unit in course_unit_year_course_units]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_edit_class_unit_interaction(message.author.name, faculty, course, course_unit_year_course_units)
        return [formated_output, False]
    elif option_chosen == 0:
        title = f"Escolheste a faculdade {faculty['name']}: {faculty['full_name'].strip()}"
        options = ["Adicionar curso", "Editar horario de curso"]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_faculty_course_interaction(message.author.name, faculty)
        return [formated_output, False]

    return ["Option not recognized", False]

def process_choose_course_unit_to_add(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    data = user.get_current_interaction_data(message.author.name)
    faculty: dict = data['faculty']
    course: dict = data['course']
    course_unit_year_course_units: List[Object] = data['course_units']
    if option_chosen < 0 or option_chosen > len(course_unit_year_course_units):
        return ["Option not recognized", False]
    
    if option_chosen != 0:
        course_unit_year_course_unit: Object = course_unit_year_course_units[option_chosen-1]
        course_unit: CourseUnit = course_unit_year_course_unit.CourseUnit
        course_unit_year: CourseUnitYear = course_unit_year_course_unit.CourseUnitYear
        added = user_schedule.add_course_unit(message.author.name, faculty, course, course_unit_year_course_unit)

        if added:
            pre_title = f"Added {course_unit.acronym}: {course_unit.name.strip()}"
        else:
            pre_title = f"You already added {course_unit.acronym}: {course_unit.name.strip()}"
    else:
        pre_title = ""
    title = f"Escolheste o curso {course['name']}: {course['full_name'].strip()}"
    options = ["Adicionar cadeira", "Editar horario de cadeira"]
    formated_output = format_output_with_cancel(pre_title + '\n\n' + title, options)
    user_schedule.add_current_course_course_unit_interaction(message.author.name, faculty, course)
    return [formated_output, False]

def process_choose_course_unit_to_edit(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    data = user.get_current_interaction_data(message.author.name)
    faculty: dict = data['faculty']
    course: dict = data['course']
    course_unit_year_course_units: List[dict] = data['course_units']

    if option_chosen == 0:
        title = f"Escolheste o curso {course['name']}: {course['full_name'].strip()}"
        options = ["Adicionar cadeira", "Editar horario de cadeira"]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_course_course_unit_interaction(message.author.name, faculty, course)
        return [formated_output, False]

    if option_chosen < 0 or option_chosen > len(course_unit_year_course_units):
        return ["Option not recognized", False]
    
    course_unit: dict = course_unit_year_course_units[option_chosen-1]
    title = f"Escolheste a cadeira {course_unit['name']}: {course_unit['acronym'].strip()}"
    options = ["Adicionar aula", "Ver horarios de aula", "Remover aula"]
    formated_output = format_output_with_cancel(title, options)
    user_schedule.add_current_course_unit_class_interaction(message.author.name, faculty, course, course_unit)
    return [formated_output, False]

def process_manage_course_unit_classes(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    data = user.get_current_interaction_data(message.author.name)
    faculty: dict = data['faculty']
    course: dict = data['course']
    course_unit: dict = data['course_unit']
    if option_chosen == 1:
        classes_: List[Schedule] = api.get_course_unit_schedules(course_unit['id'])
        title = f"Adicionar aula a {course_unit['name']}: {course_unit['acronym'].strip()}"
        options = [f"{class_.class_name}({class_.lesson_type}): {format_day(class_.day)} {format_time(class_.start_time)}-{format_time(class_.start_time + class_.duration)} in {class_.location}" for class_ in classes_]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_choose_class_to_add_interaction(message.author.name, faculty, course, course_unit, classes_)
        return [formated_output, False]
    elif option_chosen == 2 or option_chosen == 3:
        classes_: List[dict] = user_schedule.get_course_unit_classes(message.author.name, faculty, course, course_unit)
        options = [f"{class_['name']}({class_['lesson_type']}): {format_day(class_['day'])} {format_time(class_['start_time'])}-{format_time(class_['start_time'] + class_['duration'])} in {class_['location']}" for class_ in classes_]
        if option_chosen == 2:
            title = f"Horarios de aula de {course_unit['name']}: {course_unit['acronym'].strip()}"
            user_schedule.add_choose_class_to_view_interaction(message.author.name, faculty, course, course_unit, classes_)
        elif option_chosen == 3:
            title = f"Remover aula de {course_unit['name']}: {course_unit['acronym'].strip()}"
            user_schedule.add_choose_class_to_remove_interaction(message.author.name, faculty, course, course_unit, classes_)
        formated_output = format_output_with_cancel(title, options)
        return [formated_output, False]
    elif option_chosen == 0:
        title = f"Escolheste o curso {course['name']}: {course['full_name'].strip()}"
        options = ["Adicionar cadeira", "Editar horario de cadeira"]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_course_course_unit_interaction(message.author.name, faculty, course)
        return [formated_output, False]

def process_add_class(message, public, command):
    option_chosen = get_option_chosen(command)

    if option_chosen == -1:
        return ["Option not recognized", False]
    data = user.get_current_interaction_data(message.author.name)
    faculty: dict = data['faculty']
    course: dict = data['course']
    course_unit_year_course_unit: dict = data['course_unit']
    classes_ : List[Schedule]= data['classes']
    
    if option_chosen < 0 or option_chosen > len(classes_):
        return ["Option not recognized", False]
    
    if option_chosen != 0:
        class_: Schedule = classes_[option_chosen-1]
        added = user_schedule.add_class(message.author.name, faculty, course, course_unit_year_course_unit, class_)
        if added:
            pre_title = f"Added {class_.class_name}: {class_.lesson_type}"
        else:
            pre_title = f"You already added {class_.class_name}: {class_.lesson_type}"
    else:
        pre_title = ""

    title = f"Escolheste a cadeira {course_unit_year_course_unit['name']}: {course_unit_year_course_unit['acronym'].strip()}"
    options = ["Adicionar aula", "Ver horarios de aula", "Remover aula"]
    formated_output = format_output_with_cancel(pre_title + '\n\n' + title, options)
    user_schedule.add_current_course_unit_class_interaction(message.author.name, faculty, course, course_unit_year_course_unit)
    return [formated_output, False]

def process_view_class(message, public, command):
    option_chosen = get_option_chosen(command)

    if option_chosen == 0:
        data = user.get_current_interaction_data(message.author.name)
        faculty: dict = data['faculty']
        course: dict = data['course']
        course_unit: dict = data['course_unit']
        title = f"Escolheste a cadeira {course_unit['name']}: {course_unit['acronym'].strip()}"
        options = ["Adicionar aula", "Ver horarios de aula", "Remover aula"]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_course_unit_class_interaction(message.author.name, faculty, course, course_unit)
        return [formated_output, False]
    else:
        return ["Option not recognized", False]
    
def process_remove_class(message, public, command):
    option_chosen = get_option_chosen(command)

    if option_chosen == -1:
        return ["Option not recognized", False]
    data = user.get_current_interaction_data(message.author.name)
    faculty: dict = data['faculty']
    course: dict = data['course']
    course_unit: dict = data['course_unit']
    classes_ : List[dict]= data['classes']
    if option_chosen == 0:
        options = ["Adicionar aula", "Ver horarios de aula", "Remover aula"]
        title = f"Escolheste a cadeira {course_unit['name']}: {course_unit['acronym'].strip()}"
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_course_unit_class_interaction(message.author.name, faculty, course, course_unit)
        return [formated_output, False]
    
    if option_chosen < 0 or option_chosen > len(classes_):
        return ["Option not recognized", False]
    
    class_: dict = classes_[option_chosen-1]
    removed = user_schedule.remove_class(message.author.name, faculty, course, course_unit, class_)
    if removed:
        pre_title = f"Removed {class_['name']}: {class_['lesson_type']}"
    else:
        pre_title = f"You already removed {class_['name']}: {class_['lesson_type']}"
    title = f"Escolheste a cadeira {course_unit['name']}: {course_unit['acronym'].strip()}"
    options = ["Adicionar aula", "Ver horarios de aula", "Remover aula"]
    formated_output = format_output_with_cancel(pre_title + '\n\n' + title, options)
    user_schedule.add_current_course_unit_class_interaction(message.author.name, faculty, course, course_unit)
    return [formated_output, False]

def get_option_chosen(command):
    option_chosen = command[1:].strip()
    try:
        option_chosen = int(option_chosen)
    except:
        return -1
    return option_chosen

def format_output(title, options):
    numbered_options = [f'{index+1}: {elm}' for index, elm in enumerate(options)] 
    output = title + '\n' + '\n'.join(numbered_options)
    return output

def format_output_with_cancel(title, options):
    numbered_options = [f'{index+1}: {elm}' for index, elm in enumerate(options)] 
    output = title + '\n' + '\n'.join(numbered_options) + '\n' + "0: Cancel"
    return output

def format_day(day_index):
    days = ["2ª", "3ª", "4ª", "5ª", "6ª"]
    day_str = f"{days[day_index-1]} feira"
    return day_str

def format_time(start_time):
    hours = int(start_time//60)
    minutes = int(start_time%60)
    start_time_str = f"{hours:02d}:{minutes:02d}"
    return start_time_str