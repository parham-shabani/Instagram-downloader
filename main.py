import telegram
from typing import Final
import json
from telegram import Update, Bot
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests


bot = Bot(token="6635906742:AAE30y2pQOVWP6p0SRAj-KOjNDutAJ-b8ME")
BOT_USERNAME: Final = '@instagram_up_down_bot'


async def insta_scrape(link):
  print("1")
  url = "https://instagram-downloader-download-instagram-videos-stories.p.rapidapi.com/index"

  querystring = {"url": link}

  headers = {
	"X-RapidAPI-Key": "4112085f83msh4cc3fc8b35435ccp152bafjsn095e429b2119",
	"X-RapidAPI-Host": "instagram-downloader-download-instagram-videos-stories.p.rapidapi.com"
  }
  print("2")
  response = requests.get(url, headers=headers, params=querystring)
  print("3")
  print(response.status_code)
  
  print(response.json())
  print("4")
  return response.json()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text('Welcome to our bot my friend')

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
  print(f'Update {update} caused error {context.error}')




async def handle_message(update: Update, context:ContextTypes.DEFAULT_TYPE):
  await bot.send_message(chat_id=update.effective_chat.id, text="Please Wait Your Media loading")

  text: str = update.message.text


  await insta_scrape(text)


if __name__ == '__main__':
  app = Application.builder().token(bot.token).build()
  # Commands
  app.add_handler(CommandHandler('start', start_command))

  # Messages
  app.add_handler(MessageHandler(filters.TEXT, handle_message))

  # Log all errors
  app.add_error_handler(error)

  print('Polling...')
  # Run the bot
  app.run_polling(poll_interval=1)

  