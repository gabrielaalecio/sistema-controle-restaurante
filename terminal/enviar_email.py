import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def enviar_email(destinatario, assunto, corpo, anexo=None):
    remetente = "bugdosabor@gmail.com"
    senha = "dobn vywt sqaw juuk"  

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "html"))

    # Verifica se o anexo existe e o adiciona ao e-mail
    if anexo and os.path.exists(anexo):
        with open(anexo, "rb") as f:
            parte_anexo = MIMEApplication(f.read(), _subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        parte_anexo.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(anexo)}"')
        msg.attach(parte_anexo)

    try:
        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as server:
            server.login(remetente, senha)
            server.sendmail(remetente, destinatario, msg.as_string())
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False