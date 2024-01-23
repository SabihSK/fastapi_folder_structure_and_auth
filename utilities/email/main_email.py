import email.mime.text as mime
import smtplib
import ssl
from email.mime import multipart

from configuration.configure import sender_email, sender_password
from configuration.constants import PROJECT_TITLE


def gmail_html_email_sender(
    username: str,
    db_otp: str,
    receiver_email: str,
    email_template: str,
) -> None:
    file_location = "utilities/email/custom_emails/" + email_template + ".html"
    with open(
        file_location,
        "r",
        encoding="utf-8",
    ) as file:
        html_content = file.read()
        context = ssl.create_default_context()
        smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
        smtp_server.login(sender_email, sender_password)
        msg = multipart.MIMEMultipart()
        html_part = mime.MIMEText(
            html_content.format(
                username=username, otp=db_otp, receiver_email=receiver_email
            ),
            "html",
        )
        msg.attach(html_part)
        msg["Subject"] = "OTP verification"
        msg["From"] = PROJECT_TITLE  # + " <" + sender_email + ">"
        msg["To"] = receiver_email
        smtp_server.sendmail(sender_email, receiver_email, msg.as_string())
        smtp_server.quit()
