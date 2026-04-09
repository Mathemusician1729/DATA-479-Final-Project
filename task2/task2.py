import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, year, avg, round as spark_round

storage_account = "data479projectg5"
container = "raw-data"
storage_key = os.environ.get("AZURE_STORAGE_KEY")

paths = [
    "wasbs://raw-data@data479projectg5.blob.core.windows.net/1999/*",
    "wasbs://raw-data@data479projectg5.blob.core.windows.net/2000/*",
    "wasbs://raw-data@data479projectg5.blob.core.windows.net/2001/*",
    "wasbs://raw-data@data479projectg5.blob.core.windows.net/2009/*",
    "wasbs://raw-data@data479projectg5.blob.core.windows.net/2010/*",
    "wasbs://raw-data@data479projectg5.blob.core.windows.net/2011/*",
    "wasbs://raw-data@data479projectg5.blob.core.windows.net/2019/*",
    "wasbs://raw-data@data479projectg5.blob.core.windows.net/2020/*",
    "wasbs://raw-data@data479projectg5.blob.core.windows.net/2021/*"
]

spark = (
    SparkSession.builder
    .appName("Task2_ClimateAnalytics")
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-azure:3.4.3")
    .config(
        f"fs.azure.account.key.{storage_account}.blob.core.windows.net",
        storage_key
    )
    .getOrCreate()
)

df = spark.read.csv(paths, header=True, inferSchema=True)

print("Schema:")
df.printSchema()

print("Sample rows:")
df.show(5, truncate=False)

weather_df = df.select("STATION", "DATE", "TEMP")

clean_df = weather_df.filter((col("TEMP").isNotNull()) & (col("TEMP") != 9999.9))

clean_df = clean_df.withColumn("DATE", to_date(col("DATE"), "yyyy-MM-dd"))
clean_df = clean_df.withColumn("year", year(col("DATE")))
clean_df = clean_df.filter(col("year").isNotNull())

result_df = (clean_df.groupBy("STATION", "year").agg(spark_round(avg("TEMP"), 2).alias("average_temperature")).orderBy("STATION", "year"))

final_df = result_df.select(col("STATION").alias("station"), col("year"), col("average_temperature"))

print("Final output:")
final_df.show(100, truncate=False)

final_df.coalesce(1).write.mode("overwrite").option("header", True).csv("task2_output")

print("done")

spark.stop()