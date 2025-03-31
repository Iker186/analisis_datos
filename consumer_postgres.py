from kafka import KafkaConsumer
import json
import psycopg2

KAFKA_BROKER = 'localhost:9092'
TOPIC = 'results_postgres'
POSTGRES_CONFIG = {
    "dbname": "social_data",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

conn = psycopg2.connect(**POSTGRES_CONFIG)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS results (
    userid INT,
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
    auto_offset_reset='latest',  
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
)

for message in consumer:
    record = message.value
    
    cur.execute("""
        INSERT INTO results (userid, name, gender, dob, interests, city, country)
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
    print(f"Guardado en PostgreSQL: {record}")

cur.close()
conn.close()
