import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup
import time

# Gmail Configuration
GMAIL_USER = 'alertprimo@gmail.com'
GMAIL_PASS = 'Safdal123'  # Generate an app password for Gmail (see instructions below)
TO_EMAIL = 'muhammedsafdal@mail.com'

# Keywords to search
KEYWORDS = ['Quant Small Cap Fund selling Primo Chemicals Ltd']

# Websites to monitor (add more as needed)
WEBSITES = [
    "https://www.moneycontrol.com/",
    "https://economictimes.indiatimes.com/",
]

# Send email function
def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Scrape websites for keywords
def check_websites():
    for website in WEBSITES:
        try:
            response = requests.get(website)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()
            
            for keyword in KEYWORDS:
                if keyword.lower() in text.lower():
                    send_email(
                        subject=f"Alert: {keyword} Found!",
                        body=f"The following keyword was found on {website}:\n\n{keyword}"
                    )
        except Exception as e:
            print(f"Error checking website {website}: {e}")

# Main loop
def main():
    print("Starting keyword monitoring...")
    while True:
        check_websites()
        time.sleep(3600)  # Check every hour

if __name__ == "__main__":
    main()
