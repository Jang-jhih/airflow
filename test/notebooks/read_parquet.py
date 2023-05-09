from pyspark.sql import SparkSession

hdfs_address = "hdfs://namenode:50070"

spark = SparkSession.builder \
    .appName("Read Parquet from HDFS") \
    .getOrCreate()

parquet_file_path = f"{hdfs_address}/user/hive/warehouse/{tablename}/{filename}"

df = spark.read.parquet(parquet_file_path)

df.show()
