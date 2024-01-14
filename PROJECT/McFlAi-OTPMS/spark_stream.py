import pyspark,sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,IntegerType,StringType,DoubleType
from pyspark.sql.functions import col,explode,split,expr,element_at
from json import loads

schema = StructType([
    StructField("Year", IntegerType(), True),
    StructField("Month", IntegerType(), True),
    StructField("DayofMonth", IntegerType(), True),
    StructField("DayOfWeek", IntegerType(), True),
    StructField("DepTime", IntegerType(), True),
    StructField("CRSDepTime", IntegerType(), True),
    StructField("ArrTime", IntegerType(), True),
    StructField("CRSArrTime", IntegerType(), True),
    StructField("UniqueCarrier", StringType(), True),
    StructField("FlightNum", IntegerType(), True),
    StructField("TailNum", StringType(), True),
    StructField("ActualElapsedTime", IntegerType(), True),
    StructField("CRSElapsedTime", IntegerType(), True),
    StructField("AirTime", IntegerType(), True),
    StructField("ArrDelay", IntegerType(), True),
    StructField("DepDelay", IntegerType(), True),
    StructField("Origin", StringType(), True),
    StructField("Dest", StringType(), True),
    StructField("Distance", IntegerType(), True),
    StructField("TaxiIn", IntegerType(), True),
    StructField("TaxiOut", IntegerType(), True),
    StructField("Cancelled", IntegerType(), True),
    StructField("CancellationCode", StringType(), True,metadata={"nullValue": "NA"}),
    StructField("Diverted", IntegerType(), True,metadata={"nullValue": "NA"}),
    StructField("CarrierDelay", IntegerType(), True,metadata={"nullValue": "NA"}),
    StructField("WeatherDelay", IntegerType(), True,metadata={"nullValue": "NA"}),
    StructField("NASDelay", IntegerType(), True,metadata={"nullValue": "NA"}),
    StructField("SecurityDelay", IntegerType(), True,metadata={"nullValue": "NA"}),
    StructField("LateAircraftDelay", IntegerType(), True, metadata={"nullValue": "NA"})
])


spark = SparkSession\
        .builder\
        .appName("OTPMS")\
        .config("spark.jars.packages","org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0")\
        .getOrCreate()

Topic = "airport"


df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", Topic) \
  .load()

'''
#.selectExpr("CAST(value AS STRING)")
k = 0
query = df.selectExpr("CAST(value as STRING)")\
    .toDF("Potato")\
    .select(split(col("Potato"), ",").getItem(14).cast("integer").alias("Delay")) \
    .writeStream\
    .outputMode("append")\
    .format("console")\
    .start()\
'''
query = df.selectExpr("CAST(value as STRING)")\
    .toDF("Potato")\
    .select(split(col("Potato"), ",").getItem(14).cast("integer").alias("Delay"))
    
sum = 0

'''
query = query.select(split(col("value"), ",").getItem(9).cast("double").alias("col_10")) \
    .agg(sum(col("col_10")).alias("sum_col_10")) \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()
'''

#fun = df.select(split(col("value"), ",").getItem(1).cast("integer").alias("year"))

'''
fun = df.selectExpr("CAST(value as STRING)")\
      .select(element_at("value", 1)).show()

query = fun.writeStream\
    .outputMode("append")\
    .format("console")\
    .start()



'''
#fun.awaitTermination()

#query.awaitTermination()



#record = df.selectExpr("CAST(value AS STRING)")
#record_obj = record.select(split(col("value"), ",").getItem(9).cast("double").alias("col_10"))
#record_obj.show()



'''
q = df.select("value") \
  .writeStream \
  .outputMode("append")\
  .format("console") \
  .start()

q.awaitTermination()
'''
#Does not work
'''
query = df.selectExpr("CAST(value AS STRING)") \
    .select(split(col("value"), ",").getItem(9).cast("double").alias("col_10")) \
    .agg(sum(col("col_10")).alias("sum_col_10")) \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()
'''
