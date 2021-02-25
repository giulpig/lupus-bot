import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from enum import Enum



PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '1658482800:AAGvwDHhrxIeevOo3a9Ig5uJKFXOGgMDB90'


#          0        1         2         3         4
roles = ["wolf", "bitch", "medium", "madman", "peasant"]
players = []
n_players = 0




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
    


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    """Saluto iniziale"""
    update.message.reply_text('Welcome, FIGA!')
    
def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Col cazzo che ti aiuto, non ho tempo da perdere, chiedi a Giulio')










def startGame(update, context):
    update.message.reply_text('How many players?')
    state = State.STARTED
    
    
def update_from_text(update, context):
    if state == State.FINISHED:
        return
    elif state == State.STARTED:
        temp = 0
        try:
            temp = int(update.message.text)
        except Exception as e:
            update.message.reply_text('Wrong input, this must be a number')
        
        if(temp < 4 or temp > 30):
            update.message.reply_text('Wrong input, this must be a positive number between 3 and 30')
            break
        
        else:
            n_players = temp
            state = State.SETPLAYERS
            update.message.reply_text('There are ' + n_players + ' players')
        return
        
        
        








def echo(update, context):
    """Echo the user message."""
    #update.message.reply_text(update.message.text + " coglione")
    update.message.reply_text("sei un coglione")

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
    dp.add_handler(CommandHandler("join",      startGame)) #startGame handler
    dp.add_handler(CommandHandler("stopjoin",  startGame)) #startGame handler
    dp.add_handler(CommandHandler("getroles",  startGame))
    
   
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