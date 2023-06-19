import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.exception import AppwriteException
from appwrite.id import ID

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
client = Client()
(client
    .set_endpoint('https://api.thenine.co/v1') # Your API Endpoint
    .set_project('648ffac98ff185140eb8')  # Your project ID
    .set_key('52b2370511f3ec0d3d17040dd5d8ed62b9f22f47f12b51b51f4a6c92c6229e6ff39ff440cad06a66adc0d49c0eea171401c28551ae8da20996935d43d4c95c3b280e6a60a1a0689c9900f21c629934df0402999ef3a6751778ede53d897159752437685e2dc54400ac4b05c57d54120e9c357a2858a80e6585a8250bda009cd4') # Your secret API key
    )
users = Users(client)

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    tg_user = update.effective_user
    
    try:
        # Try to retrieve the user from Appwrite
        appwrite_user = users.get(str(tg_user.id))
        message = f"Welcome back {appwrite_user['name']}! Your ID is {tg_user.id}. Your Appwrite user ID is {appwrite_user['$id']}. How can I assist you?"
    except AppwriteException as e:
        # If user doesn't exist in Appwrite, create a new user
        if e.response['code'] == 404: # Assuming the code for user not found is 404
            try:
                user = users.create(
                    user_id=str(tg_user.id),
                    email=None,
                    phone=None,
                    password=None,
                    name=tg_user.first_name
                )
                logging.info(f"Created Appwrite user with id {user['$id']}")
                message = f"Hello {tg_user.first_name}! Your ID is {tg_user.id}. Your Appwrite user ID is {user['$id']}. Welcome to the Telegram Bot. How can I assist you?"
            except AppwriteException as create_ex:
                print(f"Exception occurred: {create_ex.message}")
                print(f"Response: {create_ex.response}")
                logging.error(f"Failed to create Appwrite user: {create_ex}")
                message = "Sorry, there was an error creating your Appwrite user."
        else:
            print(f"Exception occurred: {e.message}")
            print(f"Response: {e.response}")
            logging.error(f"Failed to handle Appwrite user: {e}")
            message = "Sorry, there was an error handling your Appwrite user."
    
    await context.bot.send_message(chat_id=chat_id, text=message)

# Function to handle unknown commands
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message = "Sorry, I didn't understand that command."
    await context.bot.send_message(chat_id=chat_id, text=message)

async def getMyData(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    tg_user = update.effective_user

    try:
        appwrite_user = users.get(str(tg_user.id))
        # Try to retrieve the user from Appwrite
        appwrite_user = users.get(str(tg_user.id))
        message = f"Welcome back {appwrite_user['name']}! Your ID is {tg_user.id}. Your Appwrite user ID is {appwrite_user['$id']}. How can I assist you?"
    except AppwriteException as e:
        # If user doesn't exist in Appwrite, create a new user
        if e.response['code'] == 404:
            message = f"User do not exist"
    await context.bot.send_message(chat_id=chat_id, text=message)

# Main function to start the bot
def main():
    application = ApplicationBuilder().token('6047772823:AAE_kuR1q1-OuJKpi4yEd9NbMv-5zLip6vk').build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    mydata_handler = CommandHandler('data', getMyData)
    application.add_handler(mydata_handler)
    
    application.run_polling()



if __name__ == '__main__':
    main()