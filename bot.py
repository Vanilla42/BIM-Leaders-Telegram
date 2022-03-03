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
 
def main():
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    
    # Run long-polling
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()
