import os
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import smtplib
import time

def send_bulk_emails(csv_file, sender_email, sender_password, subject, html_body, plain_body):
    failed_emails = []  # To track failed emails
    sent_count = 0

    try:
        # Read recipient emails from CSV
        data = pd.read_csv(csv_file)
        if 'email' not in data.columns:
            print("Error: The CSV file must have a column named 'email'.")
            return

        recipient_emails = data['email'].dropna().tolist()

        # SMTP setup
        smtp_server = 'mail.ninjapatchesllc.com'
        smtp_port = 465
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, sender_password)

        # Process each recipient
        for recipient_email in recipient_emails:
            try:
                # Build the email
                msg = MIMEMultipart("alternative")
                msg['From'] = sender_email
                msg['To'] = recipient_email
                msg['Subject'] = subject
                msg['Date'] = formatdate(localtime=True)  # Add Date header

                # Attach plain-text and HTML versions
                msg.attach(MIMEText(plain_body, 'plain'))
                msg.attach(MIMEText(html_body, 'html'))

                # Send email
                server.sendmail(sender_email, recipient_email, msg.as_string())
                print(f"Email sent to {recipient_email}")
                sent_count += 1

                # Delay between emails to avoid spam filters
                time.sleep(2)

            except smtplib.SMTPException as e:
                print(f"Failed to send email to {recipient_email}: {e}")
                failed_emails.append({"email": recipient_email, "error": str(e)})

        # Log failed emails
        if failed_emails:
            failed_df = pd.DataFrame(failed_emails)
            failed_df.to_csv("failed_emails.csv", index=False)
            print("Logged failed emails to failed_emails.csv")

        print(f"\nSummary: Sent {sent_count}, Failed {len(failed_emails)}")

        server.quit()

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
csv_file_path = 'test_emails.csv'
your_email = 'deals@ninjapatchesllc.com'
your_password = '%(d2@67F232d'
email_subject = "Custom Patches for Your Brand, Delivered Fast!"
email_html = """\
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <p>Hi,</p>
    <p>Looking for premium-quality custom patches? Ninja Patches LLC specializes in crafting patches tailored to your needs.</p>
    <p><a href="https://ninjapatchesllc.com" style="color: #1a73e8; text-decoration: none;">Visit our website</a> to explore our options or <a href="https://wa.me/12138143526?text=Hi!%20I%20would%20like%20to%20know%20more%20about%20custom%20patches." style="color: #1a73e8; text-decoration: none;">chat with us on WhatsApp</a>.</p>
    <p>Warm regards,<br>The Ninja Patches Team</p>
</body>
</html>
"""
email_plain = """\
Hi,

Looking for premium-quality custom patches? Ninja Patches LLC specializes in crafting patches tailored to your needs.

Visit our website: https://ninjapatchesllc.com
Chat with us on WhatsApp: https://wa.me/12138143526

Warm regards,
The Ninja Patches Team
"""

send_bulk_emails(csv_file_path, your_email, your_password, email_subject, email_html, email_plain)
