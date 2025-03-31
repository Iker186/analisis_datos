from kafka import KafkaProducer
import json
import pandas as pd
from datetime import datetime

KAFKA_BROKER = 'localhost:9092'
TOPIC = 'results_postgres'

data = pd.read_csv('./data/social_media.csv')

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for _, row in data.iterrows():
    record = {
        "user_id": row['UserID'],
        "name": row['Name'],
        "gender": row['Gender'],
        "dob": row['DOB'], 
        "interests": row['Interests'],
        "city": row['City'],
        "country": row['Country']
    }
    producer.send(TOPIC, value=record)
    print(f"Enviado: {record}")

producer.close()
