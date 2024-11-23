from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .config import emailConfig


def sendEmail(toEmail: str, subject: str, body: str, logger, isHtml: bool = False,):
    if emailConfig.DEMO_MODE:
        return True

    message = Mail(
        from_email=emailConfig.accountAddress,
        to_emails=toEmail,
        subject=subject,
        html_content=body
    )
    try:
        logger.debug(f"Sending email to {toEmail} using SendGrid")
        sg = SendGridAPIClient(emailConfig.accountPassword)
        response = sg.send(message)
        logger.debug(f"Email sent to {toEmail}, Status Code: {response.status_code}")
        print(f"Email sent to {toEmail}, Status Code: {response.status_code}")
        return True
    except Exception as e:
        logger.error(f"failed to send email from sendgrid,error:{str(e)}")
        raise Exception(f"Failed to send email: {str(e)}")