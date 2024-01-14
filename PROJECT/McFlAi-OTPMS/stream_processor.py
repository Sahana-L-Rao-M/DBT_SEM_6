import pyspark,sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,IntegerType,StringType,DoubleType
from pyspark.sql.functions import udf,col,decode,explode,split,expr,element_at
from json import loads

'''
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
'''

spark = SparkSession\
        .builder\
        .appName("OTPMS")\
        .config("spark.jars.packages","org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0")\
        .getOrCreate()


lines = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "airport") \
  .load()


split_df = split(lines['value'],",")
lines = lines.withColumn('year', split_df.getItem(0))
lines = lines.withColumn('month', split_df.getItem(1))
lines = lines.withColumn('dayofmonth', split_df.getItem(2))
lines = lines.withColumn('dayofweek', split_df.getItem(3))
lines = lines.withColumn('deptime', split_df.getItem(4))
lines = lines.withColumn('crsdeptime', split_df.getItem(5))
lines = lines.withColumn('arrtime', split_df.getItem(6))
lines = lines.withColumn('crsarrtime', split_df.getItem(7))
lines = lines.withColumn('uniquecarrier', split_df.getItem(8))
lines = lines.withColumn('flightnum', split_df.getItem(9))
lines = lines.withColumn('tailnum', split_df.getItem(10))
lines = lines.withColumn('actualelapsedtime', split_df.getItem(11))
lines = lines.withColumn('crselapsedtime', split_df.getItem(12).cast("integer"))
lines = lines.withColumn('airtime', split_df.getItem(13).cast(IntegerType()))
lines = lines.withColumn('arrdelay', split_df.getItem(14).cast("integer"))
lines = lines.withColumn('depdelay', split_df.getItem(15).cast("integer"))
lines = lines.withColumn('origin', split_df.getItem(16))
lines = lines.withColumn('dest', split_df.getItem(17))
lines = lines.withColumn('distance', split_df.getItem(18))
lines = lines.withColumn('taxiin', split_df.getItem(19))
lines = lines.withColumn('taxiout', split_df.getItem(20))
lines = lines.withColumn('cancelled', split_df.getItem(21).cast("integer"))
lines = lines.withColumn('cancellationcode', split_df.getItem(22))
lines = lines.withColumn('diverted', split_df.getItem(23))
lines = lines.withColumn('carrierdelay', split_df.getItem(24))
lines = lines.withColumn('weatherdelay', split_df.getItem(25))
lines = lines.withColumn('nasdelay', split_df.getItem(26))
lines = lines.withColumn('securitydelay', split_df.getItem(27))
lines = lines.withColumn('lateaircraftdelay', split_df.getItem(28))



#count of flights per origin
originCount = lines.groupBy("origin").count()

#count of flights per destination
destCount = lines.groupBy("dest").count()

#average arrival delay  per origin
originAvgArrDelay = lines.groupBy("origin").avg("arrdelay").withColumnRenamed("avg(arrdelay)","avgArrDelay")

#average departure delay per origin
originAvgDepDelay = lines.groupBy("origin").avg("depdelay")

#average creairtimes per origin
origincrselapsedtime = lines.groupBy("origin").avg("crselapsedtime")

#count cancelled per origin
originCancelled = lines.groupBy("origin").sum("cancelled")


#lines.select("year","month","dayofmonth","dayofweek","deptime","crsdeptime","arrtime","crsarrtime","uniquecarrier","flightnum","tailnum","actualelapsedtime","crselapsedtime","airtime","arrdelay","depdelay","origin","dest","distance","taxiin","taxiout","cancelled","cancellationcode","diverted","carrierdelay","weatherdelay","nasdelay","securitydelay","lateaircraftdelay").writeStream.format("console").start().awaitTermination()

#lines.select("crselapsedtime").writeStream.format("console").start().awaitTermination()


'''
query = originCancelled\
        .writeStream\
        .outputMode("complete")\
        .format("console")\
        .start()

#query.awaitTermination()

#write query to kafkaProducer
originCount\
        .writeStream\
        .outputMode("complete")\
        .format("kafka")\
        .option("kafka.bootstrap.servers", "localhost:9092")\
        .option("topic", "origins")\
        .option("checkpointLocation", "checkpoint")\
        .start()
'''

originAvgArrDelay\
    .selectExpr("CAST(origin AS STRING) AS key", "CAST(avgArrDelay AS STRING) AS value")\
    .writeStream\
    .format("kafka")\
    .outputMode("complete")\
    .option("kafka.bootstrap.servers", "localhost:9092")\
    .option("topic",    "origins")\
    .option("checkpointLocation", "checkpoint1")\
    .start()\
    .awaitTermination()


'''
udf_json = udf(lambda x: vals(x), StringType())

df = lines\
    .withColumn('contents',decode(lines.value, "UTF-8")\
    .cast("string"))
df_val = df.withColumn("res",udf_json(df.contents))
df_val.select("contents","res").writeStream.format("console").start().awaitTermination()
'''
'''
words = lines.select(
    explode(
        split(lines.value,",")
        ).alias("word")
    )

wordCounts = words.groupBy("word").count()

query = wordCounts\
        .writeStream\
        .outputMode("complete")\
        .format("console")\
        .start()
query.awaitTermination()
'''
