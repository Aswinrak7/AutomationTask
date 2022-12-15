from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl


def send_mail(message, to_mail=None):
    # Setup port number and servr name

    global TIE_server
    smtp_port = 587  # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server

    email_from = "automationtask2022@gmail.com"
    email_to = "automationtask2022@gmail.com"  # to_mail "Please edit receiver email ID in email_to"

    # if not email_to:
    # email_to = email_from

    pswd = "gfjrfzlwhrrelrfp"

    # Create context
    simple_email_context = ssl.create_default_context()

    try:
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = "Notification Reminder : Wallet Balance"
        msg.attach(MIMEText(message, 'plain'))
        text = msg.as_string()
        # Connect to the server
        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls(context=simple_email_context)
        TIE_server.login(email_from, pswd)
        print("Connected to server :-)")

        # Send the actual email
        print(f"Sending email to - {email_to}")
        TIE_server.sendmail(email_from, email_to, text)
        print(f"Email successfully sent to - {email_to}")

    # If there's an error, print it out
    except Exception as e:
        print(e)

    # Close the port
    finally:
        TIE_server.quit()


if __name__ == '__main__':
    send_mail("message")
