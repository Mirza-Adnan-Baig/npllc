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

# Example usage 801 to 1200
csv_file_path = '../Email_filter_script/email_filter/Ninja_Email_Sheets_180325_Split/emails_601_to_800.csv'
your_email = 'deals@ninjapatchesllc.com'
your_password = 'nA;):2v@hv32'
email_subject = "Limited Time: 10% Off Custom Patches – Order Now!"
email_html = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Get 10% Off – Custom Patches Designed Just for You!</title>
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
            color: #060e25;
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
            color: #007bff;
            font-size: 20px;
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
            color: #060e25;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 5px;
        }
        .cta a:hover {
            background: #b1b5b1;
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
            <h1>Get 10% Off – Custom Patches Designed Just for You!</h1>
        </div>
        <div class="body">
            <h2>High-Quality Custom Patches – Now with a 10% Discount!</h2>
            <p>High-quality custom patches – now at <strong>10% off</strong>! Whether for your brand, team, or a special project, we deliver patches that stand out.</p>
            <h2>Why Choose Ninja Patches?</h2>
            <ul>
                <li>✔ <strong>10% Off Your Order</strong> – Get top-quality patches at a special price.</li>
                <li>⚡ <strong>Rush Orders</strong> – Receive your patches in just 5 business days.</li>
                <li>💯 <strong>Satisfaction Guaranteed</strong> – Full refund if we don’t meet our promise.</li>
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
            <p><strong>Backings include:</strong> Iron-On, Velcro, Sew-On, Tape, and more!</p>
            <h2>How to Claim Your 10% Discount:</h2>
            <ol>
                <li>Send us your artwork & requirements.</li>
                <li>Use code <strong>SAVE10</strong> mention it in your email.</li>
                <li>We take care of the rest!</li>
            </ol>
            <h2>Contact Us Today</h2>
            <p>🌐 <a href="https://ninjapatchesllc.com/?utm_source=email&utm_medium=newsletter&utm_campaign=10percent_discount">Website</a> www.ninjapatchesllc.com</p>
            <p>📧 <strong>Orders & Queries:</strong> <a href="mailto:sales@ninjapatchesllc.com">sales@ninjapatchesllc.com</a></p>
            <p>📧 <strong>Support & Compliance:</strong> <a href="mailto:info@ninjapatchesllc.com">info@ninjapatchesllc.com</a></p>
            <p>📞 <strong>Phone:</strong> +1 (213) 814-3526</p>
        </div>
        <div class="cta">
            <a href="https://ninjapatchesllc.com/quote/?utm_source=email&utm_medium=newsletter&utm_campaign=10percent_discount">Order Now & Save 10%</a>
        </div>
        <div class="footer">
            <p>1005 Mount Olive Dr-5 Duarte M, CA 91010, USA</p>
            <p><a href="https://ninjapatchesllc.com/unsubscribe">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>

"""

email_plain = """\

High-Quality Custom Patches – Now with a 10% Discount!

High-quality custom patches – now at 10% off! Whether for your brand, team, or a special project, we deliver patches that stand out.

Why Choose Ninja Patches?
✔ 10% Off Your Order – Get top-quality patches at a special price.
⚡ Fastest Delivery – Receive your patches in just 5 business days.
💯 Satisfaction Guaranteed – Full refund if we don’t meet our promise.

Explore Our Custom Patch Options:
- Embroidered Patches
- Leather Patches
- Printed Patches
- PVC Patches
- Military Patches
- Woven Patches
- Flag Patches
- Biker Patches
- University Patches
- Chenille Patches
- Felt Patches

Backings include: Iron-On, Velcro, Sew-On, Tape, and more!

How to Claim Your 10% Discount:
1. Send us your artwork & requirements.
2. Use code SAVE10 at checkout or mention it in your email.
3. We take care of the rest!

Contact Us Today:
🌐 Website: https://ninjapatchesllc.com/?utm_source=email&utm_medium=newsletter&utm_campaign=10percent_discount
📧 Orders & Queries: sales@ninjapatchesllc.com
📧 Support & Compliance: info@ninjapatchesllc.com
📞 Phone: +1 (213) 814-3526

Order Now: https://ninjapatchesllc.com/?utm_source=email&utm_medium=newsletter&utm_campaign=10percent_discount

1005 Mount Olive Dr-5 Duarte M, CA 91010, USA
Unsubscribe: https://ninjapatchesllc.com/unsubscribe

This special 10% discount is only available for a limited time. Don’t miss out – place your order today!

"""

send_bulk_emails(csv_file_path, your_email, your_password, email_subject, email_html, email_plain)
