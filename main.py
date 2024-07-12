import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import schedule
import time
import os
from dotenv import load_dotenv

load_dotenv()


#counter
email_counter = 0


def send_email():
    global email_counter
    sender_email = "samplemail@outlook.com"
    receiver_email = ["samplemail@gmail.com"]
    # Add your password in .env file
    password = os.getenv("EMAIL_PASSWORD")
    smtp_server = "smtp.office365.com"
    smtp_port = 587

    subject = ("YOUR SUBJECT")
    body = (
        "Hello,\n\n"
        "THIS IS A SAMPLE EMAIL BODY FORMAT\n\n"
        "Regards,\n"
        "FIRSTNAME LASTNAME\n"
        "DEPARTMENT\n"
        "POSITION\n"
    )

    msg = MIMEMultipart()
    msg['From'] = sender_email
    if len(receiver_email) > 0:
        msg['To'] = ", ".join(receiver_email)
    else:
        msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # # List of image file paths
    image_paths = ["./sample file.jpg"]

    # Iterate over each image file path
    for image_path in image_paths:
        with open(image_path, "rb") as image_file:
            # Read the image file
            image_data = image_file.read()
            # Create a MIMEImage object
            image = MIMEImage(image_data)
            # Add a header to indicate the filename
            image.add_header("Content-Disposition", "attachment", filename=os.path.basename(image_path))
            # Attach the image to the email
            msg.attach(image)

    # List of PDF file paths
    pdf_paths = ["./Sample File.pdf"]

    # Iterate over each PDF file path
    for pdf_path in pdf_paths:
        with open(pdf_path, "rb") as pdf_file:
            # Read the PDF file
            pdf_data = pdf_file.read()
            # Create a MIMEApplication object
            pdf_attachment = MIMEApplication(pdf_data)
            # Add a header to indicate the filename
            pdf_attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(pdf_path))
            # Attach the PDF to the email
            msg.attach(pdf_attachment)

    server = None  # Initialize the server variable

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        email_counter += 1
        print(f"Email sent successfully, total emails sent: {email_counter}")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        if server:
            server.quit()


#First email sends immediately, IF YOU DO NOT WANT TO SEND THE FIRST EMAIL IMMEDIATELY, REMOVE THIS LINE
send_email()


#Schedule to send every minute, hour or day
# schedule.every(2).day.do(send_email)
# schedule.every(5).minute.do(send_email)
# schedule.every(1).hour.do(send_email)

while True:
    schedule.run_pending()
    time.sleep(1)

