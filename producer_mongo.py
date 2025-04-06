import os
import json
from kafka import KafkaProducer

KAFKA_BROKER = os.getenv('KAFKA_SERVER')
TOPIC = os.getenv('KAFKA_TOPIC', 'results_topic')

print(f"KAFKA_BROKER: {KAFKA_BROKER}")
print(f"TOPIC: {TOPIC}")
print("Inicializando productor de Kafka...")

try:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        security_protocol=os.getenv("KAFKA_SECURITY_PROTOCOL", "SASL_SSL"),
        sasl_mechanism=os.getenv("KAFKA_SASL_MECHANISM", "SCRAM-SHA-256"),
        sasl_plain_username=os.getenv("KAFKA_USERNAME"),
        sasl_plain_password=os.getenv("KAFKA_PASSWORD"),
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print("✅ KafkaProducer listo.")
except Exception as e:
    print(f"❌ Error al conectar a Kafka: {e}")
    exit(1)

# Enviar un mensaje de prueba
record = {"test": "mensaje de prueba"}
try:
    print(f"Enviando mensaje de prueba a {TOPIC}...")
    future = producer.send(TOPIC, value=record)
    result = future.get(timeout=10)  # ← aquí lanza errores si hay problema real
    print(f"✅ Mensaje enviado: {result}")
except Exception as e:
    print(f"❌ Error al enviar mensaje: {e}")

producer.flush()
producer.close()
