import smtplib
from email.mime.text import MIMEText
from email.header import Header
def send_mail(name, mailText, encode):
    charset = encode
    msg = MIMEText(mailText, 'plain')
    #msg = MIMEText(mailText, 'plain', charset)
    msg['Subject'] = Header(subject.encode(charset), charset)
    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.login(gmail, password)
    smtp_obj.sendmail(gmail, mail, msg.as_string())
    smtp_obj.quit()
