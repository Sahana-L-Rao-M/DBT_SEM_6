import mysql.connector
import json

# refer spark_stream.py for schema

db = mysql.connector.connect(
    host="localhost",
    database="mcFlAi",
    user = "root",
    password = "password"
)
con = db.cursor()

def create_table():
    con.execute("CREATE TABLE IF NOT EXISTS airport (Year INT, Month INT, DayofMonth INT, DayOfWeek INT, DepTime INT, CRSDepTime INT, ArrTime INT, CRSArrTime INT, UniqueCarrier VARCHAR(255), FlightNum INT, TailNum VARCHAR(255), ActualElapsedTime INT, CRSElapsedTime INT, AirTime INT, ArrDelay INT, DepDelay INT, Origin VARCHAR(255), Dest VARCHAR(255), Distance INT, TaxiIn INT, TaxiOut INT, Cancelled INT, CancellationCode VARCHAR(255), Diverted INT, CarrierDelay INT, WeatherDelay INT, NASDelay INT, SecurityDelay INT, LateAircraftDelay INT)")
    db.commit()

create_table()
