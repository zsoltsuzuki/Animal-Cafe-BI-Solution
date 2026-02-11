import os
import sys
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType

# --- ENVIRONMENT CONFIGURATION ---
# Note: Ensure these environment variables are set on your local machine
# or defined in a separate .env file.
os.environ['SPARK_HOME'] = os.getenv('SPARK_HOME', 'YOUR_SPARK_HOME_PATH')
os.environ['HADOOP_HOME'] = os.getenv('HADOOP_HOME', 'YOUR_HADOOP_HOME_PATH')
os.environ['JAVA_HOME'] = os.getenv('JAVA_HOME', 'YOUR_JAVA_HOME_PATH')

# For Windows users, specific executable paths might be needed:
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

# 1. SPARK SESSION INITIALIZATION
# Including Kafka and PostgreSQL JDBC connectors for stream processing
print("[INFO] Initializing Spark Session with Kafka and PostgreSQL support...")
spark = SparkSession.builder \
    .appName("LCA_Emissions_StreamProcessor") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.6.0") \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()

# Suppress verbose logs to focus on warnings and errors
spark.sparkContext.setLogLevel("WARN")

# 2. SCHEMA DEFINITION
# Aligning the schema with the LCA (Lifecycle Assessment) event structure
json_schema = StructType([
    StructField("timestamp", LongType(), True),
    StructField("factory_id", StringType(), True),
    StructField("location", StringType(), True),
    StructField("material", StringType(), True),
    StructField("process_step", StringType(), True),
    StructField("energy_consumption_kwh", DoubleType(), True),
    StructField("co2_emissions_kg", DoubleType(), True)
])

# 3. STREAM INGESTION FROM KAFKA
print("[INFO] Connecting to Kafka broker...")
raw_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "factory_emissions") \
    .option("startingOffsets", "earliest") \
    .load()

# 4. DATA TRANSFORMATION & PARSING
# Converting binary Kafka payload to string and parsing JSON based on schema
parsed_stream = raw_stream.select(
    from_json(col("value").cast("string"), json_schema).alias("data")
).select("data.*")

# 5. DATA CLEANSING (Silver Layer Logic)
# Filtering out records with missing IDs or impossible (negative) emission values
clean_stream = parsed_stream.filter(
    (col("factory_id").isNotNull()) & 
    (col("material").isNotNull()) &
    (col("co2_emissions_kg") >= 0)
)

# 6. PERSISTENCE LAYER - WRITING TO POSTGRESQL
# Function to persist each micro-batch into the relational database
def write_to_postgres(df, epoch_id):
    if df.count() > 0:
        print(f"[PROCESS] Persisting Batch ID: {epoch_id} | Record Count: {df.count()}")
        df.write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://localhost:5432/bigdata_db") \
            .option("driver", "org.postgresql.Driver") \
            .option("dbtable", "lca_emissions_cleansed") \
            .option("user", "admin") \
            .option("password", "password123") \
            .mode("append") \
            .save()

print("[INFO] Starting Stream Processing Pipeline...")

# Executing the stream with Checkpointing for fault tolerance
query = clean_stream.writeStream \
    .foreachBatch(write_to_postgres) \
    .option("checkpointLocation", "checkpoints/lca_pipeline") \
    .start()

query.awaitTermination()
