import telegram
from typing import Final
import os
import json
from telegram import Update, Bot
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

bot = Bot(token="6635906742:AAE30y2pQOVWP6p0SRAj-KOjNDutAJ-b8ME")
BOT_USERNAME: Final = '@instagram_up_down_bot'


async def insta_scrape(link) -> dict:
  print("1")
  url = "https://instagram-downloader-download-instagram-videos-stories.p.rapidapi.com/index"

  querystring = {"url": link}

  headers = {
    "X-RapidAPI-Key":
    "4f9eef7b62mshc232b27bba34a7ep1a12efjsn26541b47f4d8",
    "X-RapidAPI-Host":
    "instagram-downloader-download-instagram-videos-stories.p.rapidapi.com"
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


async def download_media(url, save_path):
  response = requests.get(url)
  if response.status_code == 200:
    with open(save_path, 'wb') as file:
      file.write(response.content)


async def send_media(bot_token, chat_id, file_path, caption=None):
  bot = Bot(token=bot_token)
  if file_path.endswith(('.jpg', '.jpeg', '.png')):
    await bot.send_photo(chat_id=chat_id,
                         photo=open(file_path, 'rb'),
                         caption=caption)

  elif file_path.endswith(('.mp4', '.avi', '.mov')):
    await bot.send_video(chat_id=chat_id,
                         video=open(file_path, 'rb'),
                         caption=caption)

  else:
    await bot.send_document(chat_id=chat_id,
                            document=open(file_path, 'rb'),
                            caption=caption)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  # Check if the message is from a private chat
  if update.effective_chat.type == 'private':
    await bot.send_message(chat_id=update.effective_chat.id,
                           text="Please Wait Your Media loading")
    text: str = update.message.text

    #get instagram post contents
    result = await insta_scrape(text)
    post_caption = ""

  if "story_by_id" in result:
    if result["story_by_id"]["Type"] == 'Story-Image':
      media = result["story_by_id"]["media"]
      save_path = 'media.jpg'

    if result["story_by_id"]["Type"] == 'Story-Video':
      media = result["story_by_id"]["media"]
      save_path = 'media.mp4'

  else:
    media = None
    if result["Type"] == 1 and result["Type"] == 'Post-Image':
      post_caption = result["title"]
      media = result["media"]
      save_path = 'media.jpg'

    elif result["Type"] == 'Post-Video':
      post_caption = result["title"]
      media = result["media"]
      save_path = 'media.mp4'

  bot_token = "6635906742:AAE30y2pQOVWP6p0SRAj-KOjNDutAJ-b8ME"
  chat_id = "@chaagh"

  if media is not None:
    # Download and send the media
    await download_media(media, save_path)
    await send_media(bot_token,
                     chat_id,
                     save_path,
                     caption=post_caption + "\n@Chaagh")


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
