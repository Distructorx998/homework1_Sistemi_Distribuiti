import time
import mysql.connector
import logging
import json
from datetime import datetime
from confluent_kafka import Producer, Consumer

# Configurazione del consumer Kafka
consumer_config = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'group1',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True,
    'auto.commit.interval.ms': 5000
}

# Configurazione del producer Kafka
producer_config = {
    'bootstrap.servers': 'localhost:29092'
}

# Istanziazione di consumer e producer
consumer = Consumer(consumer_config)
producer = Producer(producer_config)

# Sottoscrizione al topic di input
topic1 = 'to-alert-system'
topic2 = 'to-notifier'
consumer.subscribe([topic1])

# Configurazione database MySQL
db_config = {
    'host': 'db',
    'user': 'user',
    'password': 'password',
    'database': 'users'
}

# Funzione per produrre messaggi Kafka
def produce_sync(producer, topic, value):
    try:
        producer.produce(topic, value)
        producer.flush()
        print(f"Produced message to {topic}: {value}")
    except Exception as e:
        print(f"Failed to produce message: {e}")

# Ciclo principale
while True:
    # Poll per ricevere nuovi messaggi
    msg = consumer.poll(1.0)
    if msg is None:
        continue  # Nessun messaggio ricevuto
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue
    
    try:
        # Parsing del messaggio ricevuto
        data = json.loads(msg.value().decode('utf-8'))
        ticker = data['ticker']
        price = data['price']
        print(f"Received message: ticker={ticker}, price={price}")
        
        # Connessione al database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Usa un cursor che restituisce dict
        
        # Scansione dei profili nel database
        cursor.execute("SELECT email, ticker, low_value, high_value FROM users WHERE ticker = %s", (ticker,))
        users = cursor.fetchall()
        
        # Controlla ogni profilo
        for user in users:
            email = user['email']
            low_value = user['low_value']
            high_value = user['high_value']
            condition = None
            
            # Verifica le condizioni di superamento soglia
            if low_value is not None and price < low_value:
                condition = f"below_low ({price} < {low_value})"
            elif high_value is not None and price > high_value:
                condition = f"above_high ({price} > {high_value})"
            
            if condition:
                # Costruisci il messaggio per il topic `to-notifier`
                notification = {
                    'email': email,
                    'ticker': ticker,
                    'condition': condition
                }
                produce_sync(producer, topic2, json.dumps(notification))
        
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error processing message: {e}")

consumer.close()
