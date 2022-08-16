import costants as keys
from telegram.ext import *
import responses as R
import time
from dbGestione import admins
from sqlite import db
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

chatSession = 0
loginSession = False
isLoggedIn = False
username = ""
password = ""
From_Email = "casadomoticasender@gmail.com"
To_Email = "casadomotica202202@gmail.com"
From_Pwd = "casadomoticasender"

print("Bot started.....")

def start_command(update, context):
    update.message.reply_text('Type something to get started!')

def help_command(update, context):
    if isLoggedIn == False:
        update.message.reply_text('/registrati - per fare la registrazione. \n /login - per fare il login. \n /logout - per fare il logout. \n /cancel - per annulare un azione.')
    else:
        update.message.reply_text('*Gestione casa domotica*\n /accendi - accendere la luce. \n /spegni - spegnere la luce \n *Commandi normali* \n /logout - per fare il logout. \n /cancel - per annulare un azione.')

def handle_message(update, context):
    text = str(update.message.text).lower()
    if chatSession == 0:
        response = R.sample_responses(text)
        update.message.reply_text(response)
    elif chatSession == 1: 
        global username
        username = text
        passwordAdmin(update, context)          
    elif chatSession == 2: 
        global password
        password = text
        if loginSession == True:
            login(update, context)
        else:
            registrazione(update, context)           

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def nomeAdmin(update, context):
    text = str(update.message.text).lower()
    global chatSession
    chatSession = 1
    if text == "/login":
        if isLoggedIn ==True:
            update.message.reply_text(text='Bro, Sei gia dentro 😐')
            cleanup()
            return None
        else:
            global loginSession
            loginSession = True 
            update.message.reply_text(text='Scrivi tuo username🔎')
    elif text == "/registrati":  
        if isLoggedIn ==True:
            update.message.reply_text(text='Bro cosa vuoi quando sei gia entrato con tuo account 😐')
            return None
        else:
            update.message.reply_text(text='Scrivi tuo username🔎')             
        

def passwordAdmin(update, context):
    global chatSession
    chatSession = 2
    update.message.reply_text(text='Scrivi tuo password 👀')

def annulazione(update, context):
    global chatSession 
    if chatSession != 0:        
        cleanup()
        update.message.reply_text(text='Registrazione annulata 🙅‍♂️.')
    else:
        update.message.reply_text(text='Cancella cosa? Non hai inziato niente 🤦‍♂️')

def login(update, context):
        global loginSession, isLoggedIn
        loginSession = False
        global chatSession

        database = db()
        admin = database.get_admin(username, password)
        if admin != None:
            update.message.reply_text(text='Sei dentro 😎🥶. Per vedere cosa puoi fare usa il commando /help')  
            isLoggedIn = True           
            chatSession = 0
        else:
            update.message.reply_text(text='Oh shit 😲! Username o password sbagliata. \n Forza💪!. Puoi riprovare con il commando /login')
            isLoggedIn = False
            chatSession = 0

def logout(update, context):
        global isLoggedIn
        if isLoggedIn == False:
            update.message.reply_text(text='Bro, Non sei neancho loggato 🤦‍♂️')
        else:
           isLoggedIn = False
           cleanup()
           update.message.reply_text(text='Sei fuori 😔!')
        

        
def registrazione(update, context):
    database = db()
    id = database.get_last_id() + 1
    chad = admins(id, username, password)
    database.insert_admin(chad)

    cleanup()  
    update.message.reply_text(text='Sei stato registrato 💪. \n Ora puoi fare la login con il commando /login')

def gestione_luce(update, context):
    text = str(update.message.text).lower()
    if isLoggedIn == False:
        update.message.reply_text(text='Devi fare il login prima fra')
        return None
    if text == "/accendi":
        message = MIMEMultipart()
        message['from'] = From_Email
        message['To'] = To_Email
        message['subject'] = 'accendi la luce'
        mail_context = 'less goooo'
        message.attach(MIMEText(mail_context, 'plain'))

        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(From_Email, From_Pwd)
        msg = message.as_string()
        session.sendmail(From_Email, To_Email, msg)
        session.quit()
        update.message.reply_text(text='accendo la luce fra 3....2....1.....')
        time.sleep(3)
        update.message.reply_text(text='accesso')
    elif text == "/spegni":
        message = MIMEMultipart()
        message['from'] = From_Email
        message['To'] = To_Email
        message['subject'] = 'spegni la luce'
        mail_context = 'less goooo'
        message.attach(MIMEText(mail_context, 'plain'))

        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(From_Email, From_Pwd)
        msg = message.as_string()
        session.sendmail(From_Email, To_Email, msg)
        session.quit()
        update.message.reply_text(text='spengo la luce fra 3....2....1.....')
        time.sleep(1)
        update.message.reply_text(text='spento')
    


def cleanup():
    global loginSession
    loginSession = False
    global chatSession 
    chatSession = 0
    global username
    username = ""
    global password
    password = ""



def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("registrati", nomeAdmin))
    dp.add_handler(CommandHandler("cancel", annulazione))
    dp.add_handler(CommandHandler("login", nomeAdmin))
    dp.add_handler(CommandHandler("logout", logout))
    dp.add_handler(CommandHandler("accendi", gestione_luce))
    dp.add_handler(CommandHandler("spegni", gestione_luce))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()



main()





