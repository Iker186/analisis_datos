from kafka import KafkaConsumer
import json
import psycopg2

# Configuración del broker y PostgreSQL
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'results_postgres'
POSTGRES_CONFIG = {
    "dbname": "social_data",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

# Crear conexión a PostgreSQL
conn = psycopg2.connect(**POSTGRES_CONFIG)
cur = conn.cursor()

# Crear tabla si no existe (si es necesario)
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

# Crear consumidor de Kafka
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='latest',  # Solo leer los mensajes nuevos
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
)

# Consumir y guardar en PostgreSQL
for message in consumer:
    record = message.value
    
    # Asegurarse de que los campos estén correctamente alineados con la tabla de PostgreSQL
    cur.execute("""
        INSERT INTO results (userid, name, gender, dob, interests, city, country)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        record.get('user_id'),  # Asegúrate de que esto coincida con tu estructura de datos
        record.get('name', 'N/A'),  # Si no tienes un nombre, puedes dejar 'N/A' como valor predeterminado
        record.get('gender', 'N/A'),  # Lo mismo para el género
        record.get('dob', '1900-01-01'),  # Fecha de nacimiento predeterminada
        record.get('interests', 'N/A'),  # Intereses predeterminados
        record.get('city', 'N/A'),  # Ciudad predeterminada
        record.get('country', 'N/A')  # País predeterminado
    ))
    conn.commit()
    print(f"Guardado en PostgreSQL: {record}")

cur.close()
conn.close()
