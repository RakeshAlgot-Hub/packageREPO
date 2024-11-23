import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import emailConfig

server = None

def _createSmtpServer():
    global server
    try:
        if server is None:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(emailConfig.accountAddress, emailConfig.accountPassword)
            print("Logged in successfully.")
            return server
    except Exception as e:
        print(f"Failed to connect and login: {e}")
        raise


def sendEmail(toEmail, subject, body,logger, isHtml=False):
    global server
    try:
        if server is None:
            server = _createSmtpServer(logger)
        if server:
            msg = MIMEMultipart()
            msg["From"] = emailConfig.accountAddress
            msg["To"] = toEmail
            msg["Subject"] = subject
            if isHtml:
                msg.attach(MIMEText(body, "html"))
            else:
                msg.attach(MIMEText(body, "plain"))
            server.sendmail(emailConfig.accountAddress, toEmail, msg.as_string())
            logger.debug(f"Email sent successfully to {toEmail}")
            print(f"Email sent successfully to {toEmail}")
    except Exception as e:
        logger.error(f"Failed to send email from Gmail: {e}")
        print(f"Failed to send email: {e}")
        raise
