import user
from events.interaction import Interaction
from database.database_api import api
from typing import List
from database.dbs.schema import *
from datetime import datetime

def process_input(message, public):
    #Create an account for the author of the message and all those mentioned, podemos ter de mudar quando formos buscar dados ao sigarra
    user.account_checker(message.author.name)
    for util in message.mentions:
        user.account_checker(util.name)

    command = message.content.split()[0]
    if not user.has_current_interaction(message.author.name):
         
        if command == "!add_friend":
            if len(message.mentions) != 1:
                return ["You have to mention which friend you would like to add. Ex.: !add_friend @someone", False]
            return [user.send_friend_request(message.author.name, message.mentions[0].name), False]

        if command == "!friend_requests":
            return [user.check_friend_requests(message.author.name), False]
        
        if command == "!accept":
            if len(message.content.split()) < 2:
                return ["You have to specify which friend request to accept. Ex.: !accept 1", False]
            return [user.accept_friend_request(message.author.name, int(message.content.split()[1])), False]
        
        if command == "!remove_friend":
            if len(message.content.split()) < 2:
                return ["You have to specify which friend to remove. Ex.: !remove_friend @someone", False]
            if len(message.mentions) != 1:
                return ["You have to mention which friend you would like to remove. Ex.: !remove_friend @someone", False]
            
            return [user.remove_friend(message.author.name, message.mentions[0].name), False]
        
        if command == "!friends_list":
            return [user.show_friends_list(message.author.name), False]
        
        if command == "!add_session_cookie":
                if public:
                    return ["This is sensitive private information! Please only use this command on private DM's!", True]
                if len(message.content.split()) < 2:
                    return ["You have to input your session cookie. Ex.: !add_session_cookie <cookie>", False]
                return [user.add_cookie(message.author.name, int(message.content.split()[1])), True]
        
        if command == "!add_username":
            if public:
                return ["This is sensitive private information! Please only use this command on private DM's!", True]
            if len(message.content.split()) < 2:
                    return ["You have to input your username. Ex.: !add_username <username>", False]
            return [user.add_username(message.author.name, message.content.split()[1]), True]

        if command == "!add_password":
            if public:
                return ["This is sensitive private information! Please only use this command on private DM's!", True]
            if len(message.content.split()) < 2:
                    return ["You have to input your password. Ex.: !add_password <password>", False]
            return [user.add_password(message.author.name, message.content.split()[1]), True]

        if command == "!help":
            return ["Available commands:\n!add_friend\n!friend_requests\n!accept\n!friends_list\n!remove_friend\n!add_session_cookie", False]

        if command == "!add_schedule":
            title = "Add schedule"
            options = ["Adicionar faculdade", "Escolher faculdade para editar horario", "Editar horario de curso"]
            formated_output = format_output(title, options)
            user.add_current_schedule_interaction(message.author.name)
            return [formated_output, False]
        
        if command == "!add_event":
            if len(message.content.split()) < 3:
                return ['You have to specify the date of the event and title. You can also specify the hour. Ex.: !add_event Programming Test 31/12/2023 15:00', False]
            else:
                parts = message.content.split()
                date_index = next(((i, part) for i, part in enumerate(parts) if '/' in part or '-' in part), None)
                if date_index:
                    date_index = date_index[0]
                    if date_index >= 2:
                        event_name = ' '.join(parts[1:date_index])
                    else:
                        event_name = parts[1]
                else:
                    return ["No date found", False]
                date_obj = get_date(message.content.split()[date_index])
                minutes = 0
                hours = 0
                if len(message.content.split()) > date_index + 1:
                    hours, minutes = message.content.split()[date_index + 1].split(":")
                if date_obj[0] == "failed":
                    return ["Unsupported date format. Supported formats: '%d-%m-%Y', '%d/%m/%Y', '%d-%m-%y', '%d/%m/%y'", False]
                else:
                    return [user.create_event(message.author.name, date_obj[1], event_name, hours, minutes), False]

    else:
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
            return process_manage_course_classes(message, public, command)
        
        elif interaction == Interaction.ADD_CLASS:
            return process_choose_class_to_add(message, public, command)

    return ["Unknown command", False]

def process_add_schedule(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    if option_chosen == 1:
        faculties: List[Faculty] = api.get_faculties()
        title = "Faculdades disponiveis"
        options = [f"{faculty.acronym}: {faculty.name.strip()}" for faculty in faculties]
        formated_output = format_output(title, options)
        user.add_choose_faculty_to_add_schedule_interaction(message.author.name, faculties)
        return [formated_output, False]
    elif option_chosen == 2:
        faculties: List[dict] = user.get_faculties(message.author.name)
        title = "Inscrito em faculdades"
        options = [f"{faculty['name']}: {faculty['full_name'].strip()}" for faculty in faculties]
        formated_output = format_output(title, options)
        user.add_choose_faculty_to_edit_schedule_interaction(message.author.name, faculties)
        return [formated_output, False]
    return ["Option not recognized", False]

def process_choose_faculty_to_add(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    faculties = user.get_current_interaction_data(message.author.name)
    if option_chosen <= 0 or option_chosen > len(faculties):
        return ["Option not recognized", False]
    faculty: List[Faculty] = faculties[option_chosen-1]
    added = user.add_faculty(message.author.name, faculty)

    if added:
        pre_title = f"Added {faculty.acronym}: {faculty.name.strip()}"
    else:
        pre_title = f"You already added {faculty.acronym}: {faculty.name.strip()}"
    title = "Add schedule"
    options = ["Adicionar faculdade", "Escolher faculdade para editar horario", "Editar horario de curso"]
    formated_output = format_output(pre_title + '\n\n' + title, options)
    user.add_current_schedule_interaction(message.author.name)
    return [formated_output, False]

def process_choose_faculty_to_edit(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    faculties = user.get_current_interaction_data(message.author.name)
    if option_chosen < 0 or option_chosen > len(faculties):
        return ["Option not recognized", False]
    faculty: dict = faculties[option_chosen-1]
    title = f"Escolheste a faculdade {faculty['name']}: {faculty['full_name'].strip()}"
    options = ["Adicionar curso", "Editar horario de curso"]
    formated_output = format_output(title, options)
    user.add_current_faculty_course_interaction(message.author.name, faculty)
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
        formated_output = format_output(title, options)
        user.add_course_interaction(message.author.name, faculty, courses)
        return [formated_output, False]
    elif option_chosen == 2:
        # List current faculty courses
        courses = user.get_faculty_courses(message.author.name, faculty)
        title = f"Escolher curso de {faculty['name']} para editar horario"
        options = [f"{course['name']}: {course['full_name'].strip()}" for course in courses]
        formated_output = format_output(title, options)
        user.add_course_edit_schedule_interaction(message.author.name, faculty, courses)
        return [formated_output, False]
    return ["Option not recognized", False]

def process_add_course(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    data = user.get_current_interaction_data(message.author.name)
    faculty: dict = data['faculty']
    courses: List[Course] = data['courses']
    if option_chosen <= 0 or option_chosen > len(courses):
        return ["Option not recognized", False]
    course: Course = courses[option_chosen-1]
    added = user.add_course(message.author.name, faculty, course)

    if added:
        pre_title = f"Added {course.acronym}: {course.name.strip()}"
    else:   
        pre_title = f"You already added {course.acronym}: {course.name.strip()}"
    title = f"Escolheste a faculdade {faculty['name']}: {faculty['full_name'].strip()}"
    options = ["Adicionar curso", "Editar horario de curso"]
    formated_output = format_output(pre_title + '\n\n' + title, options)
    user.add_current_faculty_course_interaction(message.author.name, faculty)
    return [formated_output, False]

def process_edit_course(message, public, command):

    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    data = user.get_current_interaction_data(message.author.name)
    courses: List[dict] = data['courses']
    faculty: dict = data['faculty']
    if option_chosen <= 0 or option_chosen > len(courses):
        return ["Option not recognized", False]
    
    course: dict = courses[option_chosen-1]
    title = f"Escolheste o curso {course['name']}: {course['full_name'].strip()}"
    options = ["Adicionar cadeira", "Editar horario de cadeira"]
    formated_output = format_output(title, options)
    user.add_current_course_class_interaction(message.author.name, faculty, course)
    return [formated_output, False]

def process_manage_course_classes(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    data = user.get_current_interaction_data(message.author.name)
    faculty: dict = data['faculty']
    course: dict = data['course']

    if option_chosen == 1:
        classes: List[CourseUnit] = api.get_course_course_units(course['id'])
        title = f"Cadeiras disponiveis em {course['name']}: {course['full_name'].strip()}"
        options = [f"{course_unit.name.strip()}: {course_unit.year} year;  {course_unit.semester} Semester" for course_unit in classes]
        formated_output = format_output(title, options)
        user.add_class_interaction(message.author.name, faculty, course, classes)
        return [formated_output, False]
    elif option_chosen == 2:
        pass

    return ["Option not recognized", False]

def process_choose_class_to_add(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    data = user.get_current_interaction_data(message.author.name)
    faculty: dict = data['faculty']
    course: dict = data['course']
    course_units: List[CourseUnit] = data['classes']
    if option_chosen <= 0 or option_chosen > len(course_units):
        return ["Option not recognized", False]
    
    course_unit: CourseUnit = course_units[option_chosen-1]
    added = user.add_course_unit(message.author.name, faculty, course, course_unit)

    if added:
        pre_title = f"Added {course_unit.acronym}: {course_unit.name.strip()}"
    else:
        pre_title = f"You already added {course_unit.acronym}: {course_unit.name.strip()}"
    title = f"Escolheste o curso {course['name']}: {course['full_name'].strip()}"
    options = ["Adicionar cadeira", "Editar horario de cadeira"]
    formated_output = format_output(pre_title + '\n\n' + title, options)
    return [formated_output, False]

def get_option_chosen(command):
    option_chosen = command[1:].strip()
    try:
        option_chosen = int(option_chosen)
    except:
        return -1
    return option_chosen

def format_output(title, options):
    numbered_options = [f'{index+1}. {elm}' for index, elm in enumerate(options)] 
    output = title + '\n' + '\n'.join(numbered_options)
    return output

def get_date(date):
    formats = ['%d-%m-%Y', '%d/%m/%Y', '%d-%m-%y', '%d/%m/%y']
    for fmt in formats:
        try:
            date_obj = datetime.strptime(date, fmt)
            return ["worked", date_obj]
        except ValueError:
            pass
    return ["failed", None]