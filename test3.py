SMTPserver = 'smtp.gmail.com'
sender =     'joseph.huang@gmail.com'
destination = ['']

USERNAME = ""
PASSWORD = ""

# typical values for text_subtype are plain, html, xml
text_subtype = 'plain'


content="""\
Test message
"""

subject="Sent from Python"

import sys
import os
import re

from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
# from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)

# old version
# from email.MIMEText import MIMEText
from email.mime.text import MIMEText

msg = MIMEText(content, text_subtype)
msg['Subject']=       'hello'
msg['From']   = sender # some SMTP servers will do this automatically, not all

conn = SMTP(SMTPserver)
conn.set_debuglevel(False)
conn.login(USERNAME, PASSWORD)
try:
    conn.sendmail(sender, destination, msg.as_string())
finally:
    conn.quit()
