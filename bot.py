import telebot

BOT_TOKEN = "8985562775:AAGg7OTDdo5vfgj65x70fJvki7Qe-v9y_nI"
ADMIN_ID = "7699675601"

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, 
        "Hello! I help you get a freight quote 🚛\n\nWhere are you shipping FROM? (City, State)")

@bot.message_handler(func=lambda m: True)
def handle(message):
    uid = message.chat.id
    data = user_data.get(uid, {})
    
    if 'from' not in data:
        data['from'] = message.text
        user_data[uid] = data
        bot.send_message(uid, "Where are you shipping TO? (City, State)")
    
    elif 'to' not in data:
        data['to'] = message.text
        user_data[uid] = data
        bot.send_message(uid, "What type of cargo? (e.g. dry van, flatbed, reefer)")
    
    elif 'cargo' not in data:
        data['cargo'] = message.text
        user_data[uid] = data
        bot.send_message(uid, "Weight? (lbs)")
    
    elif 'weight' not in data:
        data['weight'] = message.text
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
🚛 NEW FREIGHT LEAD!
From: {data['from']}
To: {data['to']}
Cargo: {data['cargo']}
Weight: {data['weight']}
Phone: {data['phone']}
Email: {data['email']}
        """
        
        bot.send_message(ADMIN_ID, lead)
        bot.send_message(uid, "Thank you! We will contact you shortly ✅")
        user_data[uid] = {}

bot.polling()