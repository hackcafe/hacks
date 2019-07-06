def send_mail(USERNAME,PASSWORD,destination,msg_text,sender=None,subject="Test mail",attach_list=None):
    import smtplib 
    from email.mime.multipart import MIMEMultipart 
    from email.mime.text import MIMEText 
    from email.mime.base import MIMEBase 
    from email import encoders 

    fromaddr = USERNAME
    toaddr = destination
    msg = MIMEMultipart() 
    msg['From'] = fromaddr 
    msg['To'] = toaddr 
    msg['Subject'] = subject
    body = msg_text
    msg.attach(MIMEText(body, 'plain'))
    if attach_list is not None:
        for filename in attach_list:
            try:
                attachment = open(filename, "rb")
                p = MIMEBase('application', 'octet-stream') 
                p.set_payload((attachment).read()) 
                encoders.encode_base64(p) 
                p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
                msg.attach(p)
            except Exception as e:
                print("[-] Email Send Error:", e)
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(fromaddr, PASSWORD) 
    text = msg.as_string() 
    s.sendmail(fromaddr, toaddr, text) 
    s.quit() 