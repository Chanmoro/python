# Test mail send sample.
import smtplib
import email.utils
from email.mime.text import MIMEText

mailTo = 'test_to@example.com'
mailFrom = 'test_from@example.com'

mail = MIMEText('This is the body of the test message.')
mail['To'] = mailTo
mail['From'] = mailFrom
mail['Subject'] = 'Test message'

server = smtplib.SMTP('localhost', 8025)
server.set_debuglevel(True)
try:
    server.sendmail(mailTo , [mailFrom], mail.as_string())
finally:
    server.quit()