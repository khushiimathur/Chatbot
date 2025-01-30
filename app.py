import telethon.sync as ts 
from telethon.sessions import StringSession
from pymongo import MongoClient
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import google.generativeai as genai
import os
import PIL.Image


# Read environment variables (set these in Render's dashboard or .env file)
api_id = #secret
api_hash = #secret
bot_token = #secret
bot = ts.TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

gemini_api_key = #secret
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
model2 = genai.GenerativeModel("gemini-1.5-pro")

mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['records']
users = db['users']
chat_history_collection = db['chat_history']
files_collection = db['files']
search_flag = False
flag = False

def query_gemini_api(question):
    response = model.generate_content(question)
    return (response.text)

def describe_file(file_path):
    file = PIL.Image.open(file_path)
    prompt = "Caption this image."
    response = model2.generate_content([prompt, file])
    return response.text

def perform_web_search(query):
    # Perform the web search using Gemini API
    response = model.generate_content({"text": f"Search the web for: {query} and give me a summary of top results"})
    return response.text

def search_web(query) #working on it

# Handle /start command
@bot.on(ts.events.NewMessage(pattern='/start'))
async def start(event):
    sender = await event.get_sender()
    user = {
        'first_name': sender.first_name,
        'username': sender.username,
        'chat_id': event.chat_id
    }
    users.insert_one(user)
    await event.respond('Welcome! Please share your contact number.', buttons=[
        [ts.Button.request_phone('Share Phone Number')]
    ])

# Handle contact sharing
@bot.on(ts.events.NewMessage)
async def handle_contact(event):
    if event.contact:
        contact = event.contact
        user = users.find_one({'chat_id': event.chat_id})
        if user:
            users.update_one(
                {'chat_id': event.chat_id},
                {'$set': {'phone_number': contact.phone_number}}
            )
            await event.respond('Thank you for sharing your phone number!')
    
    elif event.photo or event.document:
        file = await event.download_media()
        description = describe_file(file)
        
        # Save file metadata in MongoDB
        file_metadata = {
            'filename': os.path.basename(file),
            'description': description,
            'timestamp': datetime.utcnow()
        }
        files_collection.insert_one(file_metadata)
        
        await event.respond(f"File received and described: {description}")

@bot.on(ts.events.NewMessage())
async def handleMessage(event):
    global flag, search_flag
    if event.message.message and event.message.message[0] == '/':
        command = event.message.message[1:]
        if (command == 'query'):
            response = "Please enter your prompt"
            flag = True
            await event.respond(response)
        elif command == 'websearch':
            response = "Please enter your web search query"
            search_flag = True
            await event.respond(response)
    
    elif flag == True and event.message.message:
        flag = False
        response = query_gemini_api(event.message.message)
        # Save chat history
        chat_entry = {
            'chat_id': event.chat_id,
            'user_query': event.message.message,
            'bot_response': response,
            'timestamp': datetime.utcnow()
        }
        chat_history_collection.insert_one(chat_entry)
        await event.respond(response)
    
    elif search_flag==True and event.message.message:
        search_flag = False
        search_query = event.message.message
        search_results = perform_web_search(search_query)
        await event.respond(search_results)
        search_flag = False
# Start the bot and keep it running
print('Bot is running...')
bot.run_until_disconnected()
