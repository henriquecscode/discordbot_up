import user
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



    elif option_chosen == 3:
        pass
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
    else:
        # List current faculty courses
        courses = user.get_faculty_courses(message.author.name, faculty)
        title = f"Escolher curso de {faculty['name']} para editar horario"
        options = [f"{course['name']}: {course['full_name'].strip()}" for course in courses]
        formated_output = format_output(title, options)
        user.add_course_edit_schedule_interaction(message.author.name, faculty, courses)
        return [formated_output, False]

def process_add_course(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    data = user.get_current_interaction_data(message.author.name)
    courses: List[Course] = data['courses']
    faculty: dict = data['faculty']
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