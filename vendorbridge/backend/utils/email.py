import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os

async def send_invoice_email(to_email: str, invoice_number: str, pdf_path: str):
    msg = MIMEMultipart()
    msg["From"] = os.getenv("MAIL_FROM")
    msg["To"] = to_email
    msg["Subject"] = f"Invoice {invoice_number} from VendorBridge"

    msg.attach(MIMEText(f"Please find attached invoice {invoice_number}.", "plain"))

    with open(pdf_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={invoice_number}.pdf")
    msg.attach(part)

    with smtplib.SMTP_SSL(os.getenv("MAIL_SERVER"), 465) as server:
        server.login(os.getenv("MAIL_USERNAME"), os.getenv("MAIL_PASSWORD"))
        server.sendmail(os.getenv("MAIL_FROM"), to_email, msg.as_string())