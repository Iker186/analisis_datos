import pandas as pd
from kafka import KafkaProducer
import json
import os

KAFKA_BROKER = os.getenv('KAFKA_SERVER')
TOPIC = os.getenv('KAFKA_TOPIC', 'results_topic') 

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    security_protocol=os.getenv("KAFKA_SECURITY_PROTOCOL", "SASL_SSL"),
    sasl_mechanism=os.getenv("KAFKA_SASL_MECHANISM", "SCRAM-SHA-256"),
    sasl_plain_username=os.getenv("KAFKA_USERNAME"),
    sasl_plain_password=os.getenv("KAFKA_PASSWORD"),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

data = pd.read_csv('./data/social_media.csv') 

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
    print(f"[→] Enviado a Kafka (Mongo): {record}")

producer.flush()
producer.close()
