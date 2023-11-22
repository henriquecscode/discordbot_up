import user

def process_input(message, public):
    #Create an account for the author of the message and all those mentioned, podemos ter de mudar quando formos buscar dados ao sigarra
    user.account_checker(message.author.name)
    for util in message.mentions:
        user.account_checker(util.name)

    if message.content.split()[0] == "!add_friend":
        if len(message.mentions) != 1:
            return ["You have to mention which friend you would like to add. Ex.: !add_friend @someone", False]
        return [user.send_friend_request(message.author.name, message.mentions[0].name), False]

    if message.content.split()[0] == "!friend_requests":
        return [user.check_friend_requests(message.author.name), False]
    
    if message.content.split()[0] == "!accept":
        if len(message.content.split()) < 2:
            return ["You have to specify which friend request to accept. Ex.: !accept 1", False]
        return [user.accept_friend_request(message.author.name, int(message.content.split()[1])), False]
    
    if message.content.split()[0] == "!remove_friend":
        if len(message.content.split()) < 2:
            return ["You have to specify which friend to remove. Ex.: !remove_friend @someone", False]
        if len(message.mentions) != 1:
            return ["You have to mention which friend you would like to remove. Ex.: !remove_friend @someone", False]
        
        return [user.remove_friend(message.author.name, message.mentions[0].name), False]
    
    if message.content.split()[0] == "!friends_list":
        return [user.show_friends_list(message.author.name), False]
    
    if message.content.split()[0] == "!add_session_cookie":
            if public:
                return ["This is sensitive private information! Please only use this command on private DM's!", True]
            if len(message.content.split()) < 2:
                return ["You have to input your session cookie. Ex.: !add_session_cookie <cookie>", False]
            return [user.add_cookie(message.author.name, int(message.content.split()[1])), True]
    
    if message.content.split()[0] == "!add_username":
        if public:
             return ["This is sensitive private information! Please only use this command on private DM's!", True]
        if len(message.content.split()) < 2:
                return ["You have to input your username. Ex.: !add_username <username>", False]
        return [user.add_username(message.author.name, message.content.split()[1]), True]

    if message.content.split()[0] == "!add_password":
        if public:
             return ["This is sensitive private information! Please only use this command on private DM's!", True]
        if len(message.content.split()) < 2:
                return ["You have to input your password. Ex.: !add_password <password>", False]
        return [user.add_password(message.author.name, message.content.split()[1]), True]

    if message.content.split()[0] == "!help":
        return ["Available commands:\n!add_friend\n!friend_requests\n!accept\n!friends_list\n!remove_friend\n!add_session_cookie", False]
    
    return ["Command not recognized, write !help for help", False]
