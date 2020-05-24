import html
import time
import datetime
from telegram.ext import CommandHandler, run_async, Filters
import requests, logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import Message, Chat, Update, Bot, MessageEntity
from haruka import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, WHITELIST_USERS
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from haruka.modules.helper_funcs.chat_status import user_admin

count = 0
@run_async
def video(bot: Bot, update: Update, args):
	message = update.effective_message
	global count

	chatId = update.message.chat_id
    
	video_id = ''.join(args)

	if video_id.find('youtu.be') != -1:
		index = video_id.rfind('/') + 1
		video_id = video_id[index:][:11]
		message.reply_text("Please wait...\nDownloading video.")

	elif video_id.find('youtube') != -1:
		index = video_id.rfind('?v=') + 3
		video_id = video_id[index:][:11]
		message.reply_text("Please wait...\Downloading video.")

	elif not video_id.find('youtube') != -1:
		message.reply_text("Please provide me youtube link")

	elif not video_id.find('youtu.be') != -1:
		message.reply_text("Please provide me youtube link")
		

        



	r = requests.get(f'https://api.pointmp3.com/dl/{video_id}?format=mp4')
	

	json1_response = r.json()

	if not json1_response['error']:
		

		redirect_link = json1_response['url']

		r = requests.get(redirect_link)
		

		json2_response = r.json()

		if not json2_response['error']:
			payload = json2_response['payload']

			info = '*{0}* \n\n*Uploaded by @AlexaFamilyBot*'.format(payload['fulltitle'])

			try:
				
				bot.send_video(chat_id=chatId, video=json2_response['url'], parse_mode='Markdown', caption=info)
				count += 1
		
			except:
			     return

__help__ = """ 
How to use ?

First search your video with /yt command and then copy the video link and use the command below 👇 

 - /video <the youtube link> : Extract,Download and upload audio from a youtube video link 
"""
__mod_name__ = "Video Download" 

music_handler = CommandHandler('video', video, pass_args=True)
dispatcher.add_handler(music_handler)
