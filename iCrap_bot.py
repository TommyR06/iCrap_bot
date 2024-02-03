import logging
import os
import csv
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

from config import *
# from config_dummy import *

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# custom filter for poo emoji
class PooEmojiFilter(filters.MessageFilter):
    def filter(self, message):
        check_if_poo = (message.text == u'\U0001F4A9')
        # print(check_if_poo)
        return  check_if_poo
# initialize the class
poo_emoji_filter = PooEmojiFilter()

# custom filter for allowing interaction only with selected group
class GroupFilter(filters.MessageFilter):
    def filter(self, message):
        check_if_group_ok = (message.chat_id == int(GROUP_CHAT_ID))
        # print(check_if_group_ok)
        return  check_if_group_ok
# initialize the class
group_filter = GroupFilter()


async def new_poo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async def add_entry(user_info, date):
        # for future, handle situation if user has no username!
        user = user_info.username
        fields=[user,date]
        with open(f'{REPORT_FOLDER}/iCrap_report.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)

    await add_entry(update.message.from_user, update.message.date)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    

    os.makedirs(REPORT_FOLDER, exist_ok=True)
    new_poo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND) & poo_emoji_filter & group_filter, new_poo)

    application.add_handler(new_poo_handler)
    
    application.run_polling()