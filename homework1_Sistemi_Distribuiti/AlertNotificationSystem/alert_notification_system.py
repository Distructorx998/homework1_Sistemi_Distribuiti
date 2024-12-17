import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from confluent_kafka import Consumer, KafkaException, KafkaError
import time
import logging

# Configurazione dei log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configurazione del consumer Kafka
consumer_config = {
    'bootstrap.servers': 'kafka-broker-1:19092,kafka-broker-2:29092,kafka-broker-3:39092',  # List of Kafka brokers
    'group.id': 'detailed-consumer-group',  # Consumer group ID
    'auto.offset.reset': 'earliest',  # Start reading from the earliest offset if no committed offset is available
    'enable.auto.commit': True  # Enable automatic offset commits
}

# Configurazione SMTP per inviare email
SMTP_SERVER = 'smtp.gmail.com'  # Ad esempio, server SMTP di Gmail
SMTP_PORT = 587
SMTP_USERNAME = 'distructorx@gmail.com'  # Inserire l'email del mittente
SMTP_PASSWORD = 'tlkaetutxjeahlyu'  # Inserire la password del mittente (o app-specific password)

# Nome del topic da verificare e sottoscrivere
topic = 'to-notifier'

# Funzione per verificare la disponibilità di Kafka e del topic
def wait_for_kafka(bootstrap_servers, topic, timeout=60):
    """Aspetta che Kafka sia pronto e che il topic esista."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            consumer = Consumer({'bootstrap.servers': bootstrap_servers, 'group.id': 'health-check'})
            metadata = consumer.list_topics(timeout=5.0)
            if topic in metadata.topics:
                logging.info(f"Kafka è pronto e il topic '{topic}' esiste.")
                consumer.close()
                return True
            else:
                logging.warning(f"Topic '{topic}' non trovato. Riprovo...")
        except KafkaException as e:
            logging.error(f"Errore durante la verifica di Kafka: {e}")
        time.sleep(5)
    raise RuntimeError(f"Kafka non è pronto o il topic '{topic}' non esiste entro il tempo massimo.")

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

        logging.info(f"Email inviata con successo a {to_email}")
    except Exception as e:
        logging.error(f"Errore durante l'invio dell'email a {to_email}: {e}")

# Verifica Kafka
logging.info("Verificando la disponibilità di Kafka...")
wait_for_kafka(consumer_config['bootstrap.servers'], topic)

# Creazione del consumer Kafka
consumer = Consumer(consumer_config)
logging.info(f"Sottoscrizione al topic '{topic}'...")
consumer.subscribe([topic])

# Ciclo principale per consumare messaggi
logging.info("Inizio del ciclo principale per consumare i messaggi...")
while True:
    # Poll per ricevere nuovi messaggi
    msg = consumer.poll(1.0)
    if msg is None:
        continue  # Nessun messaggio ricevuto
    if msg.error():
        logging.error(f"Errore del consumer: {msg.error()}")
        continue

    try:
        # Parsing del messaggio ricevuto
        data = json.loads(msg.value().decode('utf-8'))
        logging.info(f"Messaggio ricevuto: {data}")

        # Estrazione dei parametri dal messaggio
        email = data.get('email')
        ticker = data.get('ticker')
        condition = data.get('condition')

        if not email or not ticker or not condition:
            logging.warning("Messaggio non valido, mancano campi obbligatori")
            continue

        # Creazione dei contenuti dell'email
        subject = f"Ticker Alert: {ticker}"
        body = f"La condizione di superamento soglia per il ticker '{ticker}' è stata soddisfatta:\n\n{condition}"

        # Invio dell'email
        send_email(email, subject, body)

    except Exception as e:
        logging.error(f"Errore durante l'elaborazione del messaggio: {e}")

# Chiudi il consumer quando il processo termina
consumer.close()
logging.info("Consumer chiuso.")
