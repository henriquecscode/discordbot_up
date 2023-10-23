import user

def process_input(message):
    #Create an account for the author of the message and all those mentioned, podemos ter de mudar quando formos buscar dados ao sigarra
    user.account_checker(message.author.name)
    for util in message.mentions:
        user.account_checker(util.name)

    if message.content.split()[0] == "!add_friend":
        if len(message.mentions) != 1:
            return "You have to mention which friend you would like to add. Ex.: !add_friend @someone"
        return user.send_friend_request(message.author.name, message.mentions[0].name)

    if message.content.split()[0] == "!friend_requests":
        return user.check_friend_requests(message.author.name)
    
    if message.content.split()[0] == "!accept":
        if len(message.content.split()) < 2:
            return "You have to specify which friend request to accept. Ex.: !accept 1"
        return user.accept_friend_request(message.author.name, int(message.content.split()[1]))
    
    if message.content.split()[0] == "!remove_friend":
        if len(message.content.split()) < 2:
            return "You have to specify which friend to remove. Ex.: !remove_friend @someone"
        if len(message.mentions) != 1:
            return "You have to mention which friend you would like to remove. Ex.: !remove_friend @someone"
        
        return user.remove_friend(message.author.name, message.mentions[0].name)
    
    if message.content.split()[0] == "!friends_list":
        return user.show_friends_list(message.author.name)    
    
    if message.content.split()[0] == "!help":
        return "Available commands:\n!add_friend\n!friend_requests\n!accept\n!friends_list\n!remove_friend"
    
    return "Command not recognized, write !help for help"
