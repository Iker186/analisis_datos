# producer_mongo.py
import pandas as pd
from kafka import KafkaProducer
import json
from datetime import datetime

# Configuración del broker de Kafka
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'results_topic'

# Crear productor de Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Cargar el dataset real
data = pd.read_csv('./data/social_media.csv')

# Enviar los datos a Kafka
for _, row in data.iterrows():
    record = {
        "UserID": row["UserID"],
        "Name": row["Name"],
        "Gender": row["Gender"],
        "DOB": row["DOB"],
        "Interests": row["Interests"],
        "City": row["City"],
        "Country": row["Country"]
    }
    producer.send(TOPIC, value=record)
    print(f"Enviado a Kafka: {record}")

producer.close()
