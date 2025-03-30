# producer_postgres.py
from kafka import KafkaProducer
import json
import pandas as pd
from datetime import datetime

# Configuración del broker de Kafka
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'results_postgres'

# Cargar el dataset
data = pd.read_csv('./data/social_media.csv')

# Crear productor de Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Enviar datos del dataset a Kafka
for _, row in data.iterrows():
    record = {
        "user_id": row['UserID'],
        "name": row['Name'],
        "gender": row['Gender'],
        "dob": row['DOB'],  # Asegúrate de que el formato de la fecha sea correcto
        "interests": row['Interests'],
        "city": row['City'],
        "country": row['Country']
    }
    producer.send(TOPIC, value=record)
    print(f"Enviado: {record}")

producer.close()
