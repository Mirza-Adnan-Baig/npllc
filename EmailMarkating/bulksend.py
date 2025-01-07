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

# Example usage 1 to 400
csv_file_path = 'batches/emails_1_to_400.csv'
your_email = 'deals@ninjapatchesllc.com'
your_password = '|wm)$4n1%f#1'
email_subject = "Kick Off the New Year with 30% Off – Custom Patches Delivered in 5 Days!"
email_html = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ninja Patches New Year Offer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: #333;
        }
        .email-container {
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            background: #f9f9f9;
            padding: 20px;
            border: 1px solid #ddd;
        }
        .header {
            text-align: center;
            background: #fcb116;
            color: white;
            padding: 20px 0;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .body {
            padding: 20px;
        }
        .body h2 {
            color: #fcb116;
            font-size: 20px;
        }
        .body ul {
            list-style: none;
            padding: 0;
        }
        .body ul li {
            margin-bottom: 10px;
        }
        .cta {
            text-align: center;
            margin: 20px 0;
        }
        .cta a {
            display: inline-block;
            background: #fcb116;
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 5px;
        }
        .cta a:hover {
            background: #0056b3;
        }
        .footer {
            text-align: center;
            font-size: 12px;
            color: #666;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>Start 2025 in Style – High-Quality Custom Patches at 30% Off!</h1>
        </div>
        <div class="body">
            
            <p>Happy New Year from Ninja Patches! We're ringing in 2025 with an exclusive <strong>30% discount</strong> on all custom patches. Whether you're refreshing your brand, gearing up your team, or celebrating a special event, our precision-crafted patches are designed to impress.</p>
            <h2>Why Choose Ninja Patches?</h2>
            <ul>
                <li>✨ <strong>Unmatched Quality</strong> – State-of-the-art machinery ensures patches that stand out and last.</li>
                <li>⚡ <strong>Fastest Delivery</strong> – Get your patches within 5 business days—ideal for quick turnarounds.</li>
                <li>💯 <strong>Satisfaction Guaranteed</strong> – Late delivery or production errors? We’ll refund you in full.</li>
            </ul>
            <h2>Explore Our Custom Patch Options</h2>
            <ul>
                <li>Embroidered Patches</li>
                <li>Leather Patches</li>
                <li>Printed Patches</li>
                <li>PVC Patches</li>
                <li>Military Patches</li>
                <li>Woven Patches</li>
                <li>Flag Patches</li>
                <li>Biker Patches</li>
                <li>University Patches</li>
                <li>Chenille Patches</li>
                <li>Felt Patches</li>
            </ul>
            <p><strong>Backings include:</strong> Iron-On, Tape, Velcro, Sew-On, and more. Need borders? Select from Hot-Cut or Merrowed to match your design needs.</p>
            <h2>How to Order</h2>
            <ol>
                <li>Send us your artwork</li>
                <li>Specify size and quantity.</li>
                <li>We take care of the rest!</li>
            </ol>
            <h2>Contact Us Today</h2>
            <p>🌐 <a href="https://ninjapatchesllc.com">Website</a>: ninjapatchesllc.com</p>
            <p>📧 <strong>Orders & Queries:</strong> <a href="mailto:sales@ninjapatchesllc.com">sales@ninjapatchesllc.com</a></p>
            <p>📧 <strong>Support & Compliance:</strong> <a href="mailto:info@ninjapatchesllc.com">info@ninjapatchesllc.com</a></p>
        </div>
        <div class="footer">
            🎉 Don’t miss out—this New Year offer is available for a limited time. Start 2025 with custom patches that leave a lasting impression!  
        </div>
    </div>
</body>
</html>

"""

email_plain = """\
Start 2025 in Style – High-Quality Custom Patches at 30% Off!

Happy New Year from Ninja Patches! We're ringing in 2025 with an exclusive 30% discount on all custom patches. Whether you're refreshing your brand, gearing up your team, or celebrating a special event, our precision-crafted patches are designed to impress.

Why Choose Ninja Patches?
✨ Unmatched Quality – State-of-the-art machinery ensures patches that stand out and last.
⚡ Fastest Delivery – Get your patches within 5 business days—ideal for quick turnarounds.
💯 Satisfaction Guaranteed – Late delivery or production errors? We’ll refund you in full.

Explore Our Custom Patch Options
Choose from a wide range of custom patches, including:

Embroidered Patches
Leather Patches
Printed Patches
PVC Patches
Military Patches
Woven Patches
Flag Patches
Biker Patches
University Patches
Chenille Patches
Felt Patches
Backings include Iron-On, Tape, Velcro, Sew-On, and more. Need borders? Select from Hot-Cut or Merrowed to match your design needs.

How to Order
It’s quick and easy:

Send us your artwork
Specify size and quantity.
We take care of the rest!
Contact Us Today
🌐 Website: ninjapatchesllc.com
📧 Orders & Queries: sales@ninjapatchesllc.com
📧 Support & Compliance:info@ninjapatchesllc.com

🎉 Don’t miss out—this New Year offer is available for a limited time. Start 2025 with custom patches that leave a lasting impression!

Warm wishes,
The Ninja Patches Team
"""

send_bulk_emails(csv_file_path, your_email, your_password, email_subject, email_html, email_plain)
