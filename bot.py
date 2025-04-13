import telebot
from datetime import datetime
from flask import Flask, request
import os

# Lấy token từ biến môi trường
TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

name_bot = "HancontamBot"

# Dictionary để lưu trữ thông tin tạm thời của người dùng
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f'''
Chào mừng bạn đến với {name_bot}! 🤖

Tôi hỗ trợ nhập thông tin khách hàng và tạo template chuẩn hóa:
- /input: Nhập thông tin khách hàng từng bước và nhận template theo mẫu.

Hãy dùng /input để bắt đầu!
    ''')

@bot.message_handler(commands=['input'])
def input_start(message):
    user_data[message.chat.id] = {}
    bot.reply_to(message, "Hãy nhập TÊN KHÁCH:")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_data[message.chat.id]['name'] = message.text.strip()
    bot.reply_to(message, "Hãy nhập MÃ SỐ:")
    bot.register_next_step_handler(message, get_code)

def get_code(message):
    user_data[message.chat.id]['code'] = message.text.strip()
    bot.reply_to(message, "Hãy nhập DỊCH VỤ:")
    bot.register_next_step_handler(message, get_service)

def get_service(message):
    user_data[message.chat.id]['service'] = message.text.strip()
    bot.reply_to(message, "Hãy nhập DỊCH VỤ + GIÁ DỊCH VỤ:")
    bot.register_next_step_handler(message, get_service_price)

def get_service_price(message):
    user_data[message.chat.id]['service_price'] = message.text.strip()
    bot.reply_to(message, "Hãy nhập TÌNH TRẠNG:")
    bot.register_next_step_handler(message, get_consult)

def get_consult(message):
    user_data[message.chat.id]['consult'] = message.text.strip()
    bot.reply_to(message, "Hãy nhập QUY TRÌNH TH (Định lượng: ml):")
    bot.register_next_step_handler(message, get_status)

def get_status(message):
    user_data[message.chat.id]['status'] = message.text.strip()
    bot.reply_to(message, "Hãy nhập CẢM NHẬN KH:")
    bot.register_next_step_handler(message, get_feel)

def get_feel(message):
    user_data[message.chat.id]['feel'] = message.text.strip()
    bot.reply_to(message, "Hãy nhập Ý KIẾN ĐÓNG GÓP:")
    bot.register_next_step_handler(message, get_feedback)

def get_feedback(message):
    user_data[message.chat.id]['feedback'] = message.text.strip()
    bot.reply_to(message, "Hãy nhập DẶN KHÁCH:")
    bot.register_next_step_handler(message, get_note)

def get_note(message):
    user_data[message.chat.id]['note'] = message.text.strip()
    bot.reply_to(message, "Hãy nhập THÂM NIÊN:")
    bot.register_next_step_handler(message, get_since)

def get_since(message):
    user_data[message.chat.id]['since'] = message.text.strip()
    bot.reply_to(message, "Hãy nhập KTV + TOUR:")
    bot.register_next_step_handler(message, get_ktv)

def get_ktv(message):
    user_data[message.chat.id]['ktv'] = message.text.strip()
    
    # Chuẩn hóa dữ liệu và tạo template
    data = user_data[message.chat.id]
    date = datetime.now().strftime("%d/%m/%Y")
    
    # Chuẩn hóa: Viết hoa chữ cái đầu của các trường
    name = data['name'].title()
    code = data['code'].upper()
    service = data['service'].capitalize()
    service_price = data['service_price'].capitalize()
    consult = data['consult'].capitalize()
    status = data['status'].capitalize()
    feel = data['feel'].capitalize()
    feedback = data['feedback'].capitalize()
    note = data['note'].capitalize()
    since = data['since'].capitalize()
    ktv = data['ktv'].capitalize()

    # Tạo template
    template = f'''
{date}
1. TÊN KHÁCH : {name}
2. MÃ SỐ: {code}
3. DỊCH VỤ: {service}
4. DỊCH VỤ+ GIÁ DỊCH VỤ: {service_price}
5. TÌNH TRẠNG: {consult}
6. QUY TRÌNH TH (Định lượng: ml): {status}
7. CẢM NHẬN KH: {feel}
8. Ý KIẾN ĐÓNG GÓP: {feedback}
9. DẶN KHÁCH: {note}
10. THÂM NIÊN: {since}
11. KTV + TOUR: {ktv}
    '''
    
    bot.reply_to(message, template)
    
    # Xóa dữ liệu tạm sau khi hoàn thành
    del user_data[message.chat.id]

# Webhook endpoint
@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route('/')
def webhook():
    bot.delete_webhook()
    bot.set_webhook(url=f'https://{os.environ.get("RENDER_EXTERNAL_HOSTNAME")}/{TOKEN}')
    return "Bot is running!", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))