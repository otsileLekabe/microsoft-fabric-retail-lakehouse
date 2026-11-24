from pyspark.sql import functions as F

# 1. Read raw CSV file from Lakehouse Files storage
df_raw = (
    spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load("Files/raw/sample_retail_raw.csv")
)

# 2. Append ingestion audit metadata
df_bronze = df_raw.withColumn("ingested_at", F.current_timestamp())

# 3. Persist raw records as a Bronze Delta table
df_bronze.write.format("delta").mode("overwrite").saveAsTable("bronze_retail_sales")

print(f"Bronze ingestion complete: {df_bronze.count()} raw records loaded.")
