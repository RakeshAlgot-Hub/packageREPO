import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import emailConfig

server = None


def _createSmtpServer():
    global server
    try:
        if server is None:
            server = smtplib.SMTP("smtpout.secureserver.net", 587)
            server.starttls()
            server.login(emailConfig.accountAddress, emailConfig.accountPassword)
            print("Logged in successfully.")
            return server
    except Exception as e:
        print(f"Failed to connect and login: {e}")
        raise
    
def _ensureServerConnection():
    global server
    if server is None:
        server = _createSmtpServer()
    else:
        try:
            status = server.noop()[0]
            if status != 250:
                server = _createSmtpServer()
        except:
            server = _createSmtpServer()
            

def sendEmail(toEmail, subject, body, logger, isHtml=False):
    global server
    try:
        _ensureServerConnection()
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
            print(f"Email sent to {toEmail} using GoDaddy.")
            return True
        else:
            logger.error("Failed to send email from godaddy. Server is None.")
    except Exception as e:
        logger.error(f"Failed to send email from godaddy: {e}")
        print(f"Failed to send email: {e}")
        raise
