import config
import logging
from aiogram import Bot, Dispatcher, executor, types

# Log
logging.BasicConfig(level=logging.INFO)

# Handlers
async def start(message: types.Message):
  await message.reply("Hello, {0}".format(message.from_user.first_name))
#@dp.message_handler()
async def echo(message: types.Message):
  await message.answer(message.text)

# Lambda functions
async def register_handlers(dp: Dispatcher):
  dp.register_message_handler(start, commands=["start"])
  dp.register_message_handler(echo)

async def process_event(update, dp:Dispatcher):
  Bot.set_current(dp.bot)
  await dp.process_update(update)

# Serverless entry point
async def main(**kwargs):
  bot = Bot(token = "5249729175:AAHfTrJdQhdokgTUAIxPsAlRkEUlxmVUnAk")
  dp = Dispatcher(bot)
  
  await register_handlers(dp)
  
  update = types.Update.to_object(kwargs)
  await process_event(update, dp)
  
  return "Ok"

# Bot init
#bot = Bot(token = config.TOKEN)
#dp = Dispatcher(bot)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
