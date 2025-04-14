from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import os

from repositories.SettingRepository import SettingRepository
from constants import mail, settings, messages
from logger.logger import log, MAIL
from config import Config

settingRepository = SettingRepository()

def sendMail():
    fromAdress = settingRepository.getValue('FromAdress')
    toAdress = settingRepository.getValue('ToAdress')
    if fromAdress == None:
        log.error(MAIL, messages.ERROR_FETCHING_FROM_ADRESS)
        return None
    if toAdress == None:
        log.error(MAIL, messages.ERROR_FETCHING_TO_ADRESS)
        return None
    message = MIMEMultipart()
    message['From'] = fromAdress.value
    message['To'] = toAdress.value
    message['Subject'] = mail.SUBJECT
    message.attach(MIMEText(mail.BODY, 'plain'))
    attachmentPath = settings.WORD_PATH + settings.FINAL_WORD_FILENAME
    filename = os.path.basename(attachmentPath)
    with open(attachmentPath, 'rb') as attachment :
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={filename}')
    message.attach(part)
    try:
        with smtplib.SMTP_SSL(mail.SMTP, mail.PORT) as server:
            server.login(fromAdress.value, Config.MAIL_PASSWORD)
            server.send_message(message)
        log.info(MAIL, messages.MAIL_SENT.replace("TO_ADRESS", toAdress.value))
        return toAdress.value
    except Exception as _:
        return None
    