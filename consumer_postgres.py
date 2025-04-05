from kafka import KafkaConsumer
import json
import psycopg2
import os

KAFKA_BROKER = os.getenv('KAFKA_SERVER')
TOPIC = os.getenv('KAFKA_TOPIC_POSTGRES', 'results_postgres')

POSTGRES_CONFIG = {
    "dbname": os.getenv('POSTGRES_DB'),
    "user": os.getenv('POSTGRES_USER'),
    "password": os.getenv('POSTGRES_PASSWORD'),
    "host": os.getenv('POSTGRES_HOST'),
    "port": os.getenv('POSTGRES_PORT', '5432')
}

conn = psycopg2.connect(**POSTGRES_CONFIG)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS results (
    user_id INT,
    name VARCHAR(255),
    gender VARCHAR(10),
    dob DATE,
    interests TEXT,
    city VARCHAR(255),
    country VARCHAR(255)
)
""")
conn.commit()

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    security_protocol=os.getenv("KAFKA_SECURITY_PROTOCOL", "PLAINTEXT"),
    sasl_mechanism=os.getenv("KAFKA_SASL_MECHANISM", "PLAIN"),
    sasl_plain_username=os.getenv("KAFKA_USERNAME"),
    sasl_plain_password=os.getenv("KAFKA_PASSWORD"),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    record = message.value
    cur.execute("""
        INSERT INTO results (user_id, name, gender, dob, interests, city, country)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        record.get('user_id'), 
        record.get('name', 'N/A'), 
        record.get('gender', 'N/A'), 
        record.get('dob', '1900-01-01'),  
        record.get('interests', 'N/A'), 
        record.get('city', 'N/A'), 
        record.get('country', 'N/A')
    ))
    conn.commit()
    print(f"[✓] Guardado en PostgreSQL: {record}")

cur.close()
conn.close()
