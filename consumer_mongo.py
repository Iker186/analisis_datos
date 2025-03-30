# consumer_mongo.py
from kafka import KafkaConsumer
import json
from pymongo import MongoClient

# Configuración del broker y MongoDB
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'results_topic'
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'social_data'
COLLECTION_NAME = 'results'

# Conexión a MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Crear consumidor de Kafka
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Consumir y guardar en MongoDB
for message in consumer:
    record = message.value
    collection.insert_one(record)
    print(f"Guardado en MongoDB: {record}")
