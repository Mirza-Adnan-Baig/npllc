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

# Example usage Working on new ASI sheet
csv_file_path = '../Email_filter_script/email_filter/Syscom_Data_Sheet_ASI_Split/emails_1201_to_1600.csv'
your_email = 'deals@ninjapatchesllc.com'
your_password = 'nA;):2v@hv32'
email_subject = "Exclusive Offer for ASI Members – Personalized Service + Discount Inside!"
email_html = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Custom Patches and Digitizing – 10% Off</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      color: #333333;
      background-color: #ffffff;
      line-height: 1.6;
      padding: 20px;
    }
    .cta a {
      display: inline-block;
      background-color: #1a73e8;
      color: #ffffff;
      padding: 12px 24px;
      text-decoration: none;
      border-radius: 5px;
      margin-top: 20px;
      font-weight: bold;
    }
    .footer {
      margin-top: 40px;
      font-size: 12px;
      color: #888888;
    }
    .footer a {
      color: #888888;
      text-decoration: underline;
    }
  </style>
</head>
<body>

  <p>Hello,</p>

  <p>I hope this message finds you well. My name is <strong>Mirza Adnan Baig</strong>, from <strong>Ninja Patches LLC</strong> and <strong>Distro Digitizing</strong>, and a proud ASI member (ASI #49932). I specialize in helping businesses like yours stand out with high-quality custom patches and expert digitizing services tailored for promotional products, apparel, and more.</p>

  <p>Whether you're a brand looking to elevate your merchandise or need precise digitizing for your designs—we're here to deliver fast, reliable, and affordable service.</p>

  <h3 style="color: #1a73e8;">What We Offer:</h3>

  <p><strong><a href="https://ninjapatchesllc.com" style="color: #1a73e8;">Ninja Patches LLC</a></strong></p>
  <ul>
    <li>Embroidered, PVC, Leather, Woven, Chenille, and Custom Patches</li>
    <li>Multiple backings: Iron-On, Velcro, Sew-On & more</li>
    <li>Delivery in 5 business days</li>
    <li>100% Satisfaction Guarantee</li>
  </ul>

  <p><strong><a href="https://distrodigitizing.com" style="color: #1a73e8;">Distro Digitizing</a></strong></p>
  <ul>
    <li>High-quality digitizing for embroidery</li>
    <li>Vector conversions</li>
    <li>Fast turnaround & expert support</li>
    <li>Ideal for apparel decorators and promo shops</li>
  </ul>

  <p style="background-color: #f0f8ff; padding: 10px; border-left: 4px solid #1a73e8;">
    🎉 <strong>Get 10% Off Your First Order!</strong><br>
    Use reference code <strong>MAB10</strong> when you reply or mention it in your email to receive <strong>10% off</strong>.
  </p>

  <p><strong>💬 Our pricing is flexible and open to negotiation — we’ll work with your budget!</strong></p>

  <p>Let’s discuss your project! You can reply to this email or contact our teams:</p>
  <ul>
    <li><a href="mailto:sales@ninjapatchesllc.com">sales@ninjapatchesllc.com</a></li>
    <li><a href="mailto:sales@distrodigitizing.com">sales@distrodigitizing.com</a></li>
    <li>📞 Phone: <a href="tel:+12133701437">+1 213 370 1437</a></li>
  </ul>
  
  <p>Best regards,<br>
  <strong>Mirza Adnan Baig</strong><br>
  Co Founder – Ninja Patches LLC & Distro Digitizing<br>
  ASI #49932<br>

  <!-- CTA Button -->
  <div class="cta">
    <a href="https://ninjapatchesllc.com/quote/?utm_source=email&utm_medium=newsletter&utm_campaign=10percent_discount">Order Now & Save 10%</a>
  </div>

  <!-- Footer -->
  <div class="footer">
    <p>26429 Whisper Mill Circle, Santa Clarita, California, 91350</p>
    <p><a href="https://ninjapatchesllc.com/unsubscribe">Unsubscribe</a></p>
  </div>
</body>
</html>


"""

email_plain = """\

Exclusive Offer for ASI Members – Personalized Service + Discount Inside!

Hello,

I hope this message finds you well. My name is Mirza Adnan Baig, from Ninja Patches LLC and Distro Digitizing, and a proud ASI member (ASI #49932). I specialize in helping businesses like yours stand out with high-quality custom patches and expert digitizing services tailored for promotional products, apparel, and more.

Whether you're a brand looking to elevate your merchandise or need precise digitizing for your designs—we're here to deliver fast, reliable, and affordable service.

What We Offer:
Ninja Patches LLC

Embroidered, PVC, Leather, Woven, Chenille, and Custom Patches
Multiple backings: Iron-On, Velcro, Sew-On & more
Delivery in 5 business days
100% Satisfaction Guarantee
Distro Digitizing

High-quality digitizing for embroidery
Vector conversions
Fast turnaround & expert support
Ideal for apparel decorators and promo shops
🎉 Get 10% Off Your First Order!
Use reference code MAB10 when you reply or mention it in your email to receive 10% off.

💬 Our pricing is flexible and open to negotiation — we’ll work with your budget!

Let’s discuss your project! You can reply to this email or contact our teams:

sales@ninjapatchesllc.com
sales@distrodigitizing.com
📞 Phone: +1 213 370 1437
Best regards,
Mirza Adnan Baig
Co Founder – Ninja Patches LLC & Distro Digitizing
ASI #49932

Order Now & Save 10%

26429 Whisper Mill Circle, Santa Clarita, California, 91350

Unsubscribe

"""

send_bulk_emails(csv_file_path, your_email, your_password, email_subject, email_html, email_plain)
