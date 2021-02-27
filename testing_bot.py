import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from enum import Enum
import pymongo
import random


#connect database
client = pymongo.MongoClient("mongodb+srv://giulpig:rznstvdE8sCd6A7k@cluster0.5z0dk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db_name = "Lupus_Data"
collection_name = "users"
db = client[db_name][collection_name]



PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '1658482800:AAGvwDHhrxIeevOo3a9Ig5uJKFXOGgMDB90'




class State(Enum):
    STARTED = 0
    SETPLAYERS = 1
    JOINED = 2
    WOLFED = 3
    BITCHED = 4
    MEDIUMED = 5
    MADMANED = 6
    PEASANTED = 7
    FINISHED = 8



class LupusGame():
    def __init__(self):
        self.reset()

    def reset(self):
        self.roles = {    
            "wolf🐺"    : 0,   #roles with number of players per role (input by players)
            "bitch👩‍🎤"   : 0,
            "medium👰"  : 0,
            "madman🤪"  : 0,
            "peasant🧑‍🌾" : 0
        }

        self.uid_to_cid = {}
        self.players = []
        self.active_uids = set()
        self.cids = set()
        self.n_players = 0
        self.roled = 0

        self.state = State.STARTED


class Player():
    def __init__(self, role, uid, cid):
        self.role = role
        self.uid = uid
        self.cid = cid



game = LupusGame()




def sync_database():

    game.cids = set()
    lst_users = db.distinct(key="uid")
    for i in lst_users:
        cid = db.find_one({"uid":i})["cid"]
        game.uid_to_cid[i] = cid
        game.cids.add(cid)


    


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    """Saluto iniziale"""
    if update.message.chat.type == "private":
        update.message.reply_text('Welcome, FIGA! If you have any questions, ask Hulio aka @giulpig')

        lst_users = db.distinct(key="uid")

        #for user in lst_users:
            #update.message.reply_text('UserID: ' + user)

        if str(update.message.from_user.id) in lst_users:
            #update.message.reply_text('Aggiorno: ' + str(update.message.from_user.id))
            db.update_one({"uid" : str(update.message.from_user.id)}, { "$set": { 'cid':  str(update.message.chat.id)} })
            update.message.reply_text('Aptal, You were already registered')
        else:
            #update.message.reply_text('Aggiungo: ' + str(update.message.from_user.id))
            db.insert_one({"uid":str(update.message.from_user.id), "cid":str(update.message.chat.id)})
            update.message.reply_text('You have beeen registered successfully (or at least I hope so)')

    else:
        update.message.reply_text("You can't start from here, start in private at @lupus_bot_camplus")








def startGame(update, context):

    if update.message.chat.type != "group":
        return

    game.reset()

    update.message.reply_text('How many players?')
    
    
    
def join(update, context):

    user_id = str(update.message.from_user.id)

    if update.message.chat.type != "group":
        return

    #update.message.reply_text(str(update.message.from_user.id) + " v0")
    
    if game.state == State.SETPLAYERS:
        #update.message.reply_text(update.message.chat.username + " v1")
        if not user_id in game.active_uids:

            if not user_id in game.uid_to_cid:
                #update.message.reply_text("User " + user_id + " not found")
                update.message.reply_text("User not found")
                update.message.reply_text("You must start the bot @lupus_bot_camplus in private chat first (ask Hulio at @giulpig)")

            else:
                players.append(Player("", user_id , game.uid_to_cid[user_id]))
                game.active_uids.add(user_id)
        else:
            update.message.reply_text("You can't join twice in a game")

        if len(game.players) == game.n_players:
            game.state = State.JOINED

            update.message.reply_text("How many wolves?")
    

        
    
    
    
def update_from_text(update, context):

    if update.message.chat.type != "group":
        return


    update.message.reply_text(str(game.state))

    if game.state == State.FINISHED:
        return

    elif game.state == State.STARTED:  #input Nplayers
        update.message.reply_text('About to input Nplayers')
        temp = 0
        try:
            temp = int(update.message.text)
            #update.message.reply_text('got input')
        except Exception as e:
            pass
        

        ###DA RIMETTERE
        if False:
        #if (temp < 4 or temp > 30):
            update.message.reply_text('Wrong input, players must be between 4 and 30')
        
        else:
            game.n_players = temp
            game.state = State.SETPLAYERS

            update.message.reply_text('About to sync database')
            #update.message.reply_text('You set ' + str(n_players) + ' players')
            sync_database()

            update.message.reply_text('Now join with /join')
            
        return
        


    elif game.state == State.JOINED:  #input Nwolfes
        temp = 0
        try:
            temp = int(update.message.text)
            #update.message.reply_text('got input')
        except Exception as e:
            pass
        

        ###DA RIMETTERE
        if False:  #(temp < 0 or roled + temp > n_players):
            update.message.reply_text('Wrong input, too many')
        
        else:
            game.roles["wolf"] = temp
            game.roled += temp
            game.state = State.WOLFED
            #update.message.reply_text(str(roles["wolf"]) + ' wolf/ves')
            update.message.reply_text('How many bitches?')
            
        return



    elif game.state == State.WOLFED:  #input Nbitches
        temp = 0
        try:
            temp = int(update.message.text)
            #update.message.reply_text('got input')
        except Exception as e:
            pass
        

        ###DA RIMETTERE
        if False:
        #if (temp < 0 or roled + temp > n_players):
            update.message.reply_text('Wrong input, too many')
        
        else:
            game.roles["bitch"] = temp
            game.roled += temp
            game.state = State.BITCHED
            #update.message.reply_text(str(roles["bitch"]) + ' bitch/es')
            update.message.reply_text('How many mediums?')
            
        return



    elif game.state == State.BITCHED:  #input Nbitches
        temp = 0
        try:
            temp = int(update.message.text)
            #update.message.reply_text('got input')
        except Exception as e:
            pass
        

        ###DA RIMETTERE
        if False:
        #if (temp < 0 or roled + temp > n_players):
            update.message.reply_text('Wrong input, too many')
        
        else:
            game.roles["medium"] = temp
            game.roled += temp
            game.state = State.MEDIUMED
            #update.message.reply_text(str(roles["medium"]) + ' medium/s')
            update.message.reply_text('How many madmans?')
            
        return




    elif game.state == State.MEDIUMED:  #input Nbitches
        temp = 0
        try:
            temp = int(update.message.text)
            #update.message.reply_text('got input')
        except Exception as e:
            pass
        

        ###DA RIMETTERE
        if False:
        #if (temp < 0 or roled + temp > n_players):
            update.message.reply_text('Wrong input, too many')
        
        else:
            game.roles["madman"] = temp
            game.roled += temp
            game.state = State.MEDIUMED
            #update.message.reply_text(str(roles["madman"]) + ' madman/s')

            game.roles["peasant"] = n_players - roled

            send_roles(update, context)

            update.message.reply_text("Everyone should have recieved a private message with his role, have fun")

        return
        


def send_roles(update, context):

    random.shuffle(game.players)

    counter = 0
    for role in game.roles:
        for i in range(game.roles[role]):
            game.players[counter].role = role
            counter += 1

    for player in game.players:
        context.bot.send_message(chat_id=player.cid, text="You are a " + player.role[:-1])
        context.bot.send_message(chat_id=player.cid, text=player.role[-1])

    game.state = State.FINISHED





    
def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Col cazzo che ti aiuto, non ho tempo da perdere, chiedi a Hulio aka @giulpig')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)





def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    
    dp.add_handler(CommandHandler("startgame", startGame)) #startGame handler
    dp.add_handler(CommandHandler("join",      join))      #startGame handler
    
   
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, update_from_text))    


    # log all errors
    dp.add_error_handler(error)


    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://protected-inlet-23009.herokuapp.com/' + TOKEN)
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
