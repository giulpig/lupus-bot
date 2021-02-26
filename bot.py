import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from enum import Enum
import pymongo


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




roles = {    
    "wolf"    : 0,   #roles with number of players per role (input by players)
    "bitch"   : 0,
    "medium"  : 0,
    "madman"  : 0,
    "peasant" : 0               #
}                               #
                                #  RESET GLOBALS IN STARTGAME
uid_to_cid = {}                 #
players = []                    #
active_uids = set()
cids = set()
n_players = 0
roled = 0

state = State.STARTED




class Player():
    def __init__(self, role, uid, cid):
        self.role = role
        self.uid = uid
        self.cid = cid








def sync_database():
    cids = set()
    lst_users = db.distinct(key="uid")
    for i in lst_users:
        cid = db.find_one({"uid":i})["cid"]
        cids.add(cid)


    


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    """Saluto iniziale"""
    if update.message.chat.type != "group":
        update.message.reply_text('Welcome, FIGA!')

        lst_users = db.distinct(key="uid")
        if str(update.message.from_user.id) in lst_users:
            db.update_one({"uid" : str(update.message.from_user.id)}, { "$set": { 'cid':  str(message.chat.id)} })
        else:
            db.insert_one({"uid":str(update.message.from_user.id), "cid":str(message.chat.id)})








def startGame(update, context):
    global state
    global n_players
    global players
    global roled
    global uid_to_cid
    global active_uids
    global cids
    global roles

    roles = {
        "wolf"    : 0,   #reset globals
        "bitch"   : 0,
        "medium"  : 0,
        "madman"  : 0,
        "peasant" : 0
    }

    uid_to_cid = {}
    players = []
    active_uids = set()
    cids = set()
    n_players = 0
    roled = 0

    state = State.STARTED


    update.message.reply_text('How many players?')
    
    
    
def join(update, context):
    global state
    global n_players
    global players
    global roled

    #update.message.reply_text(str(update.message.from_user.id) + " v0")
    
    if state == State.SETPLAYERS:
        #update.message.reply_text(update.message.chat.username + " v1")
        if not update.message.from_user.id in active_uids:
            players.append(Player("", str(update.message.from_user.id), ""))
            active_uids.add(update.message.from_user.id)
        else:
            update.message.reply_text("You can't join twice")

        if len(players) == n_players:
            state = State.JOINED
            #for i in players:
            #    update.message.reply_text(str(i.pid))

            lst_users = db.distinct(key="uid")


            update.message.reply_text("How many wolves?")
    

        
    
    
    
def update_from_text(update, context):
    global state
    global n_players
    global players
    global roled

    if state == State.FINISHED:
        return

    elif state == State.STARTED:  #input Nplayers
        temp = 0
        try:
            temp = int(update.message.text)
            #update.message.reply_text('got input')
        except Exception as e:
            pass
        

        ###DA RIMETTERE
        if False:  #(temp < 4 or temp > 30):
            update.message.reply_text('Wrong input, this must be a positive number between 4 and 30')
        
        else:
            n_players = temp
            state = State.SETPLAYERS
            #update.message.reply_text('You set ' + str(n_players) + ' players')
            update.message.reply_text('Now join with /join')
            
        return
        


    elif state == State.JOINED:  #input Nwolfes
        temp = 0
        try:
            temp = int(update.message.text)
            #update.message.reply_text('got input')
        except Exception as e:
            pass
        

        ###DA RIMETTERE
        if False:  #(temp < 0 or roled + temp > n_players):
            update.message.reply_text('Wrong input, this must be a positive number between 4 and 30')
        
        else:
            roles["wolf"] = temp
            roled += temp
            state = State.WOLFED
            #update.message.reply_text(str(roles["wolf"]) + ' wolf/ves')
            update.message.reply_text('How many bitches?')
            
        return



    elif state == State.WOLFED:  #input Nbitches
        temp = 0
        try:
            temp = int(update.message.text)
            #update.message.reply_text('got input')
        except Exception as e:
            pass
        

        ###DA RIMETTERE
        if False:  #(temp < 0 or roled + temp > n_players):
            update.message.reply_text('Wrong input, this must be a positive number between 4 and 30')
        
        else:
            roles["bitch"] = temp
            roled += temp
            state = State.BITCHED
            #update.message.reply_text(str(roles["bitch"]) + ' bitch/es')
            update.message.reply_text('How many mediums?')
            
        return



    elif state == State.BITCHED:  #input Nbitches
        temp = 0
        try:
            temp = int(update.message.text)
            #update.message.reply_text('got input')
        except Exception as e:
            pass
        

        ###DA RIMETTERE
        if False:  #(temp < 0 or roled + temp > n_players):
            update.message.reply_text('Wrong input, this must be a positive number between 4 and 30')
        
        else:
            roles["medium"] = temp
            roled += temp
            state = State.MEDIUMED
            #update.message.reply_text(str(roles["medium"]) + ' medium/s')
            update.message.reply_text('How many madmans?')
            
        return




    elif state == State.MEDIUMED:  #input Nbitches
        temp = 0
        try:
            temp = int(update.message.text)
            #update.message.reply_text('got input')
        except Exception as e:
            pass
        

        ###DA RIMETTERE
        if False:  #(temp < 0 or roled + temp > n_players):
            update.message.reply_text('Wrong input, this must be a positive number between 4 and 30')
        
        else:
            roles["madman"] = temp
            roled += temp
            state = State.MEDIUMED
            #update.message.reply_text(str(roles["madman"]) + ' madman/s')

            update.message.reply_text("Ok, now everyone will have his role in a private chat")
            
        return
        







    
def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Col cazzo che ti aiuto, non ho tempo da perdere, chiedi a Giulio')

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
