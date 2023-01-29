import time
import hashlib
from bs4 import BeautifulSoup
from lxml import html
import requests
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

_ = load_dotenv()
email_address = os.environ.get("EMAIL_ADDRESS")
email_password = os.environ.get("EMAIL_PASSWORD")
error_address = os.environ.get("ERROR_ADDRESS")
recipients = os.environ.get("RECIPIENTS")

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }
url ='https://www.collegept.org/case-of-the-month'
    
response = requests.get(url, headers=HEADERS)

print(response)

tree = html.fromstring(response.content)
unicode_date = tree.xpath('//*[@id="cph_content_T7A75863F005_Col00"]/div[1]/ul/li[1]/div[1]/text()')
current_str_date = ''.join([str(d) for d in unicode_date])

print(f"current_str_date: {current_str_date}")


def send_email(to, subject, message):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg.set_content(message)
        msg['From'] = email_address
        msg['To'] = to

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)    
            smtp.close()
            print ("Email sent successfully!")   
        return True
    except Exception as e:
        print("Problem while sending email")
        print(str(e))
    return False


while True:
    try:
        time.sleep(43200)
        new_response = requests.get(url, headers=HEADERS)
        new_tree = html.fromstring(response.content)
        new_unicode_date = tree.xpath('//*[@id="cph_content_T7A75863F005_Col00"]/div[1]/ul/li[1]/div[1]/text()')
        new_str_date = ''.join([str(d) for d in unicode_date])
        print(f"new_str_date: {new_str_date}")

        if current_str_date == new_str_date:
            print("nothing changed")
            continue
        else:
            print("site updated! sending notification email")
            # send email notification
            subject = 'New Case of the Month added!'
            message = 'Click here to read: https://www.collegept.org/case-of-the-month'
            send_email(recipients, subject, message)
            time.sleep(43200)

            response = requests.get(url, headers=HEADERS)
            tree = html.fromstring(response.content)
            unicode_date = tree.xpath('//*[@id="cph_content_T7A75863F005_Col00"]/div[1]/ul/li[1]/div[1]/text()')
            current_str_date = ''.join([str(d) for d in unicode_date])
            print(f"updated current_str_date: {current_str_date}")
            continue

    except Exception as e:
        print(f"Error! Sending error email. {e}")
        subject = 'Error with Python Script: COP - Case of the Month'
        message = f'Error with COP - Case of the Month. {e}'
        send_email(error_address, subject, message)
