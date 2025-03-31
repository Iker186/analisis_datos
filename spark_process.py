from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, col, year, to_date

import os

spark = SparkSession.builder.appName("SocialMediaProcessing").getOrCreate()

df = spark.read.csv("./data/social_media.csv", header=True, inferSchema=True)

df = df.dropna()

fixed_date = to_date(lit("2025-01-01"), "yyyy-MM-dd")

df = df.withColumn("DOB", to_date(col("DOB"), "yyyy-MM-dd"))
df = df.withColumn("Edad", year(fixed_date) - year(col("DOB")))

columns_to_keep = ["UserID", "Country", "City", "Gender", "Interests", "Edad"]
df_final = df.select(columns_to_keep)

df_interests = df_final.groupBy("Interests").count().orderBy("count", ascending=False)

if not os.path.exists("results"):
    os.makedirs("results")

df_final.write.mode("overwrite").json("results/processed_data.json")
df_interests.write.mode("overwrite").json("results/interests_summary.json")

print("✅ Proceso completado y datos guardados en 'results/'")
