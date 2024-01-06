import user
import user_schedule
import user_office
import slot_types
from events.interaction import Interaction
from database.database_api import api
from typing import List, Tuple
from database.dbs.schema import *
from datetime import datetime, timedelta
import re
from dotenv import load_dotenv
import os
load_dotenv()


def get_author_ids():
    author_ids_variable = os.getenv("AUTHOR_IDS")
    if author_ids_variable is None:
        ids = []
    else:
        author_ids_variable = author_ids_variable.strip()
        if author_ids_variable == "":
            ids = []
        else:
            try:
                ids = list(map(int, author_ids_variable.split(' ')))
            except:
                ids = []
    return ids

AUTHOR_IDS = get_author_ids()


def process_input(message, public, id_overwride = None):
    #Create an account for the author of the message and all those mentioned, podemos ter de mudar quando formos buscar dados ao sigarra
    if id_overwride is not None:
        author_id = id_overwride
    else:
        author_id = message.author.id
    user.account_checker(author_id)
    for util in message.mentions:
        user.account_checker(util.id)

    command = message.content.split()[0]

    return_message = None
    new_interaction = False
         
    # Checking base interaction
    if command == "!add_friend":
        if len(message.mentions) != 1:
            return_message = ["You have to mention which friend you would like to add. Ex.: !add_friend @someone", False]
        else:
            return_message = [user.send_friend_request(author_id, message.author.name, message.mentions[0].id, message.mentions[0].name), False]

    elif command == "!friend_requests":
        return_message = [user.check_friend_requests(author_id), False]
    
    elif command == "!accept":
        if len(message.content.split()) < 2:
            return_message = ["You have to specify which friend request to accept. Ex.: !accept 1", False]
        return_message = [user.accept_friend_request(author_id, int(message.content.split()[1])), False]
    
    elif command == "!remove_friend":
        if len(message.content.split()) < 2:
            return_message = ["You have to specify which friend to remove. Ex.: !remove_friend @someone", False]
        if len(message.mentions) != 1:
            return_message = ["You have to mention which friend you would like to remove. Ex.: !remove_friend @someone", False]
        
        return_message = [user.remove_friend(author_id, message.mentions[0].id, message.mentions[0].name), False]
    
    elif command == "!friends_list":
        return_message = [user.show_friends_list(author_id), False]

    
    elif command == "!add_username":
        if public:
            return_message = ["This is sensitive private information! Please only use this command on private DM's!", True]
        if len(message.content.split()) < 2:
                return_message = ["You have to input your username. Ex.: !add_username <username>", False]
        return_message = [user.add_username(author_id, message.content.split()[1]), True]

    elif command == "!add_password":
        if public:
            return_message = ["This is sensitive private information! Please only use this command on private DM's!", True]
        if len(message.content.split()) < 2:
                return_message = ["You have to input your password. Ex.: !add_password <password>", False]
        return_message = [user.add_password(author_id, message.content.split()[1]), True]

    elif command == "!help":
        commands = ["!add_friend", "!friend_requests", "!accept", "!friends_list", "!remove_friend", "!add_event", "!events", "!add_schedule", "!view_schedule", "!schedule_meeting", "!deschedule_meeting", "!view_meetings", "!add_number", "!add_name", "!reserve_office", "!view_office_reservations", "!cancel_office"]
        return_message = ["Available commands:\n" + '\n'.join(commands), False]

    elif command == "!add_event":
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
                return ["Wrong format. Ex.: !add_event Programming Test 31/12/2023", False]
            if date_index < 2:
                return ["Wrong format. Ex.: !add_event Programming Test 31/12/2023 15:00", False]
            date_obj = get_date(message.content.split()[date_index])
            minutes = 59
            hours = 23
            if len(message.content.split()) > date_index + 1:
                pattern = r'^([0-1]?[0-9]|2[0-3]):([0-5][0-9])$'
                if not (re.match(pattern,  message.content.split()[date_index + 1])):
                    return ["Wrong format. Ex.: !add_event Programming Test 31/12/2023 15:00", False]
                hours, minutes = message.content.split()[date_index + 1].split(":")
            if date_obj is None:
                return ["Unsupported date format. Supported formats: '%d-%m-%Y', '%d/%m/%Y', '%d-%m-%y', '%d/%m/%y'", False]
            else:
                return [user.create_event(message.author.id, date_obj, event_name, hours, minutes), False]
            
    elif command == "!events":
        user.update_events(message.author.id)
        if len(message.content.split()) > 1:
            if message.content.split()[1] == "delete":
                return_message = [user.delete_event(message.author.id, int(message.content.split()[2]) - 1), False]
        else:
            title = "Your future events:"
            options = user.get_events_list(message.author.id)
            if len(options) > 0:
                return_message = [format_output(title, options) + "\n\nIn order to delete events do !events delete #", False]
            else:
                return_message = ["This user has no events!"    , False]
    

    elif command == "!add_schedule":
        title = "Add schedule"
        options = ["Adicionar faculdade", "Escolher faculdade para editar horario", "Editar horario de curso", "Adicionar manualmente", "Remover horario manual"]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_schedule_interaction(author_id)
        new_interaction = True
        return_message = [formated_output, False]

    elif command == "!view_schedule":
        return_message = process_view_schedule(author_id)

    elif command == "!_author":
        if author_id not in AUTHOR_IDS:
            return_message = ["Admin only command", False]
        elif len(message.content.split()) < 2:
            return_message = ["Author commands must have another command", False]
        else:
            split_message = message.content.split()
            id = split_message[1]
            try:
                if id.startswith('<@') and id.endswith('>'):
                    id = id[2:-1]
                    id = int(id)
                else:
                    id = int(id)
                # Get the int in <@237236210823593984>
                new_message_content = ' '.join(split_message[2:])
            except:
                id = author_id
                new_message_content = ' '.join(split_message[1:])

            if not new_message_content.startswith('!'):
                new_message_content = '!' + new_message_content
            new_message = message
            new_message.content = new_message_content
            output, public  = process_input(message, public, id)
            output = f"Command executed as {id}:\n" + output
            return_message = [output, public]

    elif command == "!schedule_meeting":

        if False: # DEBUG
            mentions = message.mentions
            id_mentions = [mention.id for mention in mentions]
        else:
            # regex to match <@12345678910>
            pattern = r'<@([0-9]+)>'
            # Capture pattern
            # Get the int in <@237236210823593984>
            all_mentions =  re.findall(pattern, message.content) 
            id_mentions = [int(mention) for mention in all_mentions]

        if len(id_mentions) == 0:
            return_message = ["You have to mention at least one person. Ex.: !schedule_meeting @someone", False]

        else:
            title = "Schedule meeting"
            subtitle = "Choose the day and time of meeting" 
            message_string = get_schedule_meeting_format_message(title + '\n' + subtitle)
            user_schedule.add_schedule_meeting_interaction(author_id, id_mentions)
            new_interaction = True
            return_message = [message_string, False]

    elif command == "!deschedule_meeting":
        meetings = user_schedule.get_meetings(author_id)
        formated_meetings = []
        for meeting in meetings:
            meeting_string = format_meeting_string(meeting)
           

            formated_meetings.append(f"Meeting {meeting_string}")

        title = "Deschedule meeting"
        options = formated_meetings
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_deschedule_meeting_interaction(author_id, meetings)
        new_interaction = True
        return_message = [formated_output, False]

    elif command == "!view_meetings":
        meetings = user_schedule.get_meetings(author_id)
        if len(meetings) == 0:
            return_message = ["You have no meetings", False]
        else:
            formated_meetings = []
            for meeting in meetings:
                meeting_string = format_meeting_string(meeting)
                formated_meetings.append(f"Meeting {meeting_string}")
            title = "Your meetings"
            content = '\n'.join(formated_meetings)
            return_message = [title + '\n' + content, False]

    elif command == "!add_number":
        words = message.content.split()
        error_message = "You have to input your student number. Ex.: !add_number <number>"
        if len(words) < 2:
            return_message = [error_message, False]
        elif len(words) > 2:
            return_message = [error_message, False]
        else:
            number = words[1]
            try:
                int_number = int(number)
                user.add_number(author_id, int_number)
                return_message = ["Number added", False]
            except:
                return_message = [error_message, False]

    elif command == "!add_name":
        words = message.content.split()
        error_message = "You have to input your name. Ex.: !add_name <name>"
        if len(words) < 2:
            return_message = [error_message, False]
        else:
            name_words = words[1:]
            name = ' '.join(name_words)
            user.add_name(author_id, name)
            return_message = ["Name added", False]

    elif command == "!reserve_office":
        
        benefficiary_id = user.get_number(author_id)
        if benefficiary_id is None:
            return_message = ["You have to input your student number. Ex.: !add_number <number>", False]
        elif len(user_office.get_office_reservations(author_id)):
            return_message = ["You already have an office request. More than one is currently not supported", False]
        else:
            user_office.add_reserve_office_interaction(author_id)
            prompt = get_reserve_office_format_message("")
            return_message = [prompt, False]
            new_interaction = True
    elif command == "!view_office_reservations":
        reservations = user_office.get_office_reservations(author_id)
        if len(reservations) == 0:
            return_message = ["You have no office reservations", False]
        else:
            office_reservation_strings = [format_office_reservation(reservation) for reservation in reservations]
            title = "Your office reservations:"
            formated_output = format_unnumbered_output(title, office_reservation_strings)
            return_message = [formated_output, False]
    elif command == "!cancel_office":
        reservations = user_office.get_office_reservations(author_id)
        if len(reservations) == 0:
            return_message = ["You have no office reservations", False]
        else:
            office_reservation_strings = [format_office_reservation(reservation) for reservation in reservations]
            title = "Your office reservations:"
            options = office_reservation_strings
            formated_output = format_output_with_cancel(title, options)
            user_office.add_cancel_office_interaction(author_id, reservations)
            return_message = [formated_output, False]
            new_interaction = True

        pass

    if return_message is not None:
        if not new_interaction:
            user.cancel_current_interaction(author_id)
        return return_message
    

    # Continuing interaction
    if user.has_current_interaction(author_id):        
        if command == "!cancel":
            user.cancel_current_interaction(author_id)
            return ["Canceled", False]
        
        interaction = user.get_current_interaction(author_id)
        if interaction == Interaction.ADD_SCHEDULE:
            return process_add_schedule(author_id, public, command)

        elif interaction == Interaction.CHOOSE_FACULTY_TO_ADD:
            return process_choose_faculty_to_add(author_id, public, command)

        elif interaction == Interaction.CHOOSE_FACULTY_TO_EDIT:
            return process_choose_faculty_to_edit(author_id, public, command)
        
        elif interaction == Interaction.MANAGE_FACULTY:
            return process_manage_faculty_courses(author_id, public, command)
        
        elif interaction == Interaction.ADD_COURSE:
            return process_add_course(author_id, public, command)
        
        elif interaction == Interaction.EDIT_COURSE:
            return process_edit_course(author_id, public, command)
        
        elif interaction == Interaction.MANAGE_COURSE:
            return process_manage_course_course_units(author_id, public, command)
        
        elif interaction == Interaction.ADD_COURSE_UNIT:
            return process_choose_course_unit_to_add(author_id, public, command)
        
        elif interaction == Interaction.EDIT_COURSE_UNIT:
            return process_choose_course_unit_to_edit(author_id, public, command)
        
        elif interaction == Interaction.MANAGE_COURSE_UNIT:
            return process_manage_course_unit_classes(author_id, public, command)
        
        elif interaction == Interaction.ADD_CLASS:
            return process_add_class(author_id, public, command)
        
        elif interaction == Interaction.VIEW_CLASS:
            return process_view_class(author_id, public, command)
        
        elif interaction == Interaction.REMOVE_CLASS:
            return process_remove_class(author_id, public, command)
        
        elif interaction == Interaction.ADD_SCHEDULE_MANUALLY:
            return process_add_schedule_manually(message, author_id, public, command)
        
        elif interaction == Interaction.CONFIRM_ADD_CLASS:
            return process_confirm_add_class(author_id, public, command)
        
        elif interaction == Interaction.REMOVE_SCHEDULE_MANUALLY:
            return process_remove_schedule_manually(author_id, public, command)
        
        elif interaction == Interaction.SCHEDULE_MEETING:
            return process_schedule_meeting(message, author_id, public, command)
        
        elif interaction == Interaction.SCHEDULE_MEETING_RETRY_SCHEDULE:
            return process_schedule_meeting_retry_schedule(author_id, public, command)

        elif interaction == Interaction.DESCHEDULE_MEETING:
            return process_deschedule_meeting(author_id, public, command)
        
        elif interaction == Interaction.RESERVE_OFFICE :
            return process_reserve_office(message, author_id, public, command)
        
        elif interaction == Interaction.CONFIRM_RESERVE_OFFICE:
            return process_confirm_reserve_office(author_id, public, command)
    
        elif interaction == Interaction.CANCEL_OFFICE:
            return process_cancel_office(author_id, public, command)
        
    else:
        if command == "!cancel":
            return ["You don't have any interaction to cancel", False]
        
    return ["Unknown command", False]

def process_view_schedule(author_id: int):
    schedule : List[dict] = user_schedule.get_schedule(author_id)
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
                    class_string = f"{class_['name']}({class_['lesson_type']}): {get_day_from_day_index(class_['day'])[0]} {format_time(class_['start_time'])}-{format_time(class_['start_time'] + class_['duration'])} in {class_['location']}"
                    schedules_classes[faculty_string][course_string][course_unit_string].append(class_string)

                if len(schedules_classes[faculty_string][course_string][course_unit_string]) == 0:
                    del schedules_classes[faculty_string][course_string][course_unit_string]

            if len(schedules_classes[faculty_string][course_string]) == 0:
                del schedules_classes[faculty_string][course_string]

        if len(schedules_classes[faculty_string]) == 0:
            del schedules_classes[faculty_string]      
    if len(schedules_classes) == 0:
        schedules_classes = None
    return_string = ""
    if schedules_classes is not None:
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

    return_string += "Manually added schedules:\n"
    manual_schedules = user_schedule.get_manual_schedules(author_id)
    for manual_schedule in manual_schedules:
        return_string += format_manual_schedule(manual_schedule) + "\n"
    return_message = [return_string, False]
    return return_message

def process_add_schedule(author_id: int, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    if option_chosen == 1:
        faculties: List[Faculty] = api.get_faculties()
        title = "Faculdades disponiveis"
        options = [f"{faculty.acronym}: {faculty.name.strip()}" for faculty in faculties]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_choose_faculty_to_add_schedule_interaction(author_id, faculties)
        return [formated_output, False]
    elif option_chosen == 2:
        faculties: List[dict] = user_schedule.get_faculties(author_id)
        title = "Inscrito em faculdades"
        options = [f"{faculty['name']}: {faculty['full_name'].strip()}" for faculty in faculties]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_choose_faculty_to_edit_schedule_interaction(author_id, faculties)
        return [formated_output, False]

    elif option_chosen == 3:
        return ["Not implemented yet. Choose another option", False]
    elif option_chosen == 4:
        title = "Adicionar horario manualmente"
        
        content_items = ["descricao de instituicao (por exemplo: faculdade, curso, cadeira)", "aula", "tipo de aula", "dia (de 0 - 2ª - a 6 - domingo -)", "hora inicio (HH:mm)", "duracao (minutos)"]
        optional_content_items = ["local"]
            
        content = f"Formato:! " + "; ".join(map (lambda x: f"<{x}>", content_items)) 
        content += "; " + "; ".join(map (lambda x: f"[<{x}>]", optional_content_items))

        cancel = "0: Cancel"
        user_schedule.add_schedule_manually_interaction(author_id)
        message = title + '\n' + content + '\n' + cancel
        return [message, False]
    elif option_chosen == 5:
        title = "Remover horario manualmente"
        schedules: List[dict] = user_schedule.get_manual_schedules(author_id)
        options = [format_manual_schedule(schedule) for schedule in schedules]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_remove_schedule_manually_interaction(author_id, schedules)
        return [formated_output, False]
    elif option_chosen == 0:
        user.cancel_current_interaction(author_id)
        return ["Canceled", False]
    return ["Option not recognized", False]

def process_choose_faculty_to_add(author_id: int, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    faculties = user.get_current_interaction_data(author_id)
    if option_chosen < 0 or option_chosen > len(faculties):
        return ["Option not recognized", False]
    faculty: List[Faculty] = faculties[option_chosen-1]
    added = user_schedule.add_faculty(author_id, faculty)

    if option_chosen != 0:
        if added:
            pre_title = f"Added {faculty.acronym}: {faculty.name.strip()}"
        else:
            pre_title = f"You already added {faculty.acronym}: {faculty.name.strip()}"
    else:
        pre_title = ""
    title = "Add schedule"
    options = ["Adicionar faculdade", "Escolher faculdade para editar horario", "Editar horario de curso", "Adicionar manualmente", "Remover horario manual"]

    formated_output = format_output_with_cancel(pre_title + '\n\n' + title, options)
    user_schedule.add_current_schedule_interaction(author_id)
    return [formated_output, False]

def process_choose_faculty_to_edit(author_id: int, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    faculties = user.get_current_interaction_data(author_id)
    if option_chosen < 0 or option_chosen > len(faculties):
        return ["Option not recognized", False]
    
    if option_chosen == 0:
        title = "Add schedule"
        options = ["Adicionar faculdade", "Escolher faculdade para editar horario", "Editar horario de curso", "Adicionar manualmente", "Remover horario manual"]

        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_schedule_interaction(author_id)
        return [formated_output, False]
    
    faculty: dict = faculties[option_chosen-1]
    title = f"Escolheste a faculdade {faculty['name']}: {faculty['full_name'].strip()}"
    options = ["Adicionar curso", "Editar horario de curso"]
    formated_output = format_output_with_cancel(title, options)
    user_schedule.add_current_faculty_course_interaction(author_id, faculty)
    return [formated_output, False]

def process_manage_faculty_courses(author_id: int, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    faculty: dict = user.get_current_interaction_data(author_id)
    if option_chosen == 1:
        courses: Course = api.get_faculty_courses(faculty['name'])
        title = f"Cursos disponiveis em {faculty['name']}: {faculty['full_name'].strip()}"
        options = [f"{course.name.strip()}" for course in courses]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_course_interaction(author_id, faculty, courses)
        return [formated_output, False]
    elif option_chosen == 2:
        # List current faculty courses
        courses = user_schedule.get_faculty_courses(author_id, faculty)
        title = f"Escolher curso de {faculty['name']} para editar horario"
        options = [f"{course['acronym']}: {course['name'].strip()}" for course in courses]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_course_edit_schedule_interaction(author_id, faculty, courses)
        return [formated_output, False]
    elif option_chosen == 0:
        title = "Add schedule"
        options = ["Adicionar faculdade", "Escolher faculdade para editar horario", "Editar horario de curso", "Adicionar manualmente", "Remover horario manual"]

        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_schedule_interaction(author_id)
        return [formated_output, False]
    return ["Option not recognized", False]

def process_add_course(author_id: int, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    data = user.get_current_interaction_data(author_id)
    faculty: dict = data['faculty']
    courses: List[Course] = data['courses']
    if option_chosen < 0 or option_chosen > len(courses):
        return ["Option not recognized", False]
    
    if option_chosen == 0:
        title = f"Escolheste a faculdade {faculty['name']}: {faculty['full_name'].strip()}"
        options = ["Adicionar curso", "Editar horario de curso"]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_faculty_course_interaction(author_id, faculty)
        return [formated_output, False]
    course: Course = courses[option_chosen-1]
    added = user_schedule.add_course(author_id, faculty, course)

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
    user_schedule.add_current_faculty_course_interaction(author_id, faculty)
    return [formated_output, False]

def process_edit_course(author_id: int, public, command):

    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    data = user.get_current_interaction_data(author_id)
    courses: List[dict] = data['courses']
    faculty: dict = data['faculty']
    if option_chosen < 0 or option_chosen > len(courses):
        return ["Option not recognized", False]
    
    if option_chosen == 0:
        title = f"Escolheste a faculdade {faculty['name']}: {faculty['full_name'].strip()}"
        options = ["Adicionar curso", "Editar horario de curso"]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_faculty_course_interaction(author_id, faculty)
        return [formated_output, False]

    course: dict = courses[option_chosen-1]
    title = f"Escolheste o curso {course['acronym']}: {course['name'].strip()}"
    options = ["Adicionar cadeira", "Editar horario de cadeira"]
    formated_output = format_output_with_cancel(title, options)
    user_schedule.add_current_course_course_unit_interaction(author_id, faculty, course)
    return [formated_output, False]

def process_manage_course_course_units(author_id: int, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    data = user.get_current_interaction_data(author_id)
    faculty: dict = data['faculty']
    course: dict = data['course']

    if option_chosen == 1:
        course_unit_year_course_units: List[Object] = api.get_course_course_units(course['id'])
        course_unit_years: List[CourseUnitYear] = [object_.CourseUnitYear for object_ in course_unit_year_course_units]
        course_units: List[CourseUnit] = [object_.CourseUnit for object_ in course_unit_year_course_units]
        title = f"Cadeiras disponiveis em {course['acronym']}: {course['name'].strip()}"
        options = [f"{course_unit.name.strip()}: {course_unit_year.course_unit_year} year;  {course_unit.semester} Semester ({course_unit.year})" for course_unit_year, course_unit in zip(course_unit_years, course_units)]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_add_class_unit_interaction(author_id, faculty, course, course_unit_year_course_units)
        return [formated_output, False]
    elif option_chosen == 2:
        course_unit_year_course_units: List[dict] = user_schedule.get_course_course_units(author_id, faculty, course)
        title = f"Escolher cadeira de {course['name']} para editar horario"
        options = [f"{course_unit['name'].strip()}: {course_unit['year']} year;  {course_unit['semester']} Semester" for course_unit in course_unit_year_course_units]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_edit_class_unit_interaction(author_id, faculty, course, course_unit_year_course_units)
        return [formated_output, False]
    elif option_chosen == 0:
        title = f"Escolheste a faculdade {faculty['name']}: {faculty['full_name'].strip()}"
        options = ["Adicionar curso", "Editar horario de curso"]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_faculty_course_interaction(author_id, faculty)
        return [formated_output, False]

    return ["Option not recognized", False]

def process_choose_course_unit_to_add(author_id: int, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    data = user.get_current_interaction_data(author_id)
    faculty: dict = data['faculty']
    course: dict = data['course']
    course_unit_year_course_units: List[Object] = data['course_units']
    if option_chosen < 0 or option_chosen > len(course_unit_year_course_units):
        return ["Option not recognized", False]
    
    if option_chosen != 0:
        course_unit_year_course_unit: Object = course_unit_year_course_units[option_chosen-1]
        course_unit: CourseUnit = course_unit_year_course_unit.CourseUnit
        course_unit_year: CourseUnitYear = course_unit_year_course_unit.CourseUnitYear
        added = user_schedule.add_course_unit(author_id, faculty, course, course_unit_year_course_unit)

        if added:
            pre_title = f"Added {course_unit.acronym}: {course_unit.name.strip()}"
        else:
            pre_title = f"You already added {course_unit.acronym}: {course_unit.name.strip()}"
    else:
        pre_title = ""
    title = f"Escolheste o curso {course['acronym']}: {course['name'].strip()}"
    options = ["Adicionar cadeira", "Editar horario de cadeira"]
    formated_output = format_output_with_cancel(pre_title + '\n\n' + title, options)
    user_schedule.add_current_course_course_unit_interaction(author_id, faculty, course)
    return [formated_output, False]

def process_choose_course_unit_to_edit(author_id: int, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    data = user.get_current_interaction_data(author_id)
    faculty: dict = data['faculty']
    course: dict = data['course']
    course_unit_year_course_units: List[dict] = data['course_units']

    if option_chosen == 0:
        title = f"Escolheste o curso {course['acronym']}: {course['name'].strip()}"
        options = ["Adicionar cadeira", "Editar horario de cadeira"]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_course_course_unit_interaction(author_id, faculty, course)
        return [formated_output, False]

    if option_chosen < 0 or option_chosen > len(course_unit_year_course_units):
        return ["Option not recognized", False]
    
    course_unit: dict = course_unit_year_course_units[option_chosen-1]
    title = f"Escolheste a cadeira {course_unit['acronym']}: {course_unit['name'].strip()}"
    options = ["Adicionar aula", "Ver horarios de aula", "Remover aula"]
    formated_output = format_output_with_cancel(title, options)
    user_schedule.add_current_course_unit_class_interaction(author_id, faculty, course, course_unit)
    return [formated_output, False]

def process_manage_course_unit_classes(author_id: int, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    data = user.get_current_interaction_data(author_id)
    faculty: dict = data['faculty']
    course: dict = data['course']
    course_unit: dict = data['course_unit']
    if option_chosen == 1:
        classes_: List[Schedule] = api.get_course_unit_schedules(course_unit['id'])
        title = f"Adicionar aula a {course_unit['acronym']}: {course_unit['name'].strip()}"
        options = [f"{class_.class_name}({class_.lesson_type}): {get_day_from_day_index(class_.day)[0]} {format_time(class_.start_time)}-{format_time(class_.start_time + class_.duration)} in {class_.location}" for class_ in classes_]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_choose_class_to_add_interaction(author_id, faculty, course, course_unit, classes_)
        return [formated_output, False]
    elif option_chosen == 2:
        classes_: List[dict] = user_schedule.get_course_unit_classes(author_id, faculty, course, course_unit)

        options = [f"{class_['name']}({class_['lesson_type']}): {get_day_from_day_index(class_['day'])[0]} {format_time(class_['start_time'])}-{format_time(class_['start_time'] + class_['duration'])} in {class_['location']}" for class_ in classes_]
        title = f"Horarios de aula de {course_unit['acronym']}: {course_unit['name'].strip()}"
        user_schedule.add_choose_class_to_view_interaction(author_id, faculty, course, course_unit, classes_)
        formated_output = format_unnumbered_output_with_cancel(title, options)
        return [formated_output, False]
    elif option_chosen == 3:
        classes_: List[dict] = user_schedule.get_course_unit_classes(author_id, faculty, course, course_unit)

        options = [f"{class_['name']}({class_['lesson_type']}): {get_day_from_day_index(class_['day'])[0]} {format_time(class_['start_time'])}-{format_time(class_['start_time'] + class_['duration'])} in {class_['location']}" for class_ in classes_]
        title = f"Remover aula de {course_unit['acronym']}: {course_unit['name'].strip()}"
        user_schedule.add_choose_class_to_remove_interaction(author_id, faculty, course, course_unit, classes_)
        formated_output = format_output_with_cancel(title, options)
        return [formated_output, False]

    elif option_chosen == 0:
        title = f"Escolheste o curso {course['acronym']}: {course['name'].strip()}"
        options = ["Adicionar cadeira", "Editar horario de cadeira"]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_course_course_unit_interaction(author_id, faculty, course)
        return [formated_output, False]

def process_add_class(author_id: int, public, command):
    option_chosen = get_option_chosen(command)

    if option_chosen == -1:
        return ["Option not recognized", False]
    data = user.get_current_interaction_data(author_id)
    faculty: dict = data['faculty']
    course: dict = data['course']
    course_unit_year_course_unit: dict = data['course_unit']
    classes_ : List[Schedule]= data['classes']
    
    if option_chosen < 0 or option_chosen > len(classes_):
        return ["Option not recognized", False]
    
    if option_chosen != 0:
        class_: Schedule = classes_[option_chosen-1]
        added = user_schedule.add_class(author_id, faculty, course, course_unit_year_course_unit, class_)
        if added:
            pre_title = f"Added {class_.class_name}: {class_.lesson_type}"
        else:
            pre_title = f"You already added {class_.class_name}: {class_.lesson_type}"
    else:
        pre_title = ""

    title = f"Escolheste a cadeira {course_unit_year_course_unit['acronym']}: {course_unit_year_course_unit['name'].strip()}"
    options = ["Adicionar aula", "Ver horarios de aula", "Remover aula"]
    formated_output = format_output_with_cancel(pre_title + '\n\n' + title, options)
    user_schedule.add_current_course_unit_class_interaction(author_id, faculty, course, course_unit_year_course_unit)
    return [formated_output, False]

def process_view_class(author_id: int, public, command):
    option_chosen = get_option_chosen(command)

    if option_chosen == 0:
        data = user.get_current_interaction_data(author_id)
        faculty: dict = data['faculty']
        course: dict = data['course']
        course_unit: dict = data['course_unit']
        title = f"Escolheste a cadeira {course_unit['acronym']}: {course_unit['name'].strip()}"
        options = ["Adicionar aula", "Ver horarios de aula", "Remover aula"]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_course_unit_class_interaction(author_id, faculty, course, course_unit)
        return [formated_output, False]
    else:
        return ["Option not recognized", False]
    
def process_remove_class(author_id: int, public, command):
    option_chosen = get_option_chosen(command)

    if option_chosen == -1:
        return ["Option not recognized", False]
    data = user.get_current_interaction_data(author_id)
    faculty: dict = data['faculty']
    course: dict = data['course']
    course_unit: dict = data['course_unit']
    classes_ : List[dict]= data['classes']
    if option_chosen == 0:
        options = ["Adicionar aula", "Ver horarios de aula", "Remover aula"]
        title = f"Escolheste a cadeira {course_unit['acronym']}: {course_unit['name'].strip()}"
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_course_unit_class_interaction(author_id, faculty, course, course_unit)
        return [formated_output, False]
    
    if option_chosen < 0 or option_chosen > len(classes_):
        return ["Option not recognized", False]
    
    class_: dict = classes_[option_chosen-1]
    removed = user_schedule.remove_class(author_id, faculty, course, course_unit, class_)
    if removed:
        pre_title = f"Removed {class_['name']}: {class_['lesson_type']}\n\n"
    else:
        pre_title = ""
    title = f"Escolheste a cadeira {course_unit['acronym']}: {course_unit['name'].strip()}"
    options = ["Adicionar aula", "Ver horarios de aula", "Remover aula"]
    formated_output = format_output_with_cancel(pre_title + title, options)
    user_schedule.add_current_course_unit_class_interaction(author_id, faculty, course, course_unit)
    return [formated_output, False]

def process_add_schedule_manually(message, author_id: int, public, command):

    option_chosen = get_option_chosen(command)
    if option_chosen == 0:
        title = "Add schedule"
        options = ["Adicionar faculdade", "Escolher faculdade para editar horario", "Editar horario de curso", "Adicionar manualmente", "Remover horario manual"]
        formated_output = format_output_with_cancel(title, options)
        user_schedule.add_current_schedule_interaction(author_id)
        return [formated_output, False]
    
    content = message.content
    content = content[1:]

    content_items = ["<descricao de instituicao (por exemplo: faculdade, curso, cadeira)", "aula", "tipo de aula", "dia (de 0 - 2ª - a 6 - domingo -)", "hora inicio (HH:mm)", "duracao (minutos)"]
    optional_content_items = ["local"]    

    parameters = content.split(";")
    parameters = list(map(lambda x: x.strip(), parameters))
    # Remove empty strings
    parameters = list(filter(lambda x: x != "", parameters))
    data = parameters
    # <faculdade>; <curso>; <cadeira>; <tipo de aula>; <dia (de 0 - 2ª - a 6 - domingo -)>; <hora inicio>; <duracao>; [<local> -opcional]\nExemplo: FEUP MIEIC PLOG TP 2 14:00 2:00 B207
    if len(data) < len (content_items):
        return [get_wrong_format_message(f"Must have at least {len(content_items)} parameters"), False]
    if len(data) > len(content_items) + len(optional_content_items):
        return [get_wrong_format_message(f"Must have at most {len(content_items) + len(optional_content_items)} parameters"), False]

    
    institution = data[0]
    class_ = data[1]
    lesson_type = data[2]
    day = data[3]
    start_time_input = data[4]
    duration = data[5]
    if len(data) == 7:
        location = data[6]
    else:
        location = None

    if not day.isdigit() or not duration.isdigit():
        return [get_wrong_format_message("Day and duration must be numbers"), False]
    else:
        day = int(day)
        duration = int(duration)

    start_time = get_time_from_formated_time_input(start_time_input)
    if start_time is None:
        return [get_wrong_format_message("Start time must be in the format HH:mm"), False]

    if not (day >= 1 and day <= 7):
        return [get_wrong_format_message("Day must be between 0 (2ª) and 6 (domingo)"), False]

    data = {
        "institution": institution,
        "class": class_,
        "lesson_type": lesson_type,
        "day": day,
        "start_time": start_time,
        "duration": duration,
        "location": location
    }
    schedule_string = format_manual_schedule(data)
    confirmation_message = f"Adicionar aula de {schedule_string}"
    
    return_message = confirmation_message + "\n1: Confirmar\n0: Cancelar"
    user_schedule.add_confirm_add_class_interaction(author_id, institution, class_, lesson_type, day, start_time, duration, location)

    return [return_message, False]

def process_confirm_add_class(author_id: int, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == 0:
        title = "Adicionar horario manualmente"
        
        content_items = ["<descricao de instituicao (por exemplo: faculdade, curso, cadeira)", "aula", "tipo de aula", "dia (de 0 - 2ª - a 6 - domingo -)", "hora inicio", "duracao"]
        optional_content_items = ["local"]
            
        content = f"Formato:! " + "; ".join(map (lambda x: f"<{x}>", content_items)) 
        content += "; " + "; ".join(map (lambda x: f"[<{x}>]", optional_content_items))

        cancel = "0: Cancel"
        user_schedule.add_schedule_manually_interaction(author_id)
        return_message = title + '\n' + content + '\n' + cancel
        return [return_message, False]
    elif option_chosen == 1:
        data: dict = user.get_current_interaction_data(author_id)
        institution = data['institution']
        class_ = data['class']
        lesson_type = data['lesson_type']
        day = data['day']
        start_time = data['start_time']
        duration = data['duration']
        location = data['location']
        user_schedule.add_manual_schedule(author_id, institution, class_, lesson_type, day, start_time, duration, location)

        day_name, day_gender = get_day_from_day_index(day)
        day_string = f"n{day_gender} {day_name}"
        schedule_string = format_manual_schedule(data)
        pretitle = f"Added  {schedule_string}"
        title = "Adicionar horario manualmente"
        
        content_items = ["<descricao de instituicao (por exemplo: faculdade, curso, cadeira)", "aula", "tipo de aula", "dia (de 0 - 2ª - a 6 - domingo -)", "hora inicio", "duracao"]
        optional_content_items = ["local"]
            
        content = f"Formato:! " + "; ".join(map (lambda x: f"<{x}>", content_items)) 
        content += "; " + "; ".join(map (lambda x: f"[<{x}>]", optional_content_items))

        cancel = "0: Cancel"
        user_schedule.add_schedule_manually_interaction(author_id)
        return_message = pretitle + '\n' + title + '\n' + content + '\n' + cancel
        return [return_message, False]
    
def process_remove_schedule_manually(author_id: int, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    schedules: List[dict] = user.get_current_interaction_data(author_id)
    if option_chosen < 0 or option_chosen > len(schedules):
        return ["Option not recognized", False]

    if option_chosen != 0:
        schedule: dict = schedules[option_chosen-1]
        removed = user_schedule.remove_manual_schedule(author_id, schedule)
        if removed:
            schedule_string = format_manual_schedule(schedule)
            pre_title = f"Removed {schedule_string}"
    else:
        pre_title = "" 
    title = "Add schedule"
    options = ["Adicionar faculdade", "Escolher faculdade para editar horario", "Editar horario de curso", "Adicionar manualmente", "Remover horario manual"]
    formated_output = format_output_with_cancel(pre_title + '\n\n' + title, options)
    user_schedule.add_current_schedule_interaction(author_id)
    return [formated_output, False]

def process_schedule_meeting(message, author_id: int, public, command):
    option_chosen = get_option_chosen(command)

    if option_chosen == 0:
        user.cancel_current_interaction(author_id)
        return ["Canceled", False]
    
    
    content = message.content[1:]
    content = content.split(";")
    content = list(filter(lambda x: x != "", content))
    content = list(map(str.strip, content)) # Check if this works

    if len(content) != 3:
        return [get_schedule_meeting_format_message("Must have 3 parameters"), False]
    input_date = content[0]
    input_time = content[1]
    duration = content[2]

    if not duration.isdigit():
        return [get_schedule_meeting_format_message("Duration must be number"), False]
    else:
        duration = int(duration)

    hours_minutes = get_hours_minutes_from_formated_time_input(input_time)
    if hours_minutes is None:
        return [get_schedule_meeting_format_message("Start time must be in the format HH:mm"), False]
    
    hours, minutes = hours_minutes
    start_time = hours * 60 + minutes

    date = get_date(input_date)

    if date is None:
        return [get_schedule_meeting_format_message("Day must be in the format DD/MM/YYYY"), False]
    
    date = date.replace(hour=hours, minute=minutes)
    input_day = ( date.weekday() ) % 7
    # Reply
    meeting_slot = user_schedule.get_slot_from_time_info(input_day, start_time, duration)
    to_meet_usernames = user.get_current_interaction_data(author_id)
     
    #  Grab our schedule
    self_schedule = user_schedule.get_joint_schedule(author_id)
    for joint_class in self_schedule:
        joint_class_type = joint_class['type']

        if joint_class_type == slot_types.ADDED_MANUAL_SCHEDULE or joint_class_type == slot_types.ADDED_SCHEDULE:
            class_ = joint_class['class']
            class_day = class_['day']
            class_start_time = class_['start_time']
            class_duration = class_['duration']
            class_slot = user_schedule.get_slot_from_time_info(class_day, class_start_time, class_duration)

            intersect = get_intersect_week_occupancy_slot(class_slot, meeting_slot)
        elif joint_class_type == slot_types.MEETING or joint_class_type == slot_types.EVENT:
            class_ = joint_class['class']
            class_date = class_['date']
            class_duration = class_['duration']

            intersect = get_intersect_absolute_slots((class_date, class_duration), (date, duration))

        else:
            raise Exception("Unknown schedule type")

        if intersect is not None:
            if joint_class['type'] == slot_types.ADDED_MANUAL_SCHEDULE:
                schedule_string = format_manual_schedule(class_)
                scheduled_event = f"You have a class at that time: {schedule_string}"
            elif joint_class['type'] == slot_types.ADDED_SCHEDULE:
                schedule_string = format_api_joint_class(class_)
                scheduled_event = f"You have a class at that time: {schedule_string}"
            elif joint_class['type'] == slot_types.MEETING:
                schedule_string = format_meeting_string(class_)
                scheduled_event = f"You have a meeting at that time: Meeting {schedule_string}"
            elif joint_class['type'] == slot_types.EVENT:
                schedule_string = format_event_string(class_)
                scheduled_event = f"You have an event at that time: {schedule_string}"
            else:
                raise Exception("Unknown schedule type")
            
            #todo
            overlap_string = f"Overlaps with your proposed meeting on {format_absolute_time_slot_info(date, duration)}"
            options = ["Try another time", "Schedule it anyway"]
            formated_output = format_output_with_cancel(scheduled_event + '\n' + overlap_string, options)
            user_schedule.add_schedule_meeting_retry_schedule_interaction(author_id, to_meet_usernames, date, duration)
            return [formated_output, False]


    not_available_usernames = []
    for to_meet_username in to_meet_usernames:
        to_meet_schedule = user_schedule.get_joint_schedule(to_meet_username)
        periodic_classes = [joint_class for joint_class in to_meet_schedule if joint_class['type'] == slot_types.ADDED_SCHEDULE or joint_class['type'] == slot_types.ADDED_MANUAL_SCHEDULE]
        to_meet_minutes_slots = get_schedule_minutes_slots(periodic_classes)
        

        periodic_intersects = [get_intersect_week_occupancy_slot(to_meet_minutes_slot, meeting_slot) for to_meet_minutes_slot in to_meet_minutes_slots]
        does_intersect = any([intersect is not None for intersect in periodic_intersects])
        if does_intersect:
            not_available_usernames.append(to_meet_username)
            continue

        exceptional_classes = [joint_class for joint_class in to_meet_schedule if joint_class['type'] == slot_types.MEETING or joint_class['type'] == slot_types.EVENT]
        exceptional_classes_absolute_slots = [ (joint_class['class']['date'], joint_class['class']['duration']) for joint_class in exceptional_classes ]
        exceptional_intersects = [get_intersect_absolute_slots(to_intersect_slot, (date, duration)) for to_intersect_slot in exceptional_classes_absolute_slots]
        does_intersect = any([intersect is not None for intersect in exceptional_intersects])
        if does_intersect:
            not_available_usernames.append(to_meet_username)
            continue
        
    
    if (len(not_available_usernames) > 0):
        #todo
        availability_string = f"Users not available on {format_absolute_time_slot_info(date, duration)}: {', '.join(map(format_id, not_available_usernames))}\n"
        options = ["Try another time", "Schedule it anyway"]
        formated_output = format_output_with_cancel(availability_string, options)
        user_schedule.add_schedule_meeting_retry_schedule_interaction(author_id, to_meet_usernames, date, duration)
    else:
        availability_string = "You can have a meeting at that time"
        options = ["Choose another time", "Schedule it"]
        formated_output = format_output_with_cancel(availability_string, options)
        user_schedule.add_schedule_meeting_retry_schedule_interaction(author_id, to_meet_usernames, date, duration)

    return [formated_output, False]


def process_schedule_meeting_retry_schedule(author_id: int, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    
    data = user.get_current_interaction_data(author_id)
    to_meet_usernames = data['to_meet_usernames']

    if option_chosen == 0:
        user.cancel_current_interaction(author_id)
        return ["Canceled", False]
    
    elif option_chosen == 1:
        title = "Try another time"
        message_string = get_schedule_meeting_format_message(title)
        user_schedule.add_schedule_meeting_interaction(author_id, to_meet_usernames)
        return [message_string, False]
    elif option_chosen == 2:

        date: datetime = data['date']
        duration: int = data['duration']
        added = user_schedule.add_meeting(author_id, to_meet_usernames, date,  duration)
        meeting_string = format_meeting_string(data)
        if added:
            message_string = f"Meeting scheduled on your calendar {meeting_string}"
            user.cancel_current_interaction(author_id)
        else:
            message_string = f"That meeting on {meeting_string} is already scheduled"
        return [message_string, False]
    else:
        return ["Option not recognized", False]
    

def process_deschedule_meeting(author_id, public, command):
    option_chosen = get_option_chosen(command)

    if option_chosen == -1:
        return ["Option not recognized", False]
    
    if option_chosen == 0:
        user.cancel_current_interaction(author_id)
        return ["Canceled", False]
    
    meetings = user_schedule.get_meetings(author_id)

    if option_chosen < 1 or option_chosen > len(meetings):
        return ["Option not recognized", False]
    
    meeting = meetings[option_chosen-1]

    user_schedule.remove_meeting(author_id, meeting)

    title = "Descheduled meeting"
    return [title, False]

def process_reserve_office(message, author_id, public, command):
    option_chosen = get_option_chosen(command)

    if option_chosen == 0:
        user.cancel_current_interaction(author_id)
        return ["Canceled", False]
    
    
    content = message.content[1:]
    content = content.split(";")
    content = list(filter(lambda x: x != "", content))
    content = list(map(str.strip, content)) # Check if this works

    input_date = content[0]
    input_time = content[1]
    duration = content[2]

    if not duration.isdigit():
        return [get_schedule_meeting_format_message("Duration must be number"), False]
    else:
        duration = int(duration)

    hours_minutes = get_hours_minutes_from_formated_time_input(input_time)
    if hours_minutes is None:
        return [get_schedule_meeting_format_message("Start time must be in the format HH:mm"), False]
    
    hours, minutes = hours_minutes

    date = get_date(input_date)

    if date is None:
        return [get_schedule_meeting_format_message("Day must be in the format DD/MM/YYYY"), False]
    
    
    full_date = date.replace(hour=hours, minute=minutes)
    now_date = datetime.now()

    if full_date < now_date:
        return ["Date must be in the future", False]

    if len(content) > 3:
        motivation = content[3]
    else:
        motivation = ""

    if len(content) > 4:
        observation = content[4]
    else:
        observation = ""

    # Get the best slot
    decimal_hour = hours
    if minutes < 30:
        pass
    else: # minutes >= 30:
        decimal_hour += 0.5

    decimal_duration_hours = duration // 60
    decimal_duration_minutes = duration % 60
    if decimal_duration_minutes == 0:
        pass
    elif decimal_duration_minutes <= 30:
        decimal_duration_hours += 0.5
    else:
        decimal_duration_hours += 1

    office_reservation = {
        "date": date,
        "start_time": decimal_hour,
        "duration": decimal_duration_hours,
        "motivation": motivation,
        "observation": observation
    }
    user_office.add_confirm_reserve_office_interaction(author_id, office_reservation)

    pretitle = "Office reservation " + format_office_reservation(office_reservation)
    options = ["Change parameters", "Confirm"]
    formated_output = format_output_with_cancel(pretitle, options)
    return [formated_output, False]
           
def process_confirm_reserve_office(author_id, public, command):
    option_chosen = get_option_chosen(command)

    if option_chosen == -1:
        return ["Option not recognized", False]
    
    if option_chosen == 0:
        user.cancel_current_interaction(author_id)
        return ["Canceled", False]
    
    elif option_chosen == 1:
        message = get_reserve_office_format_message()
        user_office.add_reserve_office_interaction(author_id)
        return [message, False]
    elif option_chosen == 2:
        office_reservation = user.get_current_interaction_data(author_id)
        added, confirmation_message = user_office.add_office_reservation(author_id, office_reservation)

        user.cancel_current_interaction(author_id)
        if not added:
            confirmation_message = "API error: " + confirmation_message
        return [confirmation_message, False]

    else:
        return ["Option not recognized", False]
    
def process_cancel_office(author_id, public, command):
    option_chosen = get_option_chosen(command)
    
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    if option_chosen == 0:
        user.cancel_current_interaction(author_id)
        return ["Canceled", False]
    
    data = user.get_current_interaction_data(author_id)

    if option_chosen < 1 or option_chosen > len(data):
        return ["Option not recognized", False]
    
    office_reservation = data[option_chosen-1]
    removed, confirmation_message = user_office.cancel_office_reservation(author_id, office_reservation)


    user.cancel_current_interaction(author_id)
    if not removed:
        confirmation_message = "API error: " + confirmation_message
    return [confirmation_message, False]




def get_option_chosen(command):
    option_chosen = command[1:].strip()
    try:
        option_chosen = int(option_chosen)
    except:
        return -1
    return option_chosen

def format_unnumbered_output(title, options):
    output = title + '\n' + '\n'.join(options)
    return output

def format_output(title, options):
    numbered_options = [f'{index+1}: {elm}' for index, elm in enumerate(options)] 
    output = title + '\n' + '\n'.join(numbered_options)
    return output

def format_unnumbered_output_with_cancel(title, options):
    unnumbered_options = '\n'.join(options)
    output = title + '\n' + unnumbered_options + '\n' + "0: Cancel"
    return output

def format_output_with_cancel(title, options):
    numbered_options = [f'{index+1}: {elm}' for index, elm in enumerate(options)] 
    output = title + '\n' + '\n'.join(numbered_options) + '\n' + "0: Cancel"
    return output

def get_day_from_day_index(day_index: int) -> Tuple[str, str]:
    days = ["2ª feira", "3ª feira", "4ª feira", "5ª feira", "6ª feira", "Sábado", "Domingo"]
    gender = ["a", "a", "a", "a", "a", "o", "o"]
    return days[day_index], gender[day_index]

def format_time(start_time): # start_time in minutes of a day
    hours = int(start_time//60)
    minutes = int(start_time%60)
    start_time_str = f"{hours:02d}:{minutes:02d}"
    return start_time_str

def format_week_slot_string(slot: Tuple[int, int]) -> str:
    week_time = 7 * 24 * 60 # 10080
    week_start_time = slot[0]
    week_end_time = slot[1]

    if week_end_time < week_start_time:
        print(f"LOG:{format_week_slot_string.__name__}: week_end_time < week_start_time")
    
    day = week_start_time // (24 * 60) + 1
    start_time = week_start_time % (24 * 60)
    duration = week_end_time - week_start_time
    return format_time_info(day, start_time, duration)


def format_time_info(day: int, start_time: int, duration:int) -> str:
    day_slot_string = f"{get_day_from_day_index(day)[0]} at {format_time(start_time)}-{format_time(start_time + duration)}"
    return day_slot_string

def format_absolute_time_slot_info(date: datetime, duration: int) -> str:
    final_date = date + timedelta(minutes=duration)
    if date.day == final_date.day:
        day_slot_string = f"{format_date_date(date)} at {format_time(date.hour*60 + date.minute)}-{format_time(final_date.hour*60 + final_date.minute)}"
    else:
        day_slot_string = f"{format_date_date(date)} at {format_time(date.hour*60 + date.minute)}-{format_date_date(final_date)} at {format_time(final_date.hour*60 + final_date.minute)}"

    return day_slot_string

def format_date_date(date: datetime) -> str:
    format = "%d/%m/%Y"
    date_string = date.strftime(format)
    return date_string

def get_hours_minutes_from_formated_time_input(time_input: str) -> None | Tuple[int, int]:
    pattern = r'^([0-1]?[0-9]|2[0-3]):([0-5][0-9])$'
    if not (re.match(pattern,  time_input)):
        return None
    else:
        hours, minutes = time_input.split(":")
        hours = int(hours)
        minutes = int(minutes)
        return hours, minutes


def get_time_from_formated_time_input(time_input: str) -> None | int:
    hours_minutes = get_hours_minutes_from_formated_time_input(time_input)
    if hours_minutes is None:
        return None
    else:
        hours, minutes = hours_minutes
        return hours * 60 + minutes
        
    
def get_date(date) -> datetime | None:
    formats = ['%d-%m-%Y', '%d/%m/%Y', '%d-%m-%y', '%d/%m/%y']
    for fmt in formats:
        try:
            date_obj = datetime.strptime(date, fmt)
            return date_obj
        except ValueError:
            pass
    return None


def format_manual_schedule(schedule: dict):
    institution = schedule['institution']
    class_name = schedule['class']
    lesson_type = schedule['lesson_type']
    day = schedule['day']
    start_time = schedule['start_time']
    duration = schedule['duration']
    location = schedule['location']
    
    day_name, day_gender = get_day_from_day_index(day)
    day_string = f"n{day_gender} {day_name}"
    start_time_str = format_time(start_time)
    end_time_str = format_time(start_time + duration)
    schedule_string = f"{institution} de {class_name} ({lesson_type}): {day_string} às {start_time_str}-{end_time_str} {'' if location is None else f' em {location}'}"
    return schedule_string

def format_api_joint_class (schedule: dict):
    faculty = schedule['faculty']
    faculty_name = faculty['name']
    course = schedule['course']
    course_acronym = course['acronym']
    course_unit = schedule['course_unit']
    course_unit_acronym = course_unit['acronym']
    class_name = schedule['name']
    lesson_type = schedule['lesson_type']
    day = schedule['day']
    start_time = schedule['start_time']
    duration = schedule['duration']
    location = schedule['location']

    schedule_string = f"{faculty_name} {course_acronym} {course_unit_acronym} {class_name} ({lesson_type}): {get_day_from_day_index(day)[0]} {format_time(start_time)}-{format_time(start_time + duration)} {'' if location is None else f' em {location}'}"
    return schedule_string

def get_wrong_format_message(wrong_format_message = "Wrong format"):
    content_items = ["<descricao de instituicao (por exemplo: faculdade, curso, cadeira)", "aula", "tipo de aula", "dia (de 0 - 2ª - a 6 - domingo -)", "hora inicio (HH:mm)", "duracao (minutos)"]
    optional_content_items = ["local"]
    error_message = wrong_format_message
    content = f"Formato:! " + "; ".join(map (lambda x: f"<{x}>", content_items)) 
    content += "; " + "; ".join(map (lambda x: f"[<{x}>]", optional_content_items))
    cancel = "0: Cancel"
    message = error_message + '\n' + content + '\n' + cancel
    return message


def get_schedule_minutes_slots(schedule: List[dict]):

    self_classes = [class_['class'] for class_ in schedule]
    week_occupied = user_schedule.get_week_occupancy_from_classes(self_classes)
   
    non_week_crossover_occupancy = get_non_week_crossover_occupancy(week_occupied)
    contiguous_week_occupied = get_contiguous_week_occupancy(non_week_crossover_occupancy)

    return contiguous_week_occupied

def get_non_week_crossover_occupancy(week_occupancy: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    week_occupied_sorted = sorted(week_occupancy, key=lambda x: x[1])
    unfold_midnight_saturday_edge_case = []
    week_maximum_time = 7 * 24 * 60 # 10080
    for i in range(len(week_occupied_sorted)-1, -1, -1):
        start_time, end_time = week_occupied_sorted[i]
        if end_time > week_maximum_time: # Went past the week maximum minutes, and started on 0 (for the first day)
            unfold_midnight_saturday_edge_case.append((0, end_time - week_maximum_time))
            week_occupied_sorted[i] = (start_time, week_maximum_time)
        else:
            break
    non_week_crossover_occupancy = unfold_midnight_saturday_edge_case + week_occupied_sorted
    return non_week_crossover_occupancy

def get_contiguous_week_occupancy(week_occupancy: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    if len(week_occupancy) == 0:
        return []
    if len(week_occupancy) == 1:
        return week_occupancy
    
    ordered_week_occupancy = sorted(week_occupancy, key = lambda x: x[0])
    contiguous_week_occupied = []
    prev_start, prev_end = ordered_week_occupancy[0]
    for i in range(1, len(ordered_week_occupancy)):
        this_start, this_end = ordered_week_occupancy[i]

        if this_start <= prev_end:
             if this_end > prev_end:
                prev_end = this_end
        else:
            contiguous_week_occupied.append((prev_start, prev_end))
            prev_start, prev_end = this_start, this_end
    contiguous_week_occupied.append((prev_start, prev_end))
    return contiguous_week_occupied

def get_intersect_week_occupancy_slot(to_intersect_slot: Tuple[int, int], target_slot: Tuple[int, int]) -> Tuple[int, int] | None:
    target_start_time, target_end_time = target_slot
    slot_start_time, slot_end_time = to_intersect_slot

    if target_start_time >= slot_start_time and target_start_time < slot_end_time:
        # Target start time is inside one of the slots
        return to_intersect_slot
    elif target_end_time > slot_start_time and target_end_time <= slot_end_time:
        # Target end time is inside one of the slots
        return to_intersect_slot
    elif target_start_time <= slot_start_time and target_end_time >= slot_end_time:
        # Target slot contains one of the slots
        return to_intersect_slot
    return None

def get_intersect_absolute_slots(to_intersect_slot: Tuple[datetime, int], target_slot: Tuple[datetime, int]) -> Tuple[datetime, int] | None:
    to_intersect_start_date, to_intersect_duration = to_intersect_slot
    target_start_date, target_duration = target_slot

    to_intersect_end_date = to_intersect_start_date + timedelta(minutes=to_intersect_duration)
    target_end_date = target_start_date + timedelta(minutes=target_duration)

    if to_intersect_start_date >= target_start_date and to_intersect_start_date < target_end_date:
        # Target start time is inside one of the slots
        return to_intersect_slot
    
    elif to_intersect_end_date > target_start_date and to_intersect_end_date <= target_end_date:
        # Target end time is inside one of the slots
        return to_intersect_slot
    
    elif to_intersect_start_date <= target_start_date and to_intersect_end_date >= target_end_date:
        # Target slot contains one of the slots
        return to_intersect_slot
    return None

def get_schedule_meeting_format_message(pretitle: str = "") -> str:
    
    content_items = ["dia (dd/MM/YYYY)", "hora (HH:mm)", "duracao (minutos)"]
    content = f"Formato:! " + "; ".join(map (lambda x: f"<{x}>", content_items))
    cancel = "0: Cancel"
    if pretitle != "":
        pretitle += '\n'
    message = pretitle + content + '\n' + cancel
    return message

def get_reserve_office_format_message(pretitle: str = "") -> str:
    content_items = ["dia (dd/MM/YYYY)", "hora (HH:mm)", "duration (minutos)"]
    optional_content_items = ["motivation", "special request"]
    content = f"Formato:! " + "; ".join(map (lambda x: f"<{x}>", content_items))
    content += "; " + "; ".join(map (lambda x: f"[<{x}>]", optional_content_items))
    cancel = "0: Cancel"
    if pretitle != "":
        pretitle += '\n'
    message = pretitle + content + '\n' + cancel
    return message


def format_id(id):
    return f"<@{id}>"

def format_meeting_string_parts(meeting: dict):
    to_meet_usernames = meeting['to_meet_usernames']
    date = meeting['date']
    duration = meeting['duration']

    to_meet_usernames_string = ', '.join(map(format_id, to_meet_usernames))
    time_string = format_absolute_time_slot_info(date, duration)

    return to_meet_usernames_string, time_string

def format_meeting_string(meeting: dict):
    to_meet_usernames_string, time_string = format_meeting_string_parts(meeting)
    return f"on {time_string} with {to_meet_usernames_string}"

def format_event_string(event: dict):
    date = event['date']
    duration = event['duration']
    name = event['name']
    time_string = format_absolute_time_slot_info(date, duration)
    return f"{name} on {time_string}"

def format_office_reservation(office_reservation: dict):
    date = office_reservation['date']
    start_time = office_reservation['start_time'] #decimal hours
    duration = office_reservation['duration'] #decimal hours
    motivation = office_reservation['motivation']
    observation = office_reservation['observation']

    canonical_duration = duration * 60
    hours = int(start_time)
    minutes = int((start_time - hours) * 60)
    date = date.replace(hour=hours, minute=minutes)
    time_string = format_absolute_time_slot_info(date, canonical_duration)
    office_string = f"{time_string}"
    if motivation != "":
        office_string += f" with motivation \"{motivation}\""
    if observation != "":
        office_string += f" with special request \"{observation}\""
    return office_string