import config
import logging
from aiogram import Bot, Dispatcher, executor, types

# Log level
logging.BasicConfig(level=logging.INFO)

# Bot init
bot = Bot(token = config.TOKEN)
dp = Dispatcher(bot)

# Echo
@dp.message_handler()
async def echo(message: types.Message):
  await message.answer(message.text)
 
# Run long-polling
if __name__ == "__main__":
  executor.start_polling(dp, skip_updates=True)
