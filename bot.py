import config
import logging
from aiogram import Bot, Dispatcher, executor, types

# Log level
logging.BasicConfig(level=logging.INFO)

# Bot init
bot = Bot(token = config.TOKEN)
dp = Dispatcher(bot)

# Start and help
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
  await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

# Echo
@dp.message_handler()
async def echo(message: types.Message):
  await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
