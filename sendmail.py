import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from maps import near_by_hospitals
from firebase_ import getmail,setbool,getdata

sender_email = "tarungopineni@gmail.com"
sender_password = "zvgz tmkp bttg cxib"
loc = (17.385044, 78.486671)
data = getdata("MH43CC1745")
mobile = data[0]
name = data[1]
def send_frame_via_email(frame, loc, subject=f"Accident detected at {loc},driver name:{name},mobile number:{mobile}"):
    success, encoded_img = cv2.imencode(".jpg", frame)
    if not success:
        raise ValueError("Could not encode frame as JPG")
    jpg_bytes = encoded_img.tobytes()
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    try:
        nodes = near_by_hospitals(loc)
        for node in nodes[:2]:
            name = node.tags.get("name", "Unnamed Hospital")
            print(name)
            setbool(name)
            mails = getmail(name)
            for mail in mails:
                msg = MIMEMultipart()
                msg["From"] = sender_email
                msg["To"] = mail
                msg["Subject"] = subject
                msg.attach(MIMEText(f"Hospital: {name}\nAttached frame.", "plain"))

                part = MIMEBase("application", "octet-stream")
                part.set_payload(jpg_bytes)
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", 'attachment; filename="frame.jpg"')
                msg.attach(part)
                server.sendmail(sender_email, mail, msg.as_string())
    except:
        msg = MIMEMultipart()
        receiver_email = "tarungopineni@gmail.com"
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Test Email from Python"
        body = f"accident detected at {loc}"
        msg.attach(MIMEText(body, 'plain'))
        server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    return True
