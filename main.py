import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import os
import threading
import requests  # ចាំបាច់សម្រាប់ការហៅ API
from bakong_khqr import KHQR

# 1. ដាក់ Token របស់ Telegram Bot
TOKEN = '8614978833:AAHLO26tvHuxzufMWw6epc_mSPuEnzIoDwA'
bot = telebot.TeleBot(TOKEN)

# 2. ដាក់ Bakong Token របស់អ្នក
BAKONG_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjoiMWUyN2QzM2NiYzNiNDkzNCJ9LCJpYXQiOjE3NzI5NTM5MDcsImV4cCI6MTc4MDcyOTkwN30.lPQ5rXUPyoyA2WCDMTfBFex9prg2MF6VOanKuBbArWU"

# បញ្ជីផលិតផល
PRODUCTS = {
    'noverify': {'name': 'Acc Form No Verify', 'price': 0.01},
    'fullset_no2fa': {'name': 'Full Set No 2FA', 'price': 5.00},
    'fullset': {'name': 'Full Set (មាន 2FA)', 'price': 7.00}
}

user_orders = {}

# --- អនុគមន៍ឆែកស្តុកពី File ---
def get_stock(product_key):
    file_path = f"{product_key}.txt"
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line for line in f if line.strip()]
            return len(lines)
    return 0

# --- អនុគមន៍កាត់ File និងបង្កើត File ថ្មីជូនភ្ញៀវ ---
def extract_account_to_file(product_key, quantity=1):
    source_file = f"{product_key}.txt"
    if not os.path.exists(source_file): return None
    with open(source_file, 'r', encoding='utf-8') as f:
        lines = [line for line in f if line.strip()]
    if len(lines) < quantity: return None
    
    buyer_accounts = lines[:quantity]
    remaining_accounts = lines[quantity:]
    
    with open(source_file, 'w', encoding='utf-8') as f:
        f.writelines(remaining_accounts)
        
    buyer_file_name = f"Your_Order_{product_key}_{int(time.time())}.txt"
    with open(buyer_file_name, 'w', encoding='utf-8') as f:
        f.writelines(buyer_accounts)
        
    return buyer_file_name

# --- មុខងារបង្កើត Menu ---
def get_main_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton(f"🛒 ទិញ {PRODUCTS['noverify']['name']} - ${PRODUCTS['noverify']['price']} (ស្តុក: {get_stock('noverify')})", callback_data="buy_noverify"),
        InlineKeyboardButton(f"🛒 ទិញ {PRODUCTS['fullset_no2fa']['name']} - ${PRODUCTS['fullset_no2fa']['price']} (ស្តុក: {get_stock('fullset_no2fa')})", callback_data="buy_fullset_no2fa"),
        InlineKeyboardButton(f"🛒 ទិញ {PRODUCTS['fullset']['name']} - ${PRODUCTS['fullset']['price']} (ស្តុក: {get_stock('fullset')})", callback_data="buy_fullset")
    )
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "សួស្តី! សូមជ្រើសរើសប្រភេទគណនីដែលអ្នកចង់ទិញខាងក្រោម៖", reply_markup=get_main_menu())

# --- ដំណាក់កាលទី១: ជ្រើសរើសទំនិញ ---
@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_buy_click(call):
    bot.answer_callback_query(call.id) 
    chat_id = call.message.chat.id
    product_key = call.data.replace('buy_', '')
    product = PRODUCTS.get(product_key)
    stock = get_stock(product_key)
    
    if product and stock > 0:
        user_orders[chat_id] = {'product_key': product_key}
        bot.delete_message(chat_id, call.message.message_id)
        msg = bot.send_message(chat_id, f"📝 អ្នកបានជ្រើសរើស **{product['name']}**។\n👉 សូមវាយបញ្ចូល **ចំនួន** ដែលអ្នកចង់ទិញ (ស្តុកសរុប: {stock} គណនី)៖", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_quantity)
    else:
        bot.send_message(chat_id, "❌ សុំទោស គណនីនេះអស់ពីស្តុកហើយ។")

# --- ដំណាក់កាលទី២: វាយបញ្ចូលចំនួន ---
def process_quantity(message):
    chat_id = message.chat.id
    if chat_id not in user_orders: return
    product_key = user_orders[chat_id]['product_key']
    stock = get_stock(product_key)
    
    try:
        qty = int(message.text.strip())
        if qty <= 0:
            msg = bot.send_message(chat_id, "❌ ចំនួនត្រូវតែធំជាង **០**។ សូមវាយបញ្ចូលម្តងទៀត៖", parse_mode="Markdown")
            bot.register_next_step_handler(msg, process_quantity)
            return
        if qty > stock:
            msg = bot.send_message(chat_id, f"❌ ស្តុកមិនគ្រប់គ្រាន់ទេ! (មានត្រឹមតែ {stock} ប៉ុណ្ណោះ)។ សូមវាយបញ្ចូលម្តងទៀត៖", parse_mode="Markdown")
            bot.register_next_step_handler(msg, process_quantity)
            return
        
        product = PRODUCTS[product_key]
        total_price = qty * product['price']
        user_orders[chat_id]['qty'] = qty
        user_orders[chat_id]['total_price'] = total_price
        
        text = (f"🛍 **ការបញ្ជាទិញ**\n📌 ប្រភេទ៖ **{product['name']}**\n🔢 ចំនួន៖ **{qty} គណនី**\n💵 សរុប៖ **${total_price:,.2f}**\n\nតើអ្នកចង់បន្តឬទេ?")
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("✅ យល់ព្រមទិញ", callback_data="confirm_order"), 
            InlineKeyboardButton("❌ បោះបង់", callback_data="cancel_order")
        )
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")
    except ValueError:
        msg = bot.send_message(chat_id, "❌ សូមវាយបញ្ចូលជា **លេខ**។ សូមព្យាយាមម្តងទៀត៖", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_quantity)

# --- មុខងារបាញ់ API ទៅ Bakong (ចម្លងពី PaymentWorker) ---
def check_payment_status(p_hash):
    url = "https://api-bakong.nbc.gov.kh/v1/check_transaction_by_md5" 
    headers = {
        "Authorization": f"Bearer {BAKONG_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"md5": p_hash} 
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        # បងអាចបើកកូដ Print នេះវិញបាន បើចង់ឃើញ Log ពេលបាញ់ API
        # print(f"[Bakong API Response Code]: {response.status_code}")
        # print(f"[Bakong API Data]: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            
            res_code = data.get("responseCode")
            if res_code == 0 or res_code == "0":
                return True
                
            if isinstance(data.get("data"), dict):
                if data["data"].get("status") == "SUCCESS":
                    return True
    except Exception as e:
        print(f"Check Payment Error: {e}")
        
    return False

# --- Worker សម្រាប់រង់ចាំឆែកការបង់ប្រាក់ពីក្រោយ ---
def auto_payment_worker(chat_id, message_id, p_hash, product_key, qty):
    timeout = 300 # រង់ចាំ ៥ នាទី (៣០០ វិនាទី)
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        
        # ហៅ Function API ខាងលើមកឆែកមើល
        is_success = check_payment_status(p_hash)
        
        if is_success:
            # លុបរូប QR ចេញ
            try: bot.delete_message(chat_id, message_id)
            except: pass
            
            bot.send_message(chat_id, "✅ **ការបង់ប្រាក់ទទួលបានជោគជ័យ!** កំពុងរៀបចំទិន្នន័យជូនលោកអ្នក...", parse_mode="Markdown")
            
            # កាត់ File និងផ្ញើជូនភ្ញៀវ
            buyer_file = extract_account_to_file(product_key, quantity=qty)
            if buyer_file and os.path.exists(buyer_file):
                with open(buyer_file, 'rb') as doc:
                    bot.send_document(chat_id, doc, caption=f"🎉 អរគុណសម្រាប់ការជាវ! នេះគឺជាឯកសារដែលមាន **{qty} គណនី** របស់អ្នក។ 🔒")
                os.remove(buyer_file)
            else:
                bot.send_message(chat_id, "❌ សុំទោស មានបញ្ហាក្នុងការទាញយក Account។ សូមទាក់ទង Admin។")
            
            if chat_id in user_orders: del user_orders[chat_id]
            return # បញ្ចប់ការងាររបស់ Worker
            
        time.sleep(5) # រង់ចាំ ៥ វិនាទីរួចឆែកម្តងទៀត
        
    # បើផុត ៥ នាទីហើយ គ្មានលុយចូល
    try:
        bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption="❌ វិក្កយបត្រនេះបានផុតកំណត់ (អស់ពេល ៥នាទី)។ ប្រសិនបើអ្នកនៅតែចង់ទិញ សូមធ្វើការកុម្ម៉ង់ម្តងទៀត។")
        if chat_id in user_orders: del user_orders[chat_id]
    except:
        pass

# --- ដំណាក់កាលទី៣: បង្កើត QR & Generate MD5 ---
@bot.callback_query_handler(func=lambda call: call.data in ['confirm_order', 'cancel_order'])
def handle_checkout(call):
    bot.answer_callback_query(call.id)
    chat_id = call.message.chat.id
    
    if call.data == 'cancel_order':
        if chat_id in user_orders: del user_orders[chat_id] 
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="🚫 ការបញ្ជាទិញត្រូវបានបោះបង់។", reply_markup=get_main_menu())
        return

    order = user_orders.get(chat_id)
    if not order: return
        
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="🔄 កំពុងបង្កើតកូដ KHQR...")
    
    try:
        khqr_tool = KHQR(BAKONG_TOKEN)
        
        qr_string = khqr_tool.create_qr(
            bank_account="ngim_bunrith1@bkrt",
            merchant_name="BUNRITH NGIM",
            merchant_city="Phnom Penh",
            amount=float(order['total_price']),
            currency="USD",
            store_label="Digital Accounts",
            phone_number="855974249441",
            bill_number=f"INV{int(time.time())}",
            terminal_label="BotAutoShop",
            static=False
        )
        
        # បង្កើត MD5 Hash (p_hash)
        p_hash = khqr_tool.generate_md5(qr_string)
        
        img_path = khqr_tool.qr_image(qr_string)

        if img_path and os.path.exists(img_path):
            with open(img_path, 'rb') as photo:
                bot.delete_message(chat_id, call.message.message_id)
                
                msg = bot.send_photo(
                    chat_id, 
                    photo, 
                    caption=f"💸 ត្រូវទូទាត់សរុប៖ **${order['total_price']:,.2f}**\n\n🔔 ប្រព័ន្ធកំពុងរង់ចាំការស្កេនបង់ប្រាក់របស់អ្នកដោយស្វ័យប្រវត្តិ (មានសុពលភាព ៥ នាទី)... ⏳",
                    parse_mode="Markdown"
                )
                
            os.remove(img_path)
            
            # ចាប់ផ្ដើម Thread ឆែកមើលស្ថានភាពបង់ប្រាក់
            threading.Thread(
                target=auto_payment_worker, 
                args=(chat_id, msg.message_id, p_hash, order['product_key'], order['qty']),
                daemon=True
            ).start()
            
    except Exception as e:
        bot.send_message(chat_id, f"❌ បញ្ហាបង្កើត QR: {str(e)}")

print("Bot លក់គណនី Auto-Pay កំពុងដំណើរការ...")
bot.polling(none_stop=True)
