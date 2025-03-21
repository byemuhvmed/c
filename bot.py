import telebot
import random
import requests
import time
from telebot import types

TOKEN = "7263198575:AAFTDaY3qWUWbqL90WE2ywL0a3LVR3lbX48"
your_chat_id = 6463481188  # استبدل هذا بمعرف دردشتك الخاص
send_cc = -1002167005803  # معرف القناة

stickers = [
    '✨', '🔥', '🎉', '⚡️',  '🌨', '🌩', '💫', '💵', '💸',
]

kk = [
    'Scrape CC', 'New CC', 'CC Damp',
]

bot = telebot.TeleBot(TOKEN)

def get_bin_info(bin_number):
    api_url = f"https://bins.antipublic.cc/bins/{bin_number}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error fetching bin info: {e}")
        return None

def format_bin_info(bin_data, full_cc):
    cc_parts = full_cc.split("|")
    cc_number = cc_parts[0]
    cc_month = cc_parts[1] if len(cc_parts) > 1 else ""
    cc_year = cc_parts[2] if len(cc_parts) > 2 else ""
    cc_cvv = cc_parts[3] if len(cc_parts) > 3 else ""
    sticker = random.choice(stickers)
    random_kk = random.choice(kk)

    formatted_info = f"""
 ｢#bin{bin_data.get('bin', '')[:6]} 」
┏━━⚇
┃<b>{random_kk}  {sticker}  </b>
┗━━━━━━━━⊛
<b>✺ Card:</b><code> {full_cc}</code>
<b>✺ Extrap:</b> <code>/gen {cc_number[:12]}xxxx|{cc_month}|{cc_year}|xxx</code>
<b>✺ Info:</b> {bin_data.get('brand', '')} - {bin_data.get('type', '')}
<b>✺ Issuer:</b> {bin_data.get('bank', '')}
<b>✺ Country:</b> {bin_data.get('country_name', '')} - {bin_data.get('country_flag', '')}
    """
    return formatted_info

def send_file_lines_to_channel(cc_file):
    with open(cc_file, "r") as file:
        lines = file.readlines()
    
    total_to_send = len(lines)
    for index, line in enumerate(lines):
        full_cc = line.strip()
        bin_info = get_bin_info(full_cc[:6])
        
        if bin_info:
            formatted_info = format_bin_info(bin_info, full_cc)
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn_right = types.InlineKeyboardButton(text="Join", url="https://t.me/+dAdU3nQ8TycyYTg8")
            btn_left = types.InlineKeyboardButton(text="Admin", url="https://t.me/The_Bigboos")
            markup.add(btn_right, btn_left)
            
            # إرسال المعلومات إلى القناة
            bot.send_message(send_cc, formatted_info, parse_mode="HTML", reply_markup=markup)
            time.sleep(10)
            print(full_cc)
        else:
            print(f"Error fetching bin info for {full_cc}")

        # إبلاغ المستخدم بعدد العناصر المتبقية
        remaining = total_to_send - (index + 1)
        bot.send_message(your_chat_id, f"تم إرسال {index + 1} فيزا من {total_to_send} المتبقي {remaining}")

    # إبلاغ المستخدم عند الانتهاء
    bot.send_message(your_chat_id, "خلصت ياعم هاتلي كومبو كمان😂🔥")

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "ابعت الفيزات يا كينج🔥")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open("received_file.txt", "wb") as new_file:
        new_file.write(downloaded_file)

    total_lines = len(downloaded_file.splitlines())
    bot.send_message(your_chat_id, f"تم استلام {total_lines} فيزا🔥")
    send_file_lines_to_channel("received_file.txt")

def recibir_msg():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    recibir_msg()
