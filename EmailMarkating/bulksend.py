import os
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
#import time
def send_bulk_emails(csv_file, sender_email, sender_password, subject, message_body):
    failed_emails = []  # List to store failed email addresses
    sent_count = 0  # Counter for successfully sent emails

    # Define the directory for failed emails
    failed_emails_dir = "Failed Emails"
    os.makedirs(failed_emails_dir, exist_ok=True)  # Create the folder if it doesn't exist

    # Generate the failed log file name dynamically based on the input file name
    file_base_name = os.path.splitext(os.path.basename(csv_file))[0]
    failed_log_file = os.path.join(failed_emails_dir, f"{file_base_name}_failed.csv")

    try:
        # Read the CSV file using the csv_file parameter
        data = pd.read_csv(csv_file)  # Use the parameter to load the file
        if 'email' not in data.columns:
            print("Error: The CSV file must have a column named 'email'.")
            return

        recipient_emails = data['email'].dropna().tolist()  # Extract email addresses

        # Setup the SMTP server
        smtp_server = 'mail.ninjapatchesllc.com'  # Replace with your SiteGround domain's mail server
        smtp_port = 465  # Use SSL for SiteGround

        # Establish connection with SMTP server
        try:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            server.login(sender_email, sender_password)
        except smtplib.SMTPException as e:
            print(f"Failed to connect to SMTP server: {e}")
            return

        # Loop through recipient emails
        for recipient_email in recipient_emails:
            try:
                # Create the email
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient_email
                msg['Subject'] = subject
                msg.attach(MIMEText(message_body, 'html'))

                # Send the email
                server.sendmail(sender_email, recipient_email, msg.as_string())
                print(f"Email sent to {recipient_email}")
                sent_count += 1  # Increment sent count

                # Introduce a delay to avoid spam detection
                #time.sleep(2)

            except smtplib.SMTPException as e:
                print(f"Failed to send email to {recipient_email}: {e}")
                failed_emails.append({"email": recipient_email, "error": str(e)})  # Log the failed email
                continue  # Skip to the next recipient

        # Save failed emails to a CSV file
        if failed_emails:
            failed_df = pd.DataFrame(failed_emails)
            failed_df.to_csv(failed_log_file, index=False)
            print(f"Failed emails have been saved to {failed_log_file}")

        # Print summary
        print("\nSummary:")
        print(f"Total Emails Sent: {sent_count}")
        print(f"Total Emails Failed: {len(failed_emails)}")

        # Close the SMTP server connection
        server.quit()
        print("All emails processed!")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage: use ../ for file batch First Run ASI
csv_file_path = ('../Email_filter_script/email_filter/split_emails/emails_801_to_1200.csv.csv')  # run 801 to 1200 The path to your CSV file
your_email = 'sales@ninjapatchesllc.com'  # Replace with your SiteGround email
your_password = '4(#sf%522m1o'  # Replace with your SiteGround email password
email_subject = 'Flat 30% Off This Christmas – Custom Patches Delivered in 5 Days!'
email_message = """\
<html>
<!-- Header -->
    <h2 style="text-align: center; color: #fcb116;">Celebrate the Holidays with High-Quality Custom Patches – Fastest Delivery Guaranteed!</h2>
    
    <!-- Body -->
    <p>Happy Holidays from Ninja Patches! This Christmas, we’re offering an exclusive <strong>30% flat discount</strong> on our high-quality custom patches. Whether for your brand, team, or a special event, our patches are crafted to stand out with precision and style.</p>
    
    <!-- Why Choose Ninja Patches -->
    <h3 style="color: #fcb116;">Why Choose Ninja Patches?</h3>
    <ul>
        <li><strong>Unmatched Quality:</strong> We use state-of-the-art machinery to produce patches trusted by customers worldwide.</li>
        <li><strong>Fastest Delivery:</strong> Receive your patches in just <strong>5 business days</strong>—perfect for last-minute orders.</li>
        <li><strong>Satisfaction Guaranteed:</strong> If we don’t deliver on time or if there’s an error on our end, you’ll get a full refund—no questions asked!</li>
    </ul>
    
    <!-- Explore Our Custom Patch Options -->
    <h3 style="color: #fcb116;">Explore Our Custom Patch Options</h3>
    <p>We create a wide variety of patches to suit your needs:</p>
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
    <p>Plus, choose from flexible backing options such as <strong>Iron-On, Tape, Velcro, Sew-On</strong>, and more. Need borders? We offer <strong>Hot-Cut</strong> and <strong>Merrowed</strong> styles tailored to your requirements.</p>
    
    <!-- How to Order -->
    <h3 style="color: #fcb116;">How to Order</h3>
    <p>It’s simple:</p>
    <ol>
        <li>Send us your artwork.</li>
        <li>Specify the size and quantity.</li>
        <li>We’ll handle the rest!</li>
    </ol>
    
<!-- Contact Us -->
    <h3 style="color: #fcb116;">Contact Us Today</h3>
    <p>🌐 <a href="https://ninjapatchesllc.com" style="text-decoration: none;"><strong style="color: #000000">Website:</strong> <strong style="color: #004589;">ninjapatchesllc.com</strong></a></p>
    
    <p>📧 <a href="mailto:sales@ninjapatchesllc.com" style="color: #fcb116; text-decoration: none;"><strong style="color: #000000">Orders & Queries: </strong> <strong style="color: #004589;"> sales@ninjapatchesllc.com</strong></a></p>
    
    <p>📧 <a href="mailto:info@ninjapatchesllc.com" style="color: #fcb116; text-decoration: none;"><strong style="color: #000000">Support & Compliance: </strong> <strong style="color: #004589;"> info@ninjapatchesllc.com</strong></a></p>
    
    <p>📞 <a href="tel:+12138143526" style="color: #fcb116; text-decoration: none;"><strong style="color: #000000">Feel free to give us a call: </strong> <strong style="color: #004589;"> +1 (213) 814-3526</strong></a></p>
    
   	<p>🟢 <a href="https://wa.me/12138143526?text=Hello%20Ninja%20Patches%20Team!" target="_blank" style="color: #fcb116; text-decoration: none;"><strong style="color: #000000">Chat with us on WhatsApp:</strong> <strong style="color: #004589;"> +1 (213) 814-3526</strong></a></p>
     
    <p style="color: #000000; text-decoration: none;">📧<strong> Or just simply reply to this email</strong> </p>

    <p>🎄 Don’t wait—this exclusive Christmas offer is only available for a limited time. Order now and make your custom patches unforgettable this holiday season!</p>
    
    <!-- Closing -->
    
    <p>Warm regards,<br><strong>The Ninja Patches Team</strong></p>
    <p>If you no longer wish to receive these emails, <a href="https://ninjapatchesllc.com/unsubscribe/" style="color: red;">unsubscribe here</a>.</p>
    
</body>
</html>
"""

# Call the function and pass the CSV file
send_bulk_emails(csv_file_path, your_email, your_password, email_subject, email_message)
