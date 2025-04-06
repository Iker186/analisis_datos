import pandas as pd
from kafka import KafkaProducer
import json
import os

KAFKA_BROKER = os.getenv('KAFKA_SERVER')
TOPIC = os.getenv('KAFKA_TOPIC', 'results_topic')

# Configuración del productor
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    security_protocol=os.getenv("KAFKA_SECURITY_PROTOCOL", "SASL_SSL"),  # Usamos SASL_SSL por Redpanda
    sasl_mechanism=os.getenv("KAFKA_SASL_MECHANISM", "SCRAM-SHA-256"),  # O SCRAM-SHA-512 según lo que hayas configurado
    sasl_plain_username=os.getenv("KAFKA_USERNAME"),
    sasl_plain_password=os.getenv("KAFKA_PASSWORD"),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Cargar datos desde CSV
try:
    data = pd.read_csv('./data/social_media.csv')
except Exception as e:
    print(f"Error al leer el archivo CSV: {e}")
    exit(1)

# Enviar cada registro a Kafka
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
    try:
        producer.send(TOPIC, value=record)
        print(f"[→] Enviado a Kafka: {record}")
    except Exception as e:
        print(f"Error al enviar mensaje a Kafka: {e}")

producer.flush()
producer.close()
