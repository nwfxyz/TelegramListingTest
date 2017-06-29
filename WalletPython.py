# -*- coding: utf-8 -*-
## To do : Curlist not being global

"""Chat Bot Test """
import re
import logging 
import os
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler,CallbackQueryHandler)
import pickle

formatter = logging.Formatter('%(asctime)s,%(levelname)s,%(message)s')



CREATE2,CREATE3,CREATE4,CREATE5 = range(4)
curList = {}



def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_object(filename):
    with open(filename, 'rb') as input:
        load = pickle.load(input)
    return load

class Listing():
    Title = []
    Desc = []
    Price = []
    Image = []
    
    def __init__(self,Type):
        self.Type = Type
        


def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

logger = setup_logger('main_logger', 'main_logfile.log')
logger.info('Test')

logger = setup_logger('main_logger', 'Info\main_logfile.log')
logger.info('Test2')

def start(bot,update):
    user = update.message.from_user
    update.message.reply_text(
            'Hi ' + str(user.first_name) + '\n' +
            'Pleased to meet you\n' +
            'Welcome to the Listing Bot\n' +
            'type /help for details'
           )
    return ConversationHandler.END

def completelisting(userid,ListID):
    List_dir = "Processing\\user" + str(userid)
    stging_list = load_object(List_dir + '\\' + ListId + '.pkl')
    Title = stging_list.Title
    Desc = stging_list.Desc
    
    
    
  
def create(bot,update,user_data):
    user_data['id'] = update.message.from_user.id
    keyboard = [[InlineKeyboardButton("Stock", callback_data='Stock')],
                 [InlineKeyboardButton("Rental Space", callback_data='Rental')],
                [InlineKeyboardButton("Others", callback_data='Others')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    
    return CREATE2
 

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command. Type /help for commands.")
    


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def help1(bot,update):
    update.message.reply_text(
            '<b>Commands</b>\n\n'  +
            '/create add listing\n' + 
            '\n',
             reply_markup=ReplyKeyboardRemove(),
             parse_mode = 'HTML')
    
    return ConversationHandler.END


def NewFolder(FolderName):
    if not os.path.exists(FolderName):
          os.makedirs(str(FolderName))


    
def NewListing(bot,update,user_data):
    
    query = update.callback_query
    userid = user_data['id']
    List_dir = "Processing\\user" + str(userid)
    NewFolder(List_dir)
    Prev_Listing = os.listdir(List_dir)
    if len(Prev_Listing) == 0:
        ListId = str('0001')
    else:
        ListId = str(max([int( re.sub('\.pkl','',i)) for i in Prev_Listing if 'pkl' in i]) + 1).zfill(4)
        
    user_data['curr'] = ListId
    bot.edit_message_text(message_id=query.message.message_id,chat_id = query.message.chat_id,
                          text = "ListID =" + str(userid) + str(ListId) + "\nType:" + query.data + "\nPlease give us a listing title")
    stging_list = Listing(query.data)
    save_object(stging_list,List_dir + '\\' + ListId + '.pkl')
    return CREATE3
     
def AddTitle(bot,update,user_data):
    
    user = update.message.from_user
    userid = user.id
    
  
    
    if len(str(update.message.text)) < 50 :
          List_dir = "Processing\\user" + str(userid)
          ListId = user_data['curr']
          stging_list = load_object(List_dir + '\\' + ListId + '.pkl')
          stging_list.Title = update.message.text
          update.message.reply_text('Add a description',
                                    reply_markup=ReplyKeyboardRemove())
          save_object(stging_list,List_dir + '\\' + ListId + '.pkl')
          return CREATE4
    else: 
        update.message.reply_text('Title too long, max 50 char',
                                    reply_markup=ReplyKeyboardRemove())
        return CREATE3
    
def AddDesc(bot,update,user_data):
    
    user = update.message.from_user
    userid = user.id
    
  
    
    if len(str(update.message.text)) < 1500 :
          List_dir = "Processing\\user" + str(userid)
          ListId = user_data['curr']
          stging_list = load_object(List_dir + '\\' + ListId + '.pkl')
          stging_list.Desc = update.message.text
          update.message.reply_text('Done. Listing added',
                                    reply_markup=ReplyKeyboardRemove())
          save_object(stging_list,List_dir + '\\' + ListId + '.pkl')
          
          return CREATE5
    else: 
        update.message.reply_text('Desc too long, max 1500 char',
                                    reply_markup=ReplyKeyboardRemove())
        return CREATE4
    



def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("355993039:AAFkJmcjKgQLWz3IWBGz1niXLFq8zq1vH6M")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create', create,pass_user_data = True),
                 
                      CommandHandler('help', help1)
                      ],

        states={
                CREATE2: [CallbackQueryHandler(NewListing,pass_user_data = True)],
                CREATE3: [MessageHandler(Filters.text,AddTitle,pass_user_data = True)]
                
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(CommandHandler("start", start))  
    dp.add_handler(conv_handler)  
    dp.add_handler(MessageHandler(Filters.command,unknown))
#     log all errors
    dp.add_error_handler(error)
    
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
    
