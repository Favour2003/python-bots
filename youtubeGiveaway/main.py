from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import constants as keys
from telegram.ext import *
import telegram
import responses as R
import time
import os
import json

statsChatSession = False
videoDownloadChatSession = False
mp3DownloadChatSession = False
videoName = ""
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--start-maximized")
bot = telegram.Bot(keys.API_KEY)

print("Bot started.....")

def start_command(update, context):
    update.message.reply_text('Type something to get started!')

def help_command(update, context):
    update.message.reply_text('/downloadyoutubevideo - per scaricare i video da youtube. \n /downloadyoutubemp3 - per scaricare mp3. \n/getyoutubevideostats \n /cancel - per annulare un azione. \n chat id: ' + str(update.message.chat.id))
    

def handle_message(update, context):
    text = str(update.message.text).lower()
    if (statsChatSession == True):    
        getStats(update, context)
    elif (videoDownloadChatSession == True):
        downloadyoutubevideo(update, context)
    elif (mp3DownloadChatSession == True):
        mp3Download(update, context)
    else:
        response = R.sample_responses(text)
        update.message.reply_text(response)
        
    

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def getYoutubeLink(update, context):
    text = str(update.message.text)
    global statsChatSession
    global videoDownloadChatSession
    global mp3DownloadChatSession
    if (text == "/getyoutubevideostats"):
        statsChatSession = True
    elif(text == "/downloadyoutubevideo"):
        videoDownloadChatSession = True    
    elif (text == '/downloadyoutubemp3'):
        mp3DownloadChatSession = True
    update.message.reply_text('bro, manda il link del video')

def getStats(update, context):
    text = str(update.message.text)
    if(("www.youtube.com" in text and "watch" in text) or "youtu.be" in text):
        driver = webdriver.Chrome(options=options)
        driver.get(text)
      
        try:
            accept = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//ytd-button-renderer[2]//a[1]//tp-yt-paper-button[1]//yt-formatted-string[1]"))
            )
            accept.click()
            time.sleep(2)

            driver.execute_script("window.scrollTo(0,1080)")
            time.sleep(3)

            name = driver.find_element(By.CSS_SELECTOR, "h1[class='title style-scope ytd-video-primary-info-renderer'] yt-formatted-string[class='style-scope ytd-video-primary-info-renderer']")
            channelname = driver.find_element(By.CSS_SELECTOR, "div[id='upload-info'] a[class='yt-simple-endpoint style-scope yt-formatted-string']")
            videoviews = driver.find_element(By.CSS_SELECTOR, ".view-count.style-scope.ytd-video-view-count-renderer")
            videolikes = driver.find_element(By.XPATH, "//ytd-watch-flexy[@role='main']//ytd-toggle-button-renderer[1]//a[1]//yt-formatted-string[1]")
            videocomments = driver.find_element(By.CSS_SELECTOR, "h2[id='count'] span:nth-child(1)")
            
            update.message.reply_text('Bro, ecco le stats del video: \n Canale: ' + channelname.text + "\n Titolo: " + name.text + "\n Visualizzazioni: " + videoviews.text + "\n Likes: " + videolikes.text + "\n Commenti: " + videocomments.text)
        except Exception as e:
            print(e)
            driver.quit()

        time.sleep(5)
        global statsChatSession
        statsChatSession = False
    else: update.message.reply_text('bro, questo non è un video su youtube 🤦‍♂️')

def downloadyoutubevideo(update, context):
    text = str(update.message.text)
    global videoName
    videoPath = "C:\\Users\\CS-9\\Downloads\\"
    if(("www.youtube.com" in text and "watch" in text) or "youtu.be" in text):
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.freemake.com/it/free_video_downloader/")
        try:
            accept = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "linkInput"))
            )
            accept.click()
            accept.send_keys(text)
            time.sleep(2)

            title = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "p[data-bind='text: searchResultViewModel.title']"))
            )     
            
            if('&' in title.text):
                videoName = title.text.split('&')[0]  + ".mp4"
            elif('-' in title.text):
                videoName = title.text + ".mp4"

             

            download = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@data-bind='html: downloadVideoButtonText']"))
            )
            download.click()

            maxWait = 120
            status = True
            while(status and maxWait > 0):
                for root, dirs, files in os.walk("C:\\Users\\CS-9\\Downloads"):
                    if videoName in files:
                        print("videoname: " + videoName)
                        status = False
                        break  
                    else:
                        maxWait - 1
                time.sleep(1)   
            bot.send_chat_action(chat_id=update.message.chat.id, action=telegram.ChatAction.UPLOAD_VIDEO)
            time.sleep(2)
            
            index = 0

            bot.send_chat_action(chat_id=update.message.chat.id, action=telegram.ChatAction.UPLOAD_VIDEO)
            bot.sendVideo(update.message.chat_id, video=open(videoPath + videoName, 'rb'))


        except Exception as e:
            print(e)
            driver.quit()

        os.remove(videoPath + videoName)
        time.sleep(5)
        global statsChatSession
        statsChatSession = False

        
    else: update.message.reply_text('bro, questo non è un video su youtube 🤦‍♂️') 

def mp3Download(update, context):
    text = str(update.message.text)
    global audioName
    audioPath = "C:\\Users\\CS-9\\Downloads\\"
    if(("www.youtube.com" in text and "watch" in text) or "youtu.be" in text):
        driver = webdriver.Chrome(options=options)
        driver.get("https://onlinevideoconverter.pro/it/youtube-converter-mp3")
        try:
            accept = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "texturl"))
            )
            accept.click()
            time.sleep(0.5)
            accept.send_keys(text)
            # accept.send_keys(Keys.TAB)
            # accept.send_keys(Keys.RETURN)
            time.sleep(2)

            start = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "START"))
            ) 
            start.click()
            time.sleep(1)

            title = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "result_title"))
            ) 

            time.sleep(1)
            audioName = title.text + ".mp3"             

            download = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, "DOWNLOAD"))
            )
            download.click()

            maxWait = 120
            status = True
            while(status and maxWait > 0):
                for root, dirs, files in os.walk("C:\\Users\\CS-9\\Downloads"):
                    if audioName in files:
                        print("audioName: " + audioName)
                        status = False
                        break  
                    else:
                        maxWait - 1
                time.sleep(1)   
            
            bot.send_chat_action(chat_id=update.message.chat.id, action=telegram.ChatAction.UPLOAD_AUDIO)
            time.sleep(2)
            
            index = 0

            global mp3DownloadChatSession 
            mp3DownloadChatSession = False

            bot.send_chat_action(chat_id=update.message.chat.id, action=telegram.ChatAction.UPLOAD_AUDIO)
            bot.sendAudio(update.message.chat_id, audio=open(audioPath + audioName, 'rb'))


        except Exception as e:
            print(e)
            driver.quit()

        os.remove(audioPath + audioName)
        time.sleep(5)
        global statsChatSession
        statsChatSession = False

        
    else: update.message.reply_text('bro, questo non è un video su youtube 🤦‍♂️') 

def cancel(update, context):
    global statsChatSession
    global videoDownloadChatSession
    global mp3DownloadChatSession
    mp3DownloadChatSession = False
    videoDownloadChatSession = False
    statsChatSession = False
    update.message.reply_text('ho cancellato tutto, bro 🙅‍♂️')

#def getIdentifier():


def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("cancel", cancel))
    dp.add_handler(CommandHandler("downloadyoutubevideo", getYoutubeLink))
    dp.add_handler(CommandHandler("getyoutubevideostats", getYoutubeLink))
    dp.add_handler(CommandHandler("downloadyoutubemp3", getYoutubeLink))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()



main()