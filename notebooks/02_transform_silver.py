from pyspark.sql import functions as F

# 1. Load raw Bronze Delta table
df_bronze = spark.read.table("bronze_retail_sales")
raw_count = df_bronze.count()

# 2. Apply automated data quality & validation checks
df_silver = (
    df_bronze
    .filter(F.col("transaction_id").isNotNull())          # Drop records missing primary key
    .dropDuplicates(["transaction_id"])                   # Remove duplicate transactions
    .filter(F.col("quantity") > 0)                        # Exclude zero/negative quantities
    .filter(F.col("unit_price") > 0)                      # Exclude negative/refunded prices
    .withColumn("status", F.initcap(F.trim(F.col("status"))))  # Standardize status casing
    .withColumn("total_revenue_zar", F.round(F.col("quantity") * F.col("unit_price"), 2))
    .withColumn("silver_processed_at", F.current_timestamp())
)

clean_count = df_silver.count()
quarantined = raw_count - clean_count
print(f"Validation summary: {clean_count} valid records promoted to Silver | {quarantined} invalid/duplicate records filtered out.")

# 3. Write validated records to Silver Delta table
df_silver.write.format("delta").mode("overwrite").saveAsTable("silver_retail_sales")
