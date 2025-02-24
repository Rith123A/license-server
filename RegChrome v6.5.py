import sys
import time
import random
import threading
import logging
import json
import os
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QFormLayout,
    QMessageBox, QComboBox, QCheckBox, QGroupBox, QFileDialog, QTextEdit, QDialog, QTableWidget, QTableWidgetItem, QHeaderView,
)

from PyQt5.QtGui import QIcon, QFont 
from PyQt5.QtCore import Qt, QTimer, QUrl, QPropertyAnimation, QPointF, QEasingCurve
from PyQt5.QtGui import QDesktopServices
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import imaplib
import email
from email.header import decode_header
import re
import traceback
import subprocess

# Constants
CONFIG_FILE = "https://raw.githubusercontent.com/Rith123A/license-server/main/licenses.json"
CHECKPOINT_FILE = "checkpoint.txt"
ACCOUNT_FILE = "Account Novery.txt"
CHROME_DRIVER_PATH = "chromedriver.exe"


# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Global list to store all running WebDriver instances
running_drivers = []
running_drivers_lock = threading.Lock()

def generate_us_phone_number():
    area_codes = [
                        # Alabama
                        205, 251, 256, 334, 938,

                        # Alaska
                        907,

                        # Arizona
                        480, 520, 623, 928,

                        # Arkansas
                        479, 501, 870,

                        # California
                        209, 213, 310, 323, 408, 415, 424, 442, 510, 530, 559, 562, 619, 626, 628, 650, 657, 661, 669, 707, 714, 747, 760, 805, 818, 820, 831, 858, 909, 916, 925, 949, 951,

                        # Colorado
                        303, 719, 720, 970,

                        # Connecticut
                        203, 475, 860, 959,

                        # Delaware
                        302,

                        # District of Columbia (Washington, D.C.)
                        202,

                        # Florida
                        239, 305, 321, 352, 386, 407, 561, 727, 754, 772, 786, 813, 850, 863, 904, 941, 954,

                        # Georgia
                        229, 404, 470, 478, 678, 706, 762, 770, 912,

                        # Hawaii
                        808,

                        # Idaho
                        208, 986,

                        # Illinois
                        217, 224, 309, 312, 331, 618, 630, 708, 773, 779, 815, 847, 872,

                        # Indiana
                        219, 260, 317, 463, 574, 765, 812, 930,

                        # Iowa
                        319, 515, 563, 641, 712,

                        # Kansas
                        316, 620, 785, 913,

                        # Kentucky
                        270, 364, 502, 859,

                        # Louisiana
                        225, 318, 337, 504, 985,

                        # Maine
                        207,

                        # Maryland
                        240, 301, 410, 443, 667,

                        # Massachusetts
                        339, 351, 413, 508, 617, 774, 781, 857, 978,

                        # Michigan
                        231, 248, 269, 313, 517, 586, 616, 734, 810, 906, 947, 989,

                        # Minnesota
                        218, 320, 507, 612, 651, 763, 952,

                        # Mississippi
                        228, 662, 769,

                        # Missouri
                        314, 417, 573, 636, 660, 816, 975,

                        # Montana
                        406,

                        # Nebraska
                        308, 402, 531,

                        # Nevada
                        702, 725, 775,

                    

                        # New Jersey
                        201, 551, 640, 732, 848, 856, 862, 908, 973,

                        # New Mexico
                        505, 575,

                        # New York
                        212, 315, 332, 347, 516, 518, 585,  631, 646, 680, 716, 718, 838, 845, 914, 917, 929, 934,

                        # North Carolina
                        252, 336, 704, 743, 828, 910, 919, 980, 984,

                        # North Dakota
                        701,

                        # Ohio
                        216, 220, 234, 330, 380, 419, 440, 513, 567, 614, 740, 937,

                        # Oklahoma
                        405, 539, 580, 918,

                        # Oregon
                        458, 503, 541, 971,

                        # Pennsylvania
                        215, 223, 267, 272, 412, 445, 484, 570, 610, 717, 724, 814, 878,

                        # Rhode Island
                        401,

                        # South Carolina
                        803, 843, 854, 864,

                        # South Dakota
                        605,

                        # Tennessee
                        423, 615, 629, 731, 865, 901, 931,

                        # Texas940
                        210, 214, 254, 281, 325, 346, 361, 409, 430, 432, 469, 512, 682, 713, 726, 737, 806, 817, 830, 832, 903, 915, 936, 956, 972, 979,

                        # Utah
                        385, 435, 801,

                        # Vermont
                        802,

                        # Virginia
                        276, 434, 540, 571, 703, 757, 804, 826, 948,

                        # Washington
                        206, 253, 360, 425, 509, 564,

                        # West Virginia
                        304, 681,

                        # Wisconsin
                        262, 414, 534, 608, 715, 920,

                        # Wyoming
                        307,

                        # US Territories
                        # Puerto Rico
                        787, 939,
                        # US Virgin Islands
                        340,
        
                    ]
    area_code = random.choice(area_codes)
    central_office_code = random.randint(200, 999)
    station_number = random.randint(1000, 9999)
    return f"+1{area_code}{central_office_code}{station_number}"

def generate_email(first_name, yandex_mail, mail_other):
    random_suffix = ''.join(random.choices("0123456789", k=2))
    return f"{yandex_mail}+{first_name}{random_suffix}{mail_other}"

def generate_android_user_agent():
    android_versions = [
    "4.4",  # KitKat
    "5.0",  # Lollipop
    "6.0",  # Marshmallow
    "7.0",  # Nougat
    "8.0",  # Oreo
    "9.0",  # Pie
    "10.0", # Android 10
    "11.0", # Android 11
    "12.0", # Android 12
    "13.0", # Android 13
    "14.0", # Android 14 (latest as of 2023)
    ]

    # Device Models
    devices = [
        # Samsung Galaxy
        "SM-S908B",  # Galaxy S22 Ultra
        "SM-S901B",  # Galaxy S22
        "SM-S906B",  # Galaxy S22+
        "SM-S911B",  # Galaxy S23
        "SM-S916B",  # Galaxy S23+
        "SM-S918B",  # Galaxy S23 Ultra
        "SM-G991B",  # Galaxy S21
        "SM-G996B",  # Galaxy S21+
        "SM-G998B",  # Galaxy S21 Ultra
        "SM-G973F",  # Galaxy S10
        "SM-G975F",  # Galaxy S10+
        "SM-F936B",  # Galaxy Z Fold 4
        "SM-F721B",  # Galaxy Z Flip 4
        "SM-G960F",  # Galaxy S9
        "SM-G965F",  # Galaxy S9+
        "SM-G970F",  # Galaxy S10e
        "SM-G780F",  # Galaxy S20 FE
        "SM-G781B",  # Galaxy S20 FE 5G
        "SM-F700F",  # Galaxy Z Flip
        "SM-F711B",  # Galaxy Z Flip 3
        "SM-F926B",  # Galaxy Z Fold 3
        "SM-F946B",  # Galaxy Z Fold 5
        "SM-F731B",  # Galaxy Z Flip 5

        # Google Pixel
        "Pixel 4",  # Pixel 4
        "Pixel 4 XL",  # Pixel 4 XL
        "Pixel 5",  # Pixel 5
        "Pixel 6",  # Pixel 6
        "Pixel 6 Pro",  # Pixel 6 Pro
        "Pixel 7",  # Pixel 7
        "Pixel 7 Pro",  # Pixel 7 Pro
        "Pixel 8",  # Pixel 8
        "Pixel 8 Pro",  # Pixel 8 Pro
        "Pixel 3",  # Pixel 3
        "Pixel 3 XL",  # Pixel 3 XL
        "Pixel 3a",  # Pixel 3a
        "Pixel 3a XL",  # Pixel 3a XL
        "Pixel 4a",  # Pixel 4a
        "Pixel 4a 5G",  # Pixel 4a 5G
        "Pixel 5a",  # Pixel 5a
        "Pixel Fold",  # Pixel Fold

        # OnePlus
        "IN2023",  # OnePlus 8 Pro
        "IN2025",  # OnePlus 9
        "NE2215",  # OnePlus 10 Pro
        "CPH2417",  # OnePlus 11
        "CPH2451",  # OnePlus Nord 3
        "GM1917",  # OnePlus 7 Pro
        "GM1925",  # OnePlus 7T Pro
        "HD1905",  # OnePlus 7T
        "KB2003",  # OnePlus 8T
        "LE2125",  # OnePlus 9 Pro
        "NE2217",  # OnePlus 10T
        "CPH2581",  # OnePlus Open (Foldable)

        # Xiaomi
        "2201122C",  # Xiaomi 12
        "2203121C",  # Xiaomi 12 Pro
        "2210132C",  # Xiaomi 13
        "2201123G",  # Redmi Note 12 Pro+
        "23021RAAEG",  # Poco X5 Pro
        "2106118C",  # Xiaomi 11 Lite 5G NE
        "2203121G",  # Xiaomi 12X
        "2210132G",  # Xiaomi 13 Pro
        "2304FPN6DG",  # Redmi Note 12
        "23076PBC4G",  # Poco F5

        # Huawei
        "ANA-NX9",  # Huawei P40
        "ELS-NX9",  # Huawei P40 Pro
        "NOH-NX9",  # Huawei Mate 40 Pro
        "LIO-L29",  # Huawei Mate 30 Pro
        "TAS-L09",  # Huawei Mate 40
        "JAD-LX9",  # Huawei Mate 50 Pro

        # Oppo
        "CPH2025",  # Oppo Find X2
        "CPH2173",  # Oppo Find X3
        "CPH2307",  # Oppo Reno 8 Pro
        "CPH2249",  # Oppo Reno 7
        "CPH2357",  # Oppo Find N2 Flip
        "CPH2459",  # Oppo Reno 10 Pro+

        # Vivo
        "V2045",  # Vivo X60 Pro
        "V2156A",  # Vivo X70 Pro+
        "V2230A",  # Vivo X90 Pro
        "V2134",  # Vivo X70
        "V2204",  # Vivo X80
        "V2245",  # Vivo X100

        # Motorola
        "XT2141-1",  # Moto G Stylus 5G
        "XT2131-3",  # Moto Edge 20
        "XT2321-3",  # Moto Edge 30 Ultra
        "XT2201-2",  # Moto G Power (2022)
        "XT2301-5",  # Moto G Stylus 5G (2023)
        "XT2335-3",  # Moto Edge 40

        # Realme
        "RMX3085",  # Realme 8
        "RMX3471",  # Realme GT Neo 2
        "RMX3708",  # Realme GT 3
        "RMX3360",  # Realme GT Master Edition
        "RMX3370",  # Realme GT 2 Pro
        "RMX3687",  # Realme 11 Pro+

        # Sony Xperia
        "XQ-AT51",  # Xperia 1 II
        "XQ-BC62",  # Xperia 1 III
        "XQ-CT72",  # Xperia 1 IV
        "XQ-DQ72",  # Xperia 5 IV
        "XQ-DS72",  # Xperia 10 IV
        "XQ-CT54",  # Xperia 1 V

        # LG
        "LM-G900N",  # LG Velvet
        "LM-V600",  # LG V60 ThinQ
        "LM-K920",  # LG Wing
        "LM-G850",  # LG G8 ThinQ
        "LM-G910",  # LG G8X ThinQ
        "LM-Q730",  # LG Q52

        # Asus
        "ZS671KS",  # Asus ROG Phone 3
        "AI2201",  # Asus ROG Phone 6
        "AI2301",  # Asus Zenfone 10
        "ZS661KS",  # Asus ROG Phone 2
        "ZS670KS",  # Asus ROG Phone 5
        "AI2202",  # Asus ROG Phone 7
    ]

    # Chrome Versions
    chrome_versions = [
        "85.0.4183.81", "86.0.4240.99", "87.0.4280.88", "88.0.4324.93",
        "89.0.4389.90", "90.0.4430.93", "91.0.4472.77", "92.0.4515.159",
        "93.0.4577.82", "94.0.4606.71", "95.0.4638.54", "96.0.4664.45",
        "97.0.4692.99", "98.0.4758.102", "99.0.4844.73", "100.0.4896.127",
        "101.0.4951.61", "102.0.5005.78", "103.0.5060.134", "104.0.5112.102",
        "105.0.5195.136", "106.0.5249.119", "107.0.5304.105", "108.0.5359.128",
        "109.0.5414.119", "110.0.5481.177", "111.0.5563.147", "112.0.5615.137",
        "113.0.5672.93", "114.0.5735.198", "115.0.5790.166", "116.0.5845.187",
        "117.0.5938.92", "118.0.5993.88", "119.0.6045.105", "120.0.6099.109",
        "121.0.6167.85", "122.0.6261.69", "123.0.6312.58", "124.0.6367.91",
        "125.0.6422.78", "126.0.6478.54", "127.0.6532.78", "128.0.6587.89",
        "129.0.6668.99", "130.0.6725.101"  # Latest as of 2023
    ]
    android_version = random.choice(android_versions)
    device = random.choice(devices)
    chrome_version = random.choice(chrome_versions)
    return (
        f"Mozilla/5.0 (Linux; Android {android_version}; {device}) "
        f"AppleWebKit/537.36 (KHTML, like Gecko) "
        f"Chrome/{chrome_version} Mobile Safari/537.36"
    )

def arrange_windows(driver, position, max_columns=6):
    column = position % max_columns
    row = position // max_columns
    x = column * 315
    y = row * 0
    logging.info(f"Arranging window {position} at column {column + 1}, row {row + 1}")
    driver.set_window_position(x, y)

def read_yandex_credentials(file_path="Yandex.txt"):
    """Read Yandex email credentials from a file."""
    try:
        with open(file_path, "r") as file:
            line = file.readline().strip()
            if "|" in line:
                email_address, password = line.split("|", 1)
                return email_address.strip(), password.strip()
    except Exception as e:
        print(f"Failed to read Yandex credentials: {e}")
    return None, None

def extract_otp_from_text(text):
    """Extract OTP from a given text (subject or body)."""
    otp_match = re.search(r'\b\d{5}\b', text)
    return otp_match.group(0) if otp_match else None

def fetch_facebook_otp():
    """Fetch OTP from the latest Facebook email."""
    email_address, password = read_yandex_credentials()
    if not email_address or not password:
        logging.error("Error: Missing or invalid Yandex credentials.")
        return None

    try:
        with imaplib.IMAP4_SSL("imap.yandex.com") as imap:
            imap.login(email_address, password)
            imap.select("INBOX")  # Always check the INBOX first

            # Search for the latest email from Facebook
            status, messages = imap.search(None, 'FROM', 'registration@facebookmail.com')
            if status != "OK" or not messages[0]:
                logging.warning("No emails found from Facebook.")
                return None

            # Fetch the latest email
            latest_email_id = messages[0].split()[-1]
            status, msg_data = imap.fetch(latest_email_id, "(RFC822)")
            if status != "OK" or not msg_data:
                logging.error("Failed to fetch the email content.")
                return None

            # Parse the email content
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_header(msg["Subject"])[0]
                    subject = subject[0].decode(subject[1] or "utf-8") if isinstance(subject[0], bytes) else subject[0]
                    logging.info(f"Email Subject: {subject}")

                    # Extract OTP from the subject
                    otp = extract_otp_from_text(subject)
                    if otp:
                        logging.info(f"OTP extracted from subject: {otp}")
                        return otp

                    # Extract OTP from the email body
                    body = None
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()

                    if body:
                        otp = extract_otp_from_text(body)
                        if otp:
                            logging.info(f"OTP extracted from body: {otp}")
                            return otp

            logging.warning("No OTP found in the email.")
            return None

    except imaplib.IMAP4.error as e:
        logging.error(f"IMAP error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        traceback.print_exc()

    return None

def get_next_email(file_path="YourEmail.txt"):
    """Get the next email from the YourEmail.txt file and remove it from the file."""
    try:
        with open(file_path, "r") as file:
            emails = file.readlines()
        if emails:
            next_email = emails[0].strip()
            with open(file_path, "w") as file:
                file.writelines(emails[1:])
            return next_email
    except Exception as e:
        logging.error(f"Failed to read email from {file_path}: {e}")
    return None

def initialize_browser(chrome_driver_path, position, device_type, headless, yandex_mail, mail_other, use_random_password, custom_password=None, enable_otp=True, reg_with_1scemail=False):
    try:
        password = custom_password if not use_random_password else ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#", k=9))

        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument(f"user-agent={generate_android_user_agent()}")
        chrome_options.add_argument("--window-size=330,500")
        chrome_options.add_argument("--app=https://www.google.com")
        chrome_options.add_argument("--force-dark-mode")
        if headless:
            chrome_options.add_argument("--headless")

        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        with running_drivers_lock:
            running_drivers.append(driver)

        if not headless:
            arrange_windows(driver, position)
            driver.get("https://m.facebook.com/r.php")
            time.sleep(10)

            fake = Faker('en_US')
            first_name = fake.first_name()
            last_name = fake.last_name()
            phone_number = generate_us_phone_number()
            birth_year = str(random.randint(1980, 2005))
            if reg_with_1scemail:
                email = get_next_email()
                if not email:
                    logging.error("No email available in email.txt")
                    return
            else:
                email = generate_email(first_name, yandex_mail, mail_other)
            birth_day = str(random.randint(1, 30)).zfill(2)
            birth_month = str(random.randint(1, 12)).zfill(2)
            birth = birth_month + birth_day + birth_year
            sex = random.choice(["Male", "Female"])

            driver.find_element(By.XPATH, "//*[@aria-label='Get started']").click()
            time.sleep(5)
            driver.find_element(By.XPATH, "//*[@aria-label='First name']").send_keys(f"{first_name}")
            time.sleep(5)
            driver.find_element(By.XPATH, "//*[@aria-label='Last name']").send_keys(last_name)
            time.sleep(5)
            driver.find_element(By.XPATH, "//*[@aria-label='Next']").click()
            time.sleep(8)
            driver.find_element(By.XPATH, "//*[@aria-label='Birthday (0 year old)']").send_keys(birth)
            time.sleep(5)
            driver.find_element(By.XPATH, "//*[@aria-label='Next']").click()
            time.sleep(5)
            driver.find_element(By.XPATH, f"//*[@aria-label='{sex}']").click()
            time.sleep(5)
            driver.find_element(By.XPATH, "//*[@aria-label='Next']").click()
            time.sleep(5)
            driver.find_element(By.XPATH, "//*[@aria-label='Mobile number']").send_keys(phone_number)
            time.sleep(5)
            driver.find_element(By.XPATH, "//*[@aria-label='Next']").click()
            time.sleep(5)

            try:
                element_continue = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Continue creating account']"))
                )
                element_continue.click()
                logging.info("Clicked on 'Continue'.")
            except Exception as e:
                logging.error(f"Error: {e}")

            time.sleep(5)
            driver.find_element(By.XPATH, "//*[@aria-label='Password']").send_keys(password)
            time.sleep(5)
            driver.find_element(By.XPATH, "//*[@aria-label='Next']").click()
            time.sleep(5)
            driver.find_element(By.XPATH, "//*[@aria-label='Save']").click()
            time.sleep(15)
            driver.find_element(By.XPATH, "//div[@role='button' and @aria-label='I agree']").click()

            with open(CHECKPOINT_FILE, "a") as file:
                file.write(f"Facebook ID: {first_name.lower()}.{last_name.lower()}\n")
                file.write(f"Phone: {phone_number}\n")
                file.write(f"Name: {first_name} {last_name}\n")
                file.write(f"Birth Date: {birth_day}/{birth_month}/{birth_year}\n")
                file.write(f"Password: {password}\n")
                file.write("=" * 50 + "\n")
            time.sleep(5)

            try:
                element_continue = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Continue']"))
                )
                element_continue.click()
                logging.info("Clicked on 'Continue'.")
            except Exception as e:
                logging.error(f"Error: {e}")

            time.sleep(5)
            driver.find_element(By.XPATH, "//div[@role='button' and @aria-label='I didn’t get the code']").click()
            time.sleep(5)
            driver.find_element(By.XPATH, "//*[@aria-label='Confirm by email']").click()
            time.sleep(5)
            driver.find_element(By.XPATH, "//*[@aria-label='Email']").send_keys(email)
            time.sleep(5)
            driver.find_element(By.XPATH, "//*[@aria-label='Next']").click()
            time.sleep(15)
            if "checkpoint" in driver.current_url or "confirmation" in driver.current_url:
                cookies_list = driver.get_cookies()
                cookieString = ""
                for cookie in cookies_list[:-1]:
                    cookieString = cookieString + cookie["name"] + "=" + cookie["value"] + "; "
                cookie = cookieString + cookies_list[-1]["name"] + "=" + cookies_list[-1]["value"]
                logging.info(f"Cookies: {cookie}")
                uid = str(cookie).split('c_user=')[1].split(';')[0]
                logging.info(f"User ID: {uid}")
                registration_details = (
                    f"{uid}|"
                    f"{password}|"
                    f"{email}|"
                    f"{cookie}\n"
                )

                try:
                    with open(ACCOUNT_FILE, "a") as file:
                        file.write(registration_details)
                    logging.info("Registration details saved successfully.")
                except Exception as e:
                    logging.error(f"Error saving registration details: {e}")
                        # Fetch OTP and input it (if enabled)
            driver.get("https://m.facebook.com/confirmemail.php?email_changed&soft=hjk")
            time.sleep(5)
            driver.find_element(By.XPATH, '//span[@class="_200_"]/a[text()="Remove"]').click()
            time.sleep(5)
            
            if enable_otp:
                try:
                    otp = fetch_facebook_otp()
                    if otp:
                        # Locate and input OTP
                        otp_input = driver.find_element(By.XPATH, "//*[@id=\"m_conf_cliff_root_id\"]/div/div/form/div/input")
                        otp_input.clear()  # Ensure no existing input
                        otp_input.send_keys(otp)
                        time.sleep(5)
                        # Click the 'Next' button
                        next_button = driver.find_element(By.XPATH, "//*[@id=\"m_conf_cliff_root_id\"]/div/div/form/a")
                        next_button.click()
                        
                        # Wait for the next step to load
                        time.sleep(20)
                    else:
                        print("No OTP received. Please check the fetching function.")
                except Exception as e:
                    print(f"Error while handling OTP input: {e}") 
            
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        time.sleep(10)
        driver.quit()
        with running_drivers_lock:
            running_drivers.remove(driver)
        logging.info(f"Browser {position + 1} closed.")


def verify_license_online(license_key):
    try:
        response = requests.get(CONFIG_FILE, timeout=10)
        response.raise_for_status()
        data = response.json()
        for license_entry in data.get("licenses", []):
            if license_entry.get("key") == license_key:
                expiration_date = license_entry.get("expiration_date")
                return True, expiration_date
        return False, None
    except Exception as e:
        logging.error(f"License verification failed: {e}")
        return False, None

class LogViewWindow(QDialog):
    def __init__(self, log_file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Account Manager")
        self.setGeometry(200, 200, 1080, 500)
        self.setWindowIcon(QIcon('fb.ico'))
        layout = QVBoxLayout()
        self.log_table = QTableWidget(self)
        self.log_table.setColumnCount(4)
        self.log_table.setHorizontalHeaderLabels(["UID", "Password", "Email", "Cookies"])

        self.log_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.log_table)
        self.load_log_data(log_file_path)
        
        button_layout = QHBoxLayout()
        check_fb_live_button = QPushButton("Check Facebook Live", self)
        check_fb_live_button.clicked.connect(self.open_check_fb_live)
        button_layout.addWidget(check_fb_live_button)

        copy_all_uids_button = QPushButton("Save All Uid", self)
        copy_all_uids_button.clicked.connect(self.copy_all_uids_to_file)
        button_layout.addWidget(copy_all_uids_button)

        confirm_otp_button = QPushButton("RemovePhoneNumber", self)
        confirm_otp_button.clicked.connect(self.start_otp_process)
        button_layout.addWidget(confirm_otp_button)

        stop_otp_button = QPushButton("Stop", self)
        stop_otp_button.clicked.connect(self.stop_otp_process)
        button_layout.addWidget(stop_otp_button)

        

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.otp_thread = None  # Initialize otp_thread as None

        # Enable selection and copying of UID
        self.log_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.log_table.setSelectionMode(QTableWidget.SingleSelection)
        self.log_table.itemDoubleClicked.connect(self.copy_uid_to_clipboard)

    def copy_uid_to_clipboard(self, item):
        if item is None:
            QMessageBox.warning(self, "No Selection", "No item selected.")
            return
        
        # Get the UID from the selected item
        uid = item.text()
        
        # Copy UID to clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(uid)
        
        # Notify the user
        QMessageBox.information(self, "Copied", f"'{uid}' copied to clipboard.")


    def copy_all_uids_to_file(self):
        uids = []
        
        # Check if the table has any rows
        if self.log_table.rowCount() == 0:
            QMessageBox.warning(self, "No Data", "The table is empty.")
            return
        
        # Iterate through each row and collect UIDs from the first column
        for row in range(self.log_table.rowCount()):
            item = self.log_table.item(row, 0)
            if item is not None:  # Ensure the item exists
                uid = item.text()
                uids.append(uid)
        
        # Check if any UIDs were collected
        if not uids:
            QMessageBox.warning(self, "No UIDs", "No UIDs found in the table.")
            return
        
        # Save UIDs to file
        with open("UID.txt", "w") as file:
            file.write("\n".join(uids))
        
        # Notify the user
        QMessageBox.information(self, "Saved", "All UIDs saved to UID.txt.")

    def start_otp_process(self):
        global stop_flag
        stop_flag = False

        def otp_worker():
            while not stop_flag:
                print("Running OTP process...")
                time.sleep(5)  # Simulate OTP processing delay

        self.otp_thread = threading.Thread(target=otp_worker)
        self.otp_thread.start()

        def otp_process():
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            import time
            import random
            from concurrent.futures import ThreadPoolExecutor
            from email.header import decode_header
            import subprocess

            # Generate a random User-Agent
            def generate_android_user_agent():
                android_versions = ["13.0", "14.0"]
                devices = [
                    # Samsung Galaxy (with detailed versions)
                    "SM-S908B",  # Galaxy S22 Ultra
                    "SM-S901B",  # Galaxy S22
                    "SM-S906B",  # Galaxy S22+
                    "SM-S911B",  # Galaxy S23
                    "SM-S916B",  # Galaxy S23+
                    "SM-S918B",  # Galaxy S23 Ultra
                    "SM-G991B",  # Galaxy S21
                    "SM-G996B",  # Galaxy S21+
                    "SM-G998B",  # Galaxy S21 Ultra
                    "SM-G973F",  # Galaxy S10
                    "SM-G975F",  # Galaxy S10+
                    "SM-F936B",  # Galaxy Z Fold 4
                    "SM-F721B",  # Galaxy Z Flip 4

                    # Google Pixel
                    "Pixel 4",  # Pixel 4
                    "Pixel 4 XL",  # Pixel 4 XL
                    "Pixel 5",  # Pixel 5
                    "Pixel 6",  # Pixel 6
                    "Pixel 6 Pro",  # Pixel 6 Pro
                    "Pixel 7",  # Pixel 7
                    "Pixel 7 Pro",  # Pixel 7 Pro
                    "Pixel 8",  # Pixel 8
                    "Pixel 8 Pro",  # Pixel 8 Pro

                    # OnePlus
                    "IN2023",  # OnePlus 8 Pro
                    "IN2025",  # OnePlus 9
                    "NE2215",  # OnePlus 10 Pro
                    "CPH2417",  # OnePlus 11
                    "CPH2451",  # OnePlus Nord 3

                    # Xiaomi
                    "2201122C",  # Xiaomi 12
                    "2203121C",  # Xiaomi 12 Pro
                    "2210132C",  # Xiaomi 13
                    "2201123G",  # Redmi Note 12 Pro+
                    "23021RAAEG",  # Poco X5 Pro

                    # Huawei
                    "ANA-NX9",  # Huawei P40
                    "ELS-NX9",  # Huawei P40 Pro
                    "NOH-NX9",  # Huawei Mate 40 Pro

                    # Oppo
                    "CPH2025",  # Oppo Find X2
                    "CPH2173",  # Oppo Find X3
                    "CPH2307",  # Oppo Reno 8 Pro

                    # Vivo
                    "V2045",  # Vivo X60 Pro
                    "V2156A",  # Vivo X70 Pro+
                    "V2230A",  # Vivo X90 Pro

                    # Motorola
                    "XT2141-1",  # Moto G Stylus 5G
                    "XT2131-3",  # Moto Edge 20
                    "XT2321-3",  # Moto Edge 30 Ultra

                    # Realme
                    "RMX3085",  # Realme 8
                    "RMX3471",  # Realme GT Neo 2
                    "RMX3708",  # Realme GT 3

                    # Sony Xperia
                    "XQ-AT51",  # Xperia 1 II
                    "XQ-BC62",  # Xperia 1 III
                    "XQ-CT72",  # Xperia 1 IV

                    # LG
                    "LM-G900N",  # LG Velvet
                    "LM-V600",  # LG V60 ThinQ
                    "LM-K920",  # LG Wing

                    # Asus
                    "ZS671KS",  # Asus ROG Phone 3
                    "AI2201",  # Asus ROG Phone 6
                    "AI2301",  # Asus Zenfone 10
                ]
                chrome_versions = ["91.0.4472.77"]

                android_version = random.choice(android_versions)
                device = random.choice(devices)
                chrome_version = random.choice(chrome_versions)

                return (
                    f"Mozilla/5.0 (Linux; Android {android_version}; {device}) "
                    f"AppleWebKit/537.36 (KHTML, like Gecko) "
                    f"Chrome/{chrome_version} Mobile Safari/537.36"
                )

            # Function to arrange browser windows in a row
            def arrange_windows(driver, position, max_columns=6):
                column = position % max_columns
                row = position // max_columns
                x = column * 315
                y = row * 0
                logging.info(f"Arranging window {position} at column {column + 1}, row {row + 1}")
                driver.set_window_position(x, y)

            # Read cookies from file
            def read_credentials(file_path):
                credentials = []
                try:
                    with open(file_path, 'r') as file:
                        for line in file:
                            parts = line.strip().split('|')
                            if len(parts) >= 6:
                                cookie = parts[5]
                                credentials.append((cookie,))
                except Exception as e:
                    print(f"Error reading credentials: {e}")

                return credentials

            # Handle login using cookies
            def handle_login_with_cookie(profile_name, cookie, chrome_driver_path, position):
                chrome_options = Options()
                chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                chrome_options.add_argument(f"user-agent={generate_android_user_agent()}")
                chrome_options.add_argument("--window-size=330,500")
                chrome_options.add_argument("--app=https://m.facebook.com")
                chrome_options.add_argument("--force-dark-mode")

                service = Service(chrome_driver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)

                try:
                    arrange_windows(driver, position)
                    driver.get("https://m.facebook.com")
                    time.sleep(1)

                    cookie_list = [
                        {"name": kv.split("=")[0], "value": kv.split("=")[1]}
                        for kv in cookie.split("; ")
                    ]

                    for cookie in cookie_list:
                        driver.add_cookie(cookie)
                        time.sleep(1)

                    driver.get("https://m.facebook.com/confirmemail.php?email_changed&soft=hjk")
                    time.sleep(5)
                    driver.find_element(By.XPATH, '//span[@class="_200_"]/a[text()="Remove"]').click()
                    time.sleep(5)

                except Exception as e:
                    print(f"An error occurred for profile {profile_name}: {e}")

                finally:
                    driver.quit()

            # Main execution
            chrome_driver_path = "chromedriver.exe"
            credentials_file = "Account RemovePhone.txt"
            credentials = read_credentials(credentials_file)

            with ThreadPoolExecutor(max_workers=4) as executor:
                for idx, (cookie,) in enumerate(credentials):
                    profile_name = f"profile_{idx}"
                    executor.submit(handle_login_with_cookie, profile_name, cookie, chrome_driver_path, idx)
                    time.sleep(random.uniform(10, 10))

        # Run the OTP extraction process on a separate thread to avoid freezing the UI
        threading.Thread(target=otp_process).start()

    def stop_otp_process(self):
        global stop_flag
        stop_flag = True

        if getattr(self, "otp_thread", None):  # Check if thread exists
            if self.otp_thread.is_alive():
                self.otp_thread.join(timeout=5)  # Timeout to prevent deadlocks
                print("OTP Process Stopped")

        # Stop all running ChromeDriver instances
        with running_drivers_lock:
            for driver in running_drivers:
                try:
                    driver.quit()
                except Exception as e:
                    print(f"Error closing driver: {e}")
            running_drivers.clear()

        # Stop all ChromeDriver processes in the task manager
        if os.name == "nt":
            subprocess.run(["taskkill", "/f", "/im", "chromedriver.exe", "/t"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif os.name == "posix":
            subprocess.run(["pkill", "-f", "chromedriver"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def open_check_fb_live(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Facebook Check Live File", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, "r") as file:
                    selected_items = file.readlines()
                if selected_items:
                    uids = "\n".join([uid.strip() for uid in selected_items])
                    chrome_options = Options()
                    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                    chrome_options.add_argument("--start-maximized")
                    chrome_options.add_argument("--force-dark-mode") 
                    chrome_options.add_argument("--app=https://hitools.pro/check-live-uid")
                    service = Service(CHROME_DRIVER_PATH)
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    driver.get("https://hitools.pro/check-live-uid")
                    time.sleep(2)
                    driver.find_element(By.XPATH, "//*[@id='theme-toggle']").click()
                    time.sleep(2)
                    driver.find_element(By.XPATH, "//*[@id='listId']").send_keys(uids)
                    time.sleep(20)
                    driver.find_element(By.XPATH, "//*[@id='btnStart']").click()
                    time.sleep(30)
                    
                    # Select all UIDs in the live list and save to file
                    live_uids = driver.find_element(By.XPATH, "//*[@id='listLive']").text
                    with open("List of Live accounts.txt", "w") as live_file:
                        live_file.write(live_uids)
                    
                    # Select all UIDs in the dead list and save to file
                    dead_uids = driver.find_element(By.XPATH, "//*[@id='listDie']").text
                    with open("List of Dead accounts.txt", "w") as dead_file:
                        dead_file.write(dead_uids)
                    time.sleep(5)
                else:
                    QMessageBox.warning(self, "Facebook Live Check", "No UID found in the selected file.")
            except FileNotFoundError:
                QMessageBox.warning(self, "Facebook Live Check", "Selected file not found.")
            except Exception as e:
                QMessageBox.warning(self, "Facebook Live Check", f"An error occurred: {e}")
            finally:
                driver.quit()
        else:
            QMessageBox.warning(self, "Facebook Live Check", "No file selected.")

    def load_log_data(self, log_file_path):
        try:
            with open(log_file_path, "r") as file:
                log_data = file.readlines()
            self.log_table.setRowCount(len(log_data))
            for row, line in enumerate(log_data):
                parts = line.strip().split("|")
                if len(parts) == 4:
                    uid, password, email, cookies = parts
                    self.log_table.setItem(row, 0, QTableWidgetItem(uid))
                    self.log_table.setItem(row, 1, QTableWidgetItem(password))
                    self.log_table.setItem(row, 2, QTableWidgetItem(email))
                    self.log_table.setItem(row, 3, QTableWidgetItem(cookies))
        except FileNotFoundError:
            self.log_table.setRowCount(1)
            self.log_table.setItem(0, 0, QTableWidgetItem("Log file not found."))
        except Exception as e:
            self.log_table.setRowCount(1)
            self.log_table.setItem(0, 0, QTableWidgetItem(f"Error reading log file: {e}"))

class NewWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GET OTP Yandex")
        self.show_message()


        
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DEV By_Dt.Bunrith")
        self.setFixedSize(1080, 500)
        self.setWindowFlags(Qt.Dialog)
        self.setWindowIcon(QIcon('fb.ico'))


        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E3440;
            }
            QLabel {
                color: #D8DEE9;
                font-size: 14px;
            }
            QLineEdit, QComboBox {
                background-color: #4C566A;
                color: #ECEFF4;
                border: 1px solid #81A1C1;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #81A1C1;
                color: #2E3440;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #88C0D0;
            }
            QPushButton:disabled {
                background-color: #4C566A;
                color: #81A1C1;
            }
            QGroupBox {
                border: 1px solid #81A1C1;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                color: #D8DEE9;
                font-size: 16px;
            }
            QTextEdit {
                background-color: #4C566A;
                color: #ECEFF4;
                border: 1px solid #81A1C1;
                border-radius: 5px;
                padding: 5px;
            }
            QTableWidget {
                background-color: #4C566A;
                color: #ECEFF4;
                border: 1px solid #81A1C1;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        self.max_workers_input = QLineEdit()
        self.max_workers_input.setPlaceholderText("Enter max work (e.g., 6)")
        self.qlink_input = QLineEdit()
        self.qlink_input.setPlaceholderText("Enter number of Chrome (e.g., 100)")
        self.yandex_mail_input = QLineEdit()
        self.yandex_mail_input.setPlaceholderText("Enter Yandex mail prefix (e.g., yourname)")
        self.mail_other_input = QLineEdit()
        self.mail_other_input.setPlaceholderText("Enter email domain (e.g., @yandex.com)")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password or generate random")
        self.random_password_checkbox = QCheckBox("Use Random Password")
        self.random_password_checkbox.stateChanged.connect(self.toggle_random_password)
        self.device_type_dropdown = QComboBox()
        self.device_type_dropdown.addItems(["Android"])
        self.headless_checkbox = QCheckBox("Run in headless mode")
        self.shutdown_checkbox = QCheckBox("Shut Down PC ")
        self.otp_checkbox = QCheckBox("Enable Reg Full Verify")
        
        self.reg_with_1scemail_checkbox = QCheckBox("Reg With Your Email")
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.open_chrome_windows)
        self.start_button.setEnabled(False)
        self.stop_button = QPushButton("Stop All Browsers")
        self.stop_button.clicked.connect(self.stop_chrome_windows)
        self.stop_button.setEnabled(False)
        self.save_config_button = QPushButton("Save Config")
        self.save_config_button.clicked.connect(self.save_config)
        self.load_config_button = QPushButton("Load Config")
        self.load_config_button.clicked.connect(self.load_config)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.save_config_button)
        button_layout.addWidget(self.load_config_button)
        input_group = QGroupBox("Settings")
        input_layout = QFormLayout()
        input_layout.addRow("Max Work:", self.max_workers_input)
        input_layout.addRow("Number of Chrome:", self.qlink_input)
        input_layout.addRow("Yandex Mail Prefix:", self.yandex_mail_input)
        input_layout.addRow("Email Domain:", self.mail_other_input)
        input_layout.addRow("Password:", self.password_input)
        
        input_layout.addRow("Device Type:", self.device_type_dropdown)
        input_layout.addRow(self.random_password_checkbox)
        input_layout.addRow(self.otp_checkbox)
        input_layout.addRow(self.reg_with_1scemail_checkbox)
        
        
        input_layout.addRow(self.headless_checkbox)
        input_layout.addRow(self.shutdown_checkbox)
        
        input_group.setLayout(input_layout)
        left_layout.addWidget(input_group)
        left_layout.addLayout(button_layout)
        right_layout = QVBoxLayout()
        license_group = QGroupBox("License Key Verify")
        license_layout = QVBoxLayout()
        self.license_key_input = QLineEdit()
        self.license_key_input.setPlaceholderText("Enter your license key")
        self.license_key_input.setEchoMode(QLineEdit.Password)
        license_layout.addWidget(self.license_key_input)
        self.verify_license_button = QPushButton("Verify License")
        self.verify_license_button.clicked.connect(self.verify_license)
        license_layout.addWidget(self.verify_license_button)
        self.license_status = QTextEdit()
        self.license_status.setPlaceholderText("License verification status will appear here...")
        self.license_status.setReadOnly(True)
        license_layout.addWidget(self.license_status)
        license_group.setLayout(license_layout)
        right_layout.addWidget(license_group)
        countdown_group = QGroupBox("License Expired")
        countdown_layout = QVBoxLayout()
        self.countdown_label = QLabel("License expires in: -- days -- hours -- minutes -- seconds")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        countdown_layout.addWidget(self.countdown_label)
        countdown_group.setLayout(countdown_layout)
        right_layout.addWidget(countdown_group)
        
        # Create a horizontal layout for "Account Manager" and "GET OTP Yandex" buttons
        button_row_layout = QHBoxLayout()
        self.open_log_view_button = QPushButton("Account Manager")
        self.open_log_view_button.clicked.connect(self.open_log_view)
        self.open_log_view_button.setEnabled(False)  # Initially disabled
        button_row_layout.addWidget(self.open_log_view_button)
        
        self.get_otp_button = QPushButton("GET OTP Yandex")
        self.get_otp_button.clicked.connect(self.open_yandex_otp_window)
        self.get_otp_button.setEnabled(False)  # Initially disabled
        button_row_layout.addWidget(self.get_otp_button)
        
        right_layout.addLayout(button_row_layout)
        
        main_layout.addLayout(left_layout, 60)
        main_layout.addLayout(right_layout, 40)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.license_verified = False
        self.verification_time = None
        self.verified_license_key = None
        self.expiration_date = None
        self.load_saved_license_key()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)

        self.snow_effect = SnowEffect(self)
        self.snow_effect.lower()  # Ensure snow effect is behind other widgets

        self.clear_temp_directories()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.snow_effect.setFixedSize(self.size())

    def toggle_random_password(self):
        if self.random_password_checkbox.isChecked():
            password_characters = "abcdefgh0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#"
            random_password = ''.join(random.choices(password_characters, k=9))
            self.password_input.setText(random_password)
            self.password_input.setReadOnly(True)
        else:
            self.password_input.clear()
            self.password_input.setReadOnly(False)

    def load_saved_license_key(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                if "license_key" in config:
                    self.license_key_input.setText(config["license_key"])
                    self.verify_license()
        except FileNotFoundError:
            pass

    def save_license_key(self, license_key):
        config = {"license_key": license_key}
        with open("config.json", "w") as f:
            json.dump(config, f)

    def clear_saved_license_key(self):
        try:
            os.remove("config.json")
        except FileNotFoundError:
            pass

    def verify_license(self):
        entered_key = self.license_key_input.text()
        if self.verified_license_key:
            self.license_status.append("License key already used. Each key can only be used once.")
            return
        valid, expiration_date = verify_license_online(entered_key)
        if valid:
            self.license_verified = True
            self.verified_license_key = entered_key
            self.expiration_date = expiration_date
            self.start_button.setEnabled(True)
            self.open_log_view_button.setEnabled(True)  # Enable the button when license is verified
            self.get_otp_button.setEnabled(True)  # Enable the button when license is verified
            self.license_status.append("License key verified! You can now start the Tool.")
            self.license_status.append(f"License expires on: {expiration_date}")

            # Save the verification time
            self.verification_time = datetime.now().isoformat()


            self.save_license_key(entered_key)

        else:
            self.license_verified = False
            self.start_button.setEnabled(False)
            self.open_log_view_button.setEnabled(False)  # Ensure the button is disabled if verification fails
            self.get_otp_button.setEnabled(False)  # Ensure the button is disabled if verification fails
            self.license_status.append("Invalid license key. Please try again.")
            self.clear_saved_license_key()

    def update_countdown(self):
        if self.license_verified and self.expiration_date:
            expiration_date = datetime.fromisoformat(self.expiration_date)
            remaining_time = expiration_date - datetime.now()
            if (remaining_time.total_seconds() > 0):
                days = remaining_time.days
                hours, remainder = divmod(remaining_time.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                self.countdown_label.setText(
                    f"License expires in: {days} days {hours} hours {minutes} minutes {seconds} seconds"
                )
            else:
                self.countdown_label.setText("License has expired. Please verify again.")
                self.license_verified = False
                self.start_button.setEnabled(False)
                self.open_log_view_button.setEnabled(False)  # Disable the button if the license expires
                self.clear_saved_license_key()
        else:
            self.countdown_label.setText("License not verified or expired.")

    def open_chrome_windows(self):
        if not self.license_verified:
            QMessageBox.warning(self, "Error", "Please verify your license key first.")
            return
        try:
            max_workers = int(self.max_workers_input.text())
            num_instances = int(self.qlink_input.text())
            device_type = self.device_type_dropdown.currentText().lower()
            headless = self.headless_checkbox.isChecked()
            yandex_mail = self.yandex_mail_input.text().strip()
            mail_other = self.mail_other_input.text().strip()
            use_random_password = self.random_password_checkbox.isChecked()
            custom_password = self.password_input.text().strip() if not use_random_password else None
            enable_otp = self.otp_checkbox.isChecked()
            reg_with_1scemail = self.reg_with_1scemail_checkbox.isChecked()
            self.stop_button.setEnabled(True)
            self.start_button.setEnabled(False)
            threading.Thread(
                target=self._open_windows_thread,
                args=(max_workers, num_instances, device_type, headless, yandex_mail, mail_other, use_random_password, custom_password, enable_otp, reg_with_1scemail),
                daemon=True
            ).start()
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid numbers.")

    def _open_windows_thread(self, max_workers, num_instances, device_type, headless, yandex_mail, mail_other, use_random_password, custom_password=None, enable_otp=True, reg_with_1scemail=False):
        try:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                for _ in range(num_instances):
                    executor.submit(
                        initialize_browser, CHROME_DRIVER_PATH, _, device_type, headless, yandex_mail, mail_other, use_random_password, custom_password, enable_otp, reg_with_1scemail
                    )
                    random_delay = random.uniform(10, 11)
                    time.sleep(random_delay)
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid input. Please enter valid numbers.")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        if self.shutdown_checkbox.isChecked():
            self.shutdown_pc()

    def shutdown_pc(self):
        try:
            if os.name == "nt":
                os.system("shutdown /s /t 60")
            elif os.name == "posix":
                os.system("sudo shutdown -h now")
            else:
                logging.warning("Unsupported operating system for shutdown.")
        except Exception as e:
            logging.error(f"Failed to shut down PC: {e}")

    def stop_chrome_windows(self):
        global stop_flag
        stop_flag = True

        # Stop all running ChromeDriver instances
        with running_drivers_lock:
            for driver in running_drivers:
                try:
                    driver.quit()
                except Exception as e:
                    logging.error(f"Error closing driver: {e}")
            running_drivers.clear()

        # Stop all ChromeDriver processes in the task manager
        if os.name == "nt":
            subprocess.run(["taskkill", "/f", "/im", "chromedriver.exe", "/t"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif os.name == "posix":
            subprocess.run(["pkill", "-f", "chromedriver"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        self.stop_button.setEnabled(False)

    def save_config(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Config", "", "JSON Files (*.json)")
        if file_path:
            config = {
                "max_workers": self.max_workers_input.text(),
                "qlink": self.qlink_input.text(),
                "device_type": self.device_type_dropdown.currentText(),
                "headless": self.headless_checkbox.isChecked(),
                "shutdown": self.shutdown_checkbox.isChecked(),
                "yandex_mail": self.yandex_mail_input.text(),
                "mail_other": self.mail_other_input.text(),
                "random_password": self.random_password_checkbox.isChecked(),
                "password": self.password_input.text(),
            }
            with open(file_path, "w") as f:
                json.dump(config, f)

    def load_config(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Config", "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, "r") as f:
                config = json.load(f)
                self.max_workers_input.setText(config.get("max_workers", ""))
                self.qlink_input.setText(config.get("qlink", ""))
                self.device_type_dropdown.setCurrentText(config.get("device_type", "Android"))
                self.headless_checkbox.setChecked(config.get("headless", False))
                self.shutdown_checkbox.setChecked(config.get("shutdown", False))
                self.yandex_mail_input.setText(config.get("yandex_mail", ""))
                self.mail_other_input.setText(config.get("mail_other", ""))
                self.random_password_checkbox.setChecked(config.get("random_password", False))
                self.password_input.setText(config.get("password", ""))

    def open_log_view(self):
        log_file_path = ACCOUNT_FILE 
        self.log_view_window = LogViewWindow(log_file_path, self)
        self.log_view_window.exec_()
        

    def open_yandex_otp_window(self):
        if not self.license_verified:
            QMessageBox.warning(self, "Error", "Please verify your license key first.")
            return
        self.yandex_otp_window = YandexOtpApp()
        self.yandex_otp_window.show()

    def closeEvent(self, event):
        self.stop_chrome_windows()
        event.accept()

    def clear_temp_directories(self):
        clear_temp_directories()

def clear_temp_directories():
    temp_dirs = [os.getenv('TEMP'), os.getenv('TMP')]
    for temp_dir in temp_dirs:
        if temp_dir and os.path.exists(temp_dir):
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                    except Exception as e:
                        logging.error(f"Failed to remove {file}: {e}")
                for dir in dirs:
                    try:
                        os.rmdir(os.path.join(root, dir))
                    except Exception as e:
                        logging.error(f"Failed to remove {dir}: {e}")

class YandexOtpApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('GET Yandex OTP')
        self.setWindowIcon(QIcon('fb.ico'))

        self.setFixedSize(400, 380)
        self.setWindowFlags(Qt.Dialog)

        self.setGeometry(100, 100, 420, 330)
        

        # Set a stylesheet for the application
        self.setStyleSheet("""
            QWidget {
                background-color: #2E3440;
                color: #ECEFF4;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #4C566A;
                color: #ECEFF4;
                border: 1px solid #81A1C1;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #81A1C1;
                color: #2E3440;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #88C0D0;
            }
            QPushButton:pressed {
                background-color: #5E81AC;
            }
            QPushButton:disabled {
                background-color: #4C566A;
                color: #777777;
            }
            QMessageBox {
                background-color: #2E3440;
                color: #ECEFF4;
            }
            QGroupBox {
                border: 1px solid #81A1C1;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                color: #D8DEE9;
                font-size: 16px;
            }
        """)

        layout = QVBoxLayout()

        email_groupbox = QGroupBox("Yandex Email")
        email_layout = QVBoxLayout()

        # Remove the Yandex Email label
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('Enter Your YandexEmail')
        email_layout.addWidget(self.email_input)
        # App Password Input
        self.password_label = QLabel('App Password:')
        self.password_label.setFont(QFont("Arial", 12))
        email_layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Enter your app password')
        self.password_input.setEchoMode(QLineEdit.Password)
        email_layout.addWidget(self.password_input)

        # Save Button
        self.save_button = QPushButton('Save', self)
        self.save_button.clicked.connect(self.save_credentials)
        email_layout.addWidget(self.save_button)

        email_groupbox.setLayout(email_layout)
        layout.addWidget(email_groupbox)

        # YourEmail GroupBox
        your_email_groupbox = QGroupBox("YourEmail")
        your_email_layout = QVBoxLayout()

        self.this_email_input = QLineEdit(self)
        self.this_email_input.setPlaceholderText('Enter YourEmail')
        your_email_layout.addWidget(self.this_email_input)

        your_email_groupbox.setLayout(your_email_layout)
        layout.addWidget(your_email_groupbox)

        # Fetch OTP Button
        self.fetch_button = QPushButton('GET OTP', self)
        self.fetch_button.clicked.connect(self.fetch_otp)
        layout.addWidget(self.fetch_button)

        # Result Label
        self.result_label = QLabel('')
        self.result_label.setFont(QFont("Arial", 14))
        self.result_label.setStyleSheet("color: #88C0D0;")  # Set a custom color for the result
        layout.addWidget(self.result_label)

        # Copy OTP Button
        self.copy_otp_button = QPushButton('Copy OTP', self)
        self.copy_otp_button.clicked.connect(self.copy_otp)
        self.copy_otp_button.setEnabled(False)  # Disabled by default
        layout.addWidget(self.copy_otp_button)

        self.setLayout(layout)

        # Load saved credentials (if any)
        self.load_credentials()


    def load_credentials(self):
        """
        Loads saved credentials from the file and populates the email and password fields.
        """
        credentials = get_credentials_from_file("Yandexsave.txt")
        if credentials:
            self.email_input.setText(credentials[0])
            self.password_input.setText(credentials[1])

    def save_credentials(self):
        """
        Saves the Yandex email and app password to a file.
        """
        username = self.email_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Input Error', 'Please fill in both email and password fields.')
            return

        if save_credentials_to_file("Yandexsave.txt", username, password):
            QMessageBox.information(self, 'Success', 'saved successfully!')
        else:
            QMessageBox.warning(self, 'Error', 'Failed to save credentials.')

    def fetch_otp(self):
        username = self.email_input.text()
        password = self.password_input.text()
        thisEmail = self.this_email_input.text()

        if not username or not password or not thisEmail:
            QMessageBox.warning(self, 'Input Error', 'Please fill in all fields.')
            return

        code = get_code_from_email(username, password, thisEmail)
        self.result_label.setText(f'OTP Code: {code}')
        self.copy_otp_button.setEnabled(code != "0")  # Enable the Copy OTP button if a valid code is fetched

    def copy_otp(self):
        """
        Copies the extracted OTP to the clipboard.
        """
        clipboard = QApplication.clipboard()
        code = self.result_label.text().replace("OTP Code: ", "").strip()
        if code != "0":
            clipboard.setText(code)
            QMessageBox.information(self, 'Success', 'OTP copied to clipboard!')
        else:
            QMessageBox.warning(self, 'Error', 'No valid OTP to copy.')

def get_credentials_from_file(file_path):
    """
    Reads the Yandex username and password from the specified file.
    """
    try:
        with open(file_path, "r") as file:
            line = file.readline().strip()
            if "|" in line:
                username, password = line.split("|", 1)
                return username.strip(), password.strip()
    except Exception as e:
        print(f"Error reading credentials: {e}")
    return None, None

def save_credentials_to_file(file_path, username, password):
    """
    Saves the Yandex username and password to the specified file.
    """
    try:
        with open(file_path, "w") as file:
            file.write(f"{username}|{password}")
        return True
    except Exception as e:
        print(f"Error saving credentials: {e}")
        return False

def get_code_from_email(username, password, thisEmail):
    """
    Retrieves a code from the subject of the latest email sent to a specific address.
    """
    GET_CODE = "No emails found"
    mail = None
    try:
        # Connect to Yandex IMAP server
        imap_server = "imap.yandex.com"
        mail = imaplib.IMAP4_SSL(imap_server)

        # Login to the email account
        mail.login(username, password)

        # Select the folder (e.g., "INBOX", "Spam", "Social")
        status, _ = mail.select("Social")  # Change folder name if needed
        if status != "OK":
            print("Failed to select folder. Defaulting to INBOX.")
            mail.select("INBOX")  # Fallback to INBOX if "Social" fails

        # Search for emails sent to the specified address
        status, messages = mail.search(None, f'TO "{thisEmail}"')
        if status != "OK" or not messages[0]:
            print("No emails found for the specified recipient.")
            return GET_CODE

        # Get the latest email ID
        email_ids = messages[0].split()
        latest_email_id = email_ids[-1]

        # Fetch the latest email
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        if status != "OK":
            print("Failed to fetch the email.")
            return GET_CODE

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                # Parse the email
                msg = email.message_from_bytes(response_part[1])

                # Decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")

                print(f"Subject: {subject}")  # Debugging purpose

                # Extract the code from the subject
                match = re.search(r"(\d+)", subject)
                if match:
                    GET_CODE = match.group(1)
                else:
                    # Handle different subject formats
                    match = re.search(r"Code: (\d+)", subject)
                    if match:
                        GET_CODE = match.group(1)

    except imaplib.IMAP4.error as imap_error:
        print(f"IMAP error occurred: {imap_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if mail:
            mail.close()
            mail.logout()
        return GET_CODE

class Snowflake(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(10, 10)
        self.setStyleSheet("background-color: white; border-radius: 5px;")

class SnowEffect(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(parent.size())
        self.snowflakes = []

        for _ in range(100):
            snowflake = Snowflake(self)
            snowflake.move(random.randint(0, self.width()), random.randint(-self.height(), 0))
            self.snowflakes.append(snowflake)
            self.animate_snowflake(snowflake)

    def animate_snowflake(self, snowflake):
        animation = QPropertyAnimation(snowflake, b"pos")
        animation.setDuration(random.randint(5000, 10000))
        animation.setStartValue(snowflake.pos())
        animation.setEndValue(QPointF(snowflake.x(), self.height()))
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.finished.connect(lambda: self.reset_snowflake(snowflake))
        animation.start()

    def reset_snowflake(self, snowflake):
        snowflake.move(random.randint(0, self.width()), random.randint(-self.height(), 0))
        self.animate_snowflake(snowflake)

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
