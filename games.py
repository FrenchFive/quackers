import random

def roll(num):
    dicelist = []
    for i in range(num):
        dicelist.append(random.randint(1,6))
    return(dicelist)

def dices(num, money, name):
    botroll = roll(num)
    userroll = roll(num)

    bottotal = sum(botroll)
    usertotal = sum(userroll)

    response = ""
    for i in range(num):
        response+= f'ROUND {i+1}\n'
        response+= f'{name.capitalize()} rolls a {userroll[i]}\n'
        response+= f'Quackers rolls a {botroll[i]}\n'
        response+= ' \n'
    
    if bottotal > usertotal:
        response+= f'\nQuackers WON // with {bottotal} over {usertotal}\n'
        response+= f'{money} <:quackCoin:1124255606782578698> removed from {name} balance.'
        end = 0
    elif usertotal > bottotal :
        response+= f'\n{name.capitalize()} WON // with {usertotal} over {bottotal}\n'
        response+= f'{money} <:quackCoin:1124255606782578698> added to {name} balance.'
        end = 1
    else :
        response+= f'\nEGALITE !!! // with {usertotal} over {bottotal}\n'
        end = 2
    
    return(response, end)

def rps(user, bet, name):
    play = ["scissors","paper","rock","lizard","spock"]
    emoji = ['✂️', '🧻', '🪨', '🦎', '🖖']
    bot = random.randint(0, len(play)-1)

    if user == bot:
        gameresult = 0
        text = "EGALITE"
    elif user+1 == bot or user-2 == bot or user+1 == bot+5 or user-2 == bot-5:
        gameresult = 1
        text = f'\n {name} a GAGNE !!! // {bet} <:quackCoin:1124255606782578698> gagnés'
    elif bot+1 == user or bot-2 == user or bot+1 == user+5 or bot-2 == user-5:
        gameresult = -1
        text = f'\n {name} a PERDU !!! // {bet} <:quackCoin:1124255606782578698> perdus'
    else:
        return('ERROR', 0)
    
    tosay = f'{name} a joué : {play[user]} - {emoji[user]} \n'
    tosay += f'Quackers a joué : {play[bot]} - {emoji[bot]} \n'
    tosay += text

    return(tosay, gameresult)
    