import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from confluent_kafka import Consumer

# Configurazione del consumer Kafka
consumer_config = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'email-notification-group',
    'auto.offset.reset': 'earliest'
}

# Configurazione SMTP per inviare email
SMTP_SERVER = 'smtp.gmail.com'  # Ad esempio, server SMTP di Gmail
SMTP_PORT = 587
SMTP_USERNAME = 'hw2.giu.sofi@gmail.com'  # Inserire l'email del mittente
SMTP_PASSWORD = '8volteAA'  # Inserire la password del mittente (o app-specific password)

# Creazione del consumer Kafka
consumer = Consumer(consumer_config)

# Sottoscrizione al topic di input
topic = 'to-notifier'
consumer.subscribe([topic])

# Funzione per inviare email
def send_email(to_email, subject, body):
    try:
        # Creazione dell'email
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connessione al server SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Avvia TLS per una connessione sicura
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, to_email, msg.as_string())

        print(f"Email inviata con successo a {to_email}")
    except Exception as e:
        print(f"Errore durante l'invio dell'email a {to_email}: {e}")

# Ciclo principale per consumare messaggi
while True:
    # Poll per ricevere nuovi messaggi
    msg = consumer.poll(1.0)
    if msg is None:
        continue  # Nessun messaggio ricevuto
    if msg.error():
        print(f"Errore del consumer: {msg.error()}")
        continue

    try:
        # Parsing del messaggio ricevuto
        data = json.loads(msg.value().decode('utf-8'))
        print(f"Messaggio ricevuto: {data}")

        # Estrazione dei parametri dal messaggio
        email = data.get('email')
        ticker = data.get('ticker')
        condition = data.get('condition')

        if not email or not ticker or not condition:
            print("Messaggio non valido, mancano campi obbligatori")
            continue

        # Creazione dei contenuti dell'email
        subject = f"Ticker Alert: {ticker}"
        body = f"La condizione di superamento soglia per il ticker '{ticker}' è stata soddisfatta:\n\n{condition}"

        # Invio dell'email
        send_email(email, subject, body)

    except Exception as e:
        print(f"Errore durante l'elaborazione del messaggio: {e}")

# Chiudi il consumer quando il processo termina
consumer.close()
