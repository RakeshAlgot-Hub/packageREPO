from .config import emailConfig,setupLogging
import pkg_resources

if emailConfig.emailProvider == "SendGrid":
    from .SendGrid import sendEmail
elif emailConfig.emailProvider == "GoDaddy":
    from .GoDaddy import sendEmail
elif emailConfig.emailProvider == "Gmail":
    from .Gmail import sendEmail
else:
    print("Please Provide emailProvider")


def sendOtpViaEmail(email, subject, otp, userName):
    if emailConfig.DEMO_MODE:
        return True
    logger = setupLogging()
    
    template = pkg_resources.resource_string(__name__, "EmailTemplates/OtpTemplate.html").decode("utf-8")
    template = template.replace("{{OTP}}", otp).replace("{{USER_NAME}}", userName)
    
    try:
        
        if not emailConfig.accountAddress or not emailConfig.accountPassword:
            raise ValueError("Please provide a valid account address and password in the email configuration.")
        
        logger.debug(f"Sending OTP to {email}")
        sendEmail(email, subject, template, logger, isHtml=True)
        logger.debug(f"Email sent to {email}")
        print(f"Email sent to {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send otp via email: {e}")
        print(f"Failed to send email: {e}")
        raise


def sendTeamPlayerInviteEmail(toEmail, subject, userName, teamName, inviteLink):
    if emailConfig.DEMO_MODE:
        return True
    logger = setupLogging()
    
    template = pkg_resources.resource_string(__name__, "EmailTemplates/TeamPlayerInviteTemplate.html").decode("utf-8")
    template = template.replace("{{USER_NAME}}", userName).replace("{{TEAM_NAME}}", teamName).replace("{{INVITE_LINK}}", inviteLink)
    
    try:
        
        if not emailConfig.accountAddress or not emailConfig.accountPassword:
            raise ValueError("Please provide a valid account address and password in the email configuration.")
        
        logger.debug(f"Sending team player invite to {toEmail}")
        sendEmail(toEmail, subject, template, logger, isHtml=True)
        logger.debug(f"Email to invite team player to {toEmail}")
        print(f"Email sent to {toEmail}")
        return True
    except Exception as e:
        logger.error(f"Failed to send team player invite email: {e}")
        print(f"Failed to send email: {e}")
        raise


def sendTeamOwnerInviteEmail(toEmail, subject, userName, teamName, inviteLink):
    if emailConfig.DEMO_MODE:
        return True
    logger = setupLogging()
    
    template = pkg_resources.resource_string(__name__, "EmailTemplates/TeamOwnerInviteTemplate.html").decode("utf-8")
    template = template.replace("{{USER_NAME}}", userName).replace("{{TEAM_NAME}}", teamName).replace("{{INVITE_LINK}}", inviteLink)
    
    try:
        
        if not emailConfig.accountAddress or not emailConfig.accountPassword:
            raise ValueError("Please provide a valid account address and password in the email configuration.")
        
        logger.debug(f"Sending team owner invite to {toEmail}")
        sendEmail(toEmail, subject, template, logger, isHtml=True)
        logger.debug(f"Email to invite team owner to {toEmail}")
        print(f"Email sent to {toEmail}")
        return True
    except Exception as e:
        logger.error(f"Failed to send team owner invite email: {e}")
        print(f"Failed to send email: {e}")
        raise




def sendResetPassword(email, token, userName):
    if emailConfig.DEMO_MODE:
        return True
    
    if not emailConfig.emailBaseUrl:
        print("Please provide emailBaseUrl to send the reset link.")
        return False
    
    logger = setupLogging()

    resetLink = f"{emailConfig.emailBaseUrl}/auth/resetPassword?token={token}"
    
    template = pkg_resources.resource_string(__name__, "EmailTemplates/ResetPasswordTemplate.html").decode("utf-8")
    template = template.replace("{{RESET_LINK}}", resetLink).replace("{{USER_NAME}}", userName)

    try:
        if not emailConfig.accountAddress or not emailConfig.accountPassword:
            raise ValueError("Please provide a valid account address and password in the email configuration.")
        
        logger.debug(f"Sending reset password link to {email}")
        sendEmail(email, "Reset Password", template, logger,isHtml=True)
        logger.debug(f"Reset Password Email sent to {email}")
        print(f"Email sent to {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send reset password email: {e}")
        print(f"Failed to send email: {e}")
        raise
