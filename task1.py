from pyspark.sql import SparkSession
from pyspark.sql.functions import col, length, count

# Initialiser SparkSession
spark = SparkSession.builder \
    .appName("TelegramAnomalyDetection") \
    .getOrCreate()

# Lire les fichiers Parquet en continu
parquet_dir = 'parquet_files'
df = spark.readStream \
    .format("parquet") \
    .schema("timestamp TIMESTAMP, source STRING, text STRING, has_media BOOLEAN") \
    .load(parquet_dir)

# Analyser les anomalies (exemple : longueur de texte inhabituellement longue/courte)
# Анализ аномалий (пример: необычно длинная/короткая длина текста)
anomalies = df.withColumn("text_length", length(col("text"))) \
    .filter((col("text_length") > 500) | (col("text_length") < 10))

# Afficher les anomalies détectées
query = anomalies.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
