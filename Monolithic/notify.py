import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logger import Logger


logger = Logger()



class Notify(): 

    def send_Notification (self, to_Email, subject, body):
        
        message = {
            "to_Email" : to_Email,
            "subject": subject,
            "body": body,
        }

        try:

            smtp_server = 'smtp.gmail.com'
            smtp_port = 587  # For SSL: 465, For TLS: 587
            sender_email = 'fornotificationuseseproject3@gmail.com'  
            password = 'fdyilrhtqqfdxvws'  

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = message["to_Email"]
            msg['Subject'] = message["subject"]

            body = message["body"]
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, password)

            text = msg.as_string()
            server.sendmail(sender_email, message["to_Email"], text)

            server.quit()

            logger.log_Message("notification", "INFO", f'An email to {message["to_Email"]} has been successfully sent')
        

        except Exception as ex:
            logger.log_Message("notification", "ERROR", f'Error in sending an email to {message["to_Email"]}: {ex}')
