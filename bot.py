import telebot
import json
import os

BOT_TOKEN = "8985562775:AAGg7OTDdo5vfgJ65x70fJvki7Qe-v9y_nI"
ADMIN_ID = 7699675601
LOG_CHANNEL = -1003857107976

bot = telebot.TeleBot(BOT_TOKEN)

# Foydalanuvchilar faylda saqlanadi
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

users = load_users()
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.chat.id)
    name = message.from_user.first_name or "User"
    
    if uid not in users:
        users[uid] = {"name": name}
        save_users(users)
        bot.send_message(LOG_CHANNEL, f"🆕 Yangi foydalanuvchi: {name} | ID: {uid}")
    
    user_data[uid] = {}
    bot.send_message(message.chat.id,
        f"Hello! I help you get a freight quote 🚗\n\nWhere are you shipping FROM? (City, State)")

@bot.message_handler(commands=['admin'])
def admin(message):
    if message.chat.id != ADMIN_ID:
        return
    total = len(users)
    names = "\n".join([f"• {v['name']} (ID: {k})" for k, v in list(users.items())[-10:]])
    bot.send_message(ADMIN_ID, f"📊 Admin Panel\n\n👥 Jami foydalanuvchilar: {total}\n\n🕐 So'nggi 10 ta:\n{names}")

@bot.message_handler(func=lambda m: True)
def handle(message):
    uid = str(message.chat.id)
    name = message.from_user.first_name or "User"
    
    # Logs kanalga yuborish
    bot.send_message(LOG_CHANNEL, f"💬 {name} (ID: {uid}):\n{message.text}")
    
    data = user_data.get(uid, {})

    if 'from' not in data:
        data['from'] = message.text
        user_data[uid] = data
        bot.send_message(uid, "Where are you shipping TO? (City, State)")

    elif 'to' not in data:
        data['to'] = message.text
        user_data[uid] = data
        bot.send_message(uid, "What type of vehicle?")

    elif 'cargo' not in data:
        data['cargo'] = message.text
        user_data[uid] = data
        bot.send_message(uid, "Your phone number?")

    elif 'phone' not in data:
        data['phone'] = message.text
        user_data[uid] = data
        bot.send_message(uid, "Your email?")

    elif 'email' not in data:
        data['email'] = message.text
        user_data[uid] = data

        lead = f"""
🚗 NEW VEHICLE SHIPPING LEAD
From: {data['from']}
To: {data['to']}
Vehicle: {data['cargo']}
Phone: {data['phone']}
Email: {data['email']}
"""
        bot.send_message(ADMIN_ID, lead)
        bot.send_message(LOG_CHANNEL, lead)
        bot.send_message(uid, "Thank you! We will contact you shortly ✅")
        user_data[uid] = {}

bot.infinity_polling()
