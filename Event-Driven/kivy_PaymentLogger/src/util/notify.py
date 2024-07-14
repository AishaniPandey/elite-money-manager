from kafka_Producer import kafka_Producer
from kafka import KafkaConsumer
from global_Data import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logger import Logger
import threading
import json


logger = Logger()


class Notify(): 

    def send_Notification (self, to_Email, subject, body):
        
        message = {
            "to_Email" : to_Email,
            "subject": subject,
            "body": body,
        }

        while True:
            try:
                producerForLogging = kafka_Producer()
                producerForLogging.send_message("notify", message)
                break

            except Exception as ex:
                logger.log_Message("notification", "ERROR", f'Error while sending notification through kafka to {to_Email}: {ex}')



    def process_Notification (self):

        consumer = KafkaConsumer("notify", bootstrap_servers=[KAFKA_IP+":"+KAFKA_PORT_NO])

        try:
            for message in consumer:

                messageContents = json.loads(message.value)

                smtp_server = 'smtp.gmail.com'
                smtp_port = 587  # For SSL: 465, For TLS: 587
                sender_email = 'fornotificationuseseproject3@gmail.com'  
                password = 'fdyilrhtqqfdxvws'  

                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = messageContents["to_Email"]
                msg['Subject'] = messageContents["subject"]

                body = messageContents["body"]
                msg.attach(MIMEText(body, 'plain'))

                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, password)

                text = msg.as_string()
                server.sendmail(sender_email, messageContents["to_Email"], text)

                server.quit()

                logger.log_Message("notification", "INFO", f'An email to {messageContents["to_Email"]} has been successfully sent')
        

        except Exception as ex:
            logger.log_Message("notification", "ERROR", f'Error in sending an email to {messageContents["to_Email"]}: {ex}')


    def start_Notification(self):
        t = threading.Thread(target=self.process_Notification, args=( ))
        t.start()


if __name__ == '__main__':
    notify = Notify()
    notify.start_Notification()
