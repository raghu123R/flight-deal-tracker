import smtplib
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

class NotificationManager:

    def __init__(self):
        #  TWILIO (SMS ONLY)
        self.client = Client(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH')
        )

        self.twilio_number = os.getenv('TWILIO_NUMBER')
        self.my_number = os.getenv('MY_NUMBER')

        #  EMAIL SETUP
        self.smtp_address = os.getenv("EMAIL_PROVIDER_SMTP_ADDRESS")
        self.email = os.getenv("MY_EMAIL")
        self.email_password = os.getenv("MY_EMAIL_PASSWORD")

    # SMS
    def send_sms(self, message_body):
        message = self.client.messages.create(
            from_=self.twilio_number,
            body=message_body,
            to=self.my_number
        )
        print(message.sid)

    #  EMAIL
    def send_emails(self, email_list, email_body):

        with smtplib.SMTP(self.smtp_address, 587, timeout=30) as connection:
            connection.starttls()
            connection.login(self.email, self.email_password)

            for email in email_list:
                connection.sendmail(
                    from_addr=self.email,
                    to_addrs=email,
                    msg=f"Subject:✈️ New Low Price Flight!\n\n{email_body}".encode("utf-8")
                )

                print(f"Email sent to {email}")