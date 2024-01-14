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

userSchema = StructType()\
            .add("year","integer")\
            .add("month","integer")\
            .add("dayofmonth","integer")\
            .add("dayofweek","integer")\
            .add("deptime","integer")\
            .add("crsdeptime","integer")\
            .add("arrtime","integer")\
            .add("carrier","string")\
            .add("flightnum","integer")\
            .add("tailnum","string")\
            .add("elapsedtime","integer")\
            .add("crselapsedtime","integer")\
            .add("airtime","string")\
            .add("arrdelay","integer")\
            .add("depdelay","integer")\
            .add("origin","string")\
            .add("dest","string")\
            .add("distance","integer")\
            .add("taxiin","string")\
            .add("taxiout","string")\
            .add("cancelled","string")\
            .add("cancellationcode","string")\
            .add("diverted","string")\
            .add("carrierdelay","string")\
            .add("weatherdelay","string")\
            .add("nasdelay","string")\
            .add("securitydelay","string")\
            .add("lateaircraftdelay","string")\

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



lines = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "airport") \
  .option("sep",",")\
  .schema(userSchema)
  .load()

words = lines.select(
    explode(
        split(lines.value,",")
        ).alias("word")
    )

wordCounts = words.groupBy("word").count()
wordCounts = words.agg
query = wordCounts\
        .writeStream\
        .outputMode("complete")\
        .format("console")\
        .start()
query.awaitTermination()






###
lines = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "airport") \
  .option("sep",",")\
  .schema(userSchema)\
  .load()

carrierCounts = lines.groupBy("carrier").count()
query = carrierCOunts\
        .writeStream\
        .outputMode("complete")\
        .format("console")\
        .start()
query.awaitTermination()
'''
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
originAvgArrDelay = lines.groupBy("origin").avg("arrdelay")

#average departure delay per origin
originAvgDepDelay = lines.groupBy("origin").avg("depdelay")

#average creairtimes per origin
origincrselapsedtime = lines.groupBy("origin").avg("crselapsedtime")

#count cancelled per origin
originCancelled = lines.groupBy("origin").sum("cancelled")


#lines.select("year","month","dayofmonth","dayofweek","deptime","crsdeptime","arrtime","crsarrtime","uniquecarrier","flightnum","tailnum","actualelapsedtime","crselapsedtime","airtime","arrdelay","depdelay","origin","dest","distance","taxiin","taxiout","cancelled","cancellationcode","diverted","carrierdelay","weatherdelay","nasdelay","securitydelay","lateaircraftdelay").writeStream.format("console").start().awaitTermination()

#lines.select("crselapsedtime").writeStream.format("console").start().awaitTermination()



query = originCancelled\
        .writeStream\
        .outputMode("complete")\
        .format("console")\
        .start()

'''