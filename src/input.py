import user
from events.interaction import Interaction
from database.database_api import api

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
        
        if user.get_current_interaction(message.author.name) == Interaction.ADD_SCHEDULE:
            return process_add_schedule(message, public, command)

        if user.get_current_interaction(message.author.name) == Interaction.CHOOSE_FACULTY_TO_ADD:
            return process_choose_faculty_to_add(message, public, command)

    return ["Unknown command", False]

def process_add_schedule(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    if option_chosen == 1:
        faculties = api.get_faculties()
        title = "Faculdades disponiveis"
        options = [f"{faculty.acronym}: {faculty.name.strip()}" for faculty in faculties]
        formated_output = format_output(title, options)
        user.add_choose_faculty_to_add_schedule_interaction(message.author.name, faculties)
        return [formated_output, False]
    elif option_chosen == 2:
        pass
    elif option_chosen == 3:
        pass
    else:
        return ["Option not recognized", False]

def process_choose_faculty_to_add(message, public, command):
    option_chosen = get_option_chosen(command)
    if option_chosen == -1:
        return ["Option not recognized", False]
    
    faculties = user.get_current_interaction_data(message.author.name)
    if option_chosen < 0 or option_chosen > len(faculties):
        return ["Option not recognized", False]
    faculty = faculties[option_chosen-1]
    added = user.add_current_faculty(message.author.name, faculty.acronym)
    if added:
        return [f"Added {faculty.acronym}: {faculty.name.strip()}", False]
    else:
        return ["You already added this faculty", False]


def get_option_chosen(command):
    option_chosen = command[1:].strip()
    try:
        option_chosen = int(option_chosen)
    except:
        return -1
    return option_chosen
def format_output(title, options):
    numbered_options = [f'{index}. {elm}' for index, elm in enumerate(options)] 
    output = title + '\n' + '\n'.join(numbered_options)
    return output