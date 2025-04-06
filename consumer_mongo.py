from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import os

KAFKA_BROKER = os.getenv('KAFKA_SERVER')
TOPIC = os.getenv('KAFKA_TOPIC', 'results_topic')
MONGO_URI = os.getenv('MONGO_URI')  
DB_NAME = 'social_data'
COLLECTION_NAME = 'results'

try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[DB_NAME]
    collection = db[COLLECTION_NAME]
    print("Conexión con MongoDB exitosa.")
except Exception as e:
    print(f"Error al conectar con MongoDB: {e}")
    exit(1)

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    security_protocol=os.getenv("KAFKA_SECURITY_PROTOCOL", "SASL_SSL"), 
    sasl_mechanism=os.getenv("KAFKA_SASL_MECHANISM", "SCRAM-SHA-256"),  
    sasl_plain_username=os.getenv("KAFKA_USERNAME"),
    sasl_plain_password=os.getenv("KAFKA_PASSWORD"),
    auto_offset_reset='earliest', 
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    consumer_timeout_ms=15000
)

for message in consumer:
    record = message.value
    try:
        collection.insert_one(record)
        print(f"[✓] Guardado en MongoDB: {record}")
    except Exception as e:
        print(f"Error al guardar en MongoDB: {e}")
