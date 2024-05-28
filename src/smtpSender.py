from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.htmlGenerator import HTMLEmail

# NOTE: the vlist is a dictionary containing video records
def generateEmailMsg(emailSubject, sender_email, receiver_email, vlist: list): 
    # Header
    message = MIMEMultipart("alternative")
    message["Subject"] = emailSubject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Payload (HTML)
    title = "Bilibili Posts Update"
    desc = datetime.now().strftime("%Y%m%d")
    htmlEmail = HTMLEmail(title, desc, vlist)
    htmlContent = htmlEmail.generate()
    htmlMsg = MIMEText(htmlContent, "html")
    message.attach(htmlMsg)
    
    # Show digest
    print('emailSubject: ', emailSubject)
    print('title: ', title)
    print('description: ', desc)
    return message

def notify(smtp_port, smtp_server, login, password, emailMsg):
    # Sending the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(login, password)
            server.sendmail(
                sender_email,
                receiver_email,
                emailMsg.as_string()
            )
       # Confirmation
        print('The msg is sent')
        return True
    except:
        return False

