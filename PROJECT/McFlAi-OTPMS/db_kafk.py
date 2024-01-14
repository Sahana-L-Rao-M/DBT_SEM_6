'''
Schema of db:
refer spark_stream.py

'''
import mysql.connector
from kafka import KafkaConsumer
from json import loads
from sys import argv
from create_db import create_table

Consumer = None
Topic = argv[1]

colum = ["Year","Month","DayofMonth","DayOfWeek","DepTime","CRSDepTime","ArrTime","CRSArrTime","UniqueCarrier","FlightNum","TailNum","ActualElapsedTime","CRSElapsedTime","AirTime","ArrDelay","DepDelay","Origin","Dest","Distance","TaxiIn","TaxiOut","Cancelled","CancellationCode","Diverted","CarrierDelay","WeatherDelay","NASDelay","SecurityDelay","LateAircraftDelay"]

def init_db():
	global DB_CON
	DB_CON = mysql.connector.connect(
		host="localhost",
		database="mcFlAi",
		user="root",
		password="password"
    )
	

cur = DB_CON.cursor()	
def insert_db(data):
	global DB_CON
    

def init_consumer():
    global consumer
    consumer = KafkaConsumer(
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )
    consumer.subscribe([Topic]) 

def insert_db(data):
    global DB_CON

    # Prepare the SQL query to insert the data into the database
    sql = "INSERT INTO flights (Year, Month, DayofMonth, DayOfWeek, DepTime, CRSDepTime, ArrTime, CRSArrTime, UniqueCarrier, FlightNum, TailNum, ActualElapsedTime, CRSElapsedTime, AirTime, ArrDelay, DepDelay, Origin, Dest, Distance, TaxiIn, TaxiOut, Cancelled, CancellationCode, Diverted, CarrierDelay, WeatherDelay, NASDelay, SecurityDelay, LateAircraftDelay) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    try:
        # Iterate over the messages and insert them into the database
        for message in data:
            # Get the message value
            value = message.value

            # Extract the required columns from the message
            values = [
                value.get("Year"),
                value.get("Month"),
                value.get("DayofMonth"),
                value.get("DayOfWeek"),
                value.get("DepTime"),
                value.get("CRSDepTime"),
                value.get("ArrTime"),
                value.get("CRSArrTime"),
                value.get("UniqueCarrier"),
                value.get("FlightNum"),
                value.get("TailNum"),
                value.get("ActualElapsedTime"),
                value.get("CRSElapsedTime"),
                value.get("AirTime"),
                value.get("ArrDelay"),
                value.get("DepDelay"),
                value.get("Origin"),
                value.get("Dest"),
                value.get("Distance"),
                value.get("TaxiIn"),
                value.get("TaxiOut"),
                value.get("Cancelled"),
                value.get("CancellationCode"),
                value.get("Diverted"),
                value.get("CarrierDelay"),
                value.get("WeatherDelay"),
                value.get("NASDelay"),
                value.get("SecurityDelay"),
                value.get("LateAircraftDelay")
            ]

            # Execute the query and commit the changes
            cur = DB_CON.cursor()
            cur.execute(sql, values)
            DB_CON.commit()

            # Print a message to indicate the successful insertion
            print("Message inserted successfully!")
    except Exception as e:
        # Rollback the transaction in case of an error
        DB_CON.rollback()
        print("Failed to insert message:", e)
                 
