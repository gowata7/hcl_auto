import os
import glob
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
from pathlib import Path
from string import Template

# 이미지 폴더 지정
screenshots_path = 'ScreenShots'

# 이미지 폴더 존재 유무 체크 (필요 시 생성)
isExist = os.path.exists(screenshots_path)
if not isExist:
    os.makedirs(screenshots_path)
    print("The new directory is created!")

# 리포트 폴더 지정
pdf_path = 'Reports'
# 리포트 폴더 존재 유무 체크 (필요 시 생성)
# to_email = "C:\work\jinhong\Mail\test.txt"
# to_email1 = "C:\work\jinhong\Mail\mailcontent_RU.txt"
    
isExist = os.path.exists(pdf_path)
if not isExist:
    os.makedirs(pdf_path)
    print("The new directory is created!")

# 이메일 발신처
MY_ADDRESS = '9458131@ict-companion.com'
PASSWORD = 'Dlstod97@'

# 이메일 수신처
def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """
    
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

# 이메일 바디 Template
def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

# 이메일 발신
def send_email(region):
    Sent = False
    
    if region == "KR":

        while not Sent:
            try:    
                names, emails = get_contacts('Mail/to_email.txt') # read contacts
                message_template = read_template('Mail/mailcontent_KR.txt')

                # set up the SMTP server
                s = smtplib.SMTP(host='outlook.hyundai.net', port=25)  # 25 - smtp, 110 - pop3
                s.starttls()
                s.login(MY_ADDRESS, PASSWORD)

                filename_infra = glob.glob(os.path.join(pdf_path, '%sInfra_in_detail*.pdf' %(region)))[-1]
                filename_jennifer = glob.glob(os.path.join(pdf_path, 'JenniferInfra_in_detail*.pdf'))[-1]

                files = [
                    filename_infra,
                    filename_jennifer,
                ]     

                # For each contact, send the email:
                for name, email in zip(names, emails):
                    msg = MIMEMultipart()       # create a message

                    # email 제목
                    # title = f"추석연휴 내수 인프라/어플리케이션 주요 대시보드"
                    title = f"일일 내수 인프라/어플리케이션 주요 대시보드"
                    # email 바디
                    #message = message_template.substitute(current_time=datetime.now())
                    message = message_template.substitute(current_time=datetime.now().strftime('%Y-%m-%d %H:%M'))
                    # Prints out the message body for our sake
                    print(message)

                    # setup the parameters of the message
                    msg['From']=MY_ADDRESS
                    msg['To']=email
                    msg['Subject']=title
                    
                    # add in the message body
                    msg.attach(MIMEText(message, 'plain'))

                    # add attached files
                    try:
                        for path in files:
                            part = MIMEBase('application', 'octet-stream')
                            with open(path, 'rb') as file:
                                part.set_payload(file.read())
                            encoders.encode_base64(part)
                            part.add_header('Content-Disposition', 
                                            'attachment; filename={}'.format(Path(path).name))
                            msg.attach(part)                
                    except Exception as e:
                        f= open('SMTPchuseok.log', 'w')

                        print(e, file=f)
                        f.close
                        pass
                        
                    # send the message via the server set up earlier.
                    s.send_message(msg)
                    del msg
                # Terminate the SMTP session and close the connection
                s.quit()

                Sent = True

            except Exception as e:
                print(e)
                pass
    else :
        while not Sent:
            try:    
                #names, emails = get_contacts('receipients_%s.txt'%(region)) # read contacts
                names, emails = get_contacts('Mail/to_email.txt') # read contacts
                message_template = read_template('Mail/mailcontent_other.txt')

                # set up the SMTP server
                s = smtplib.SMTP(host='outlook.hyundai.net', port=25)  # 25 - smtp, 110 - pop3
                s.starttls()
                s.login(MY_ADDRESS, PASSWORD)

                filename_infra = glob.glob(os.path.join(pdf_path, '%sInfra_in_detail*.pdf' %(region)))[-1]
                

                files = [
                    filename_infra
                ]     

                # For each contact, send the email:
                for name, email in zip(names, emails):
                    msg = MIMEMultipart()       # create a message

                    # email 제목
                    # title = f"추석연휴 내수 인프라/어플리케이션 주요 대시보드"
                    title = f"일일 %s 인프라 주요 대시보드" % (region)
                    # email 바디
                    #message = message_template.substitute(current_time=datetime.now())
                    
                    message = message_template.substitute(current_time=datetime.now().strftime('%Y-%m-%d %H:%M'))
                    # Prints out the message body for our sake
                    print(message)

                    # setup the parameters of the message
                    msg['From']=MY_ADDRESS
                    msg['To']=email
                    msg['Subject']=title
                    
                    # add in the message body
                    msg.attach(MIMEText(message, 'plain'))

                    # add attached files
                    try:
                        for path in files:
                            part = MIMEBase('application', 'octet-stream')
                            with open(path, 'rb') as file:
                                part.set_payload(file.read())
                            encoders.encode_base64(part)
                            part.add_header('Content-Disposition', 
                                            'attachment; filename={}'.format(Path(path).name))
                            msg.attach(part)                
                    except Exception as e:
                        print(e)
                        pass
                        
                    # send the message via the server set up earlier.
                    s.send_message(msg)
                    del msg
                # Terminate the SMTP session and close the connection
                s.quit()

                Sent = True

            except Exception as e:
                print(e)
                pass                    
    
