from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, to_date
import os

# ✅ Iniciar sesión de Spark
spark = SparkSession.builder.appName("SocialMediaProcessing").getOrCreate()

# 📥 Cargar dataset desde CSV
df = spark.read.csv("./data/social_media.csv", header=True, inferSchema=True)

# 🧹 Limpieza de datos
df = df.dropna()

# 🎂 Calcular edad a partir del DOB
df = df.withColumn("DOB", to_date(col("DOB"), "yyyy-MM-dd"))
df = df.withColumn("Edad", year("2025-01-01") - year(col("DOB")))

# 🎯 Seleccionar columnas relevantes
columns_to_keep = ["UserID", "Country", "City", "Gender", "Interests", "Edad"]
df_final = df.select(columns_to_keep)

# 📊 Agregar análisis de interés principal
df_interests = df_final.groupBy("Interests").count().orderBy("count", ascending=False)

# 📂 Crear carpeta para resultados si no existe
if not os.path.exists("results"):
    os.makedirs("results")

# 💾 Guardar resultados procesados
df_final.write.mode("overwrite").json("results/processed_data.json")
df_interests.write.mode("overwrite").json("results/interests_summary.json")

print("✅ Proceso completado y datos guardados en 'results/'")
