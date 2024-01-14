from time import sleep
from json import dumps
from kafka import KafkaProducer
import csv
import sys

data_sender = KafkaProducer(
        bootstrap_servers = ['localhost:9092'],
        value_serializer = lambda x : dumps(x).encode('utf-8')
        )

if (len(sys.argv) != 2):
    print("\nUsage is 'python3 airport.py <csv filename>' \n") 
    sys.exit()

try:
    with open(sys.argv[1]) as source:
        header = next(source)
        rows = csv.reader(source)
        num = 0
        for row in rows:
            if(row[12]=='NA' or row[14]=='NA' or row[15]=='NA'):
                continue
            row[12] = int(row[12])  
            row[14] = int(row[14])  
            row[15] = int(row[15])  
            if(row[21] == 'NA'):
                row[21] = 0
            else:
                row[21] = int(row[21])
            data_sender.send('airport',value = row)
            num = num+1
            print("Sent row : "+str(num))
            sleep(1)


except FileNotFoundError:
    print("\n You've put a wrong file you nitwit\n")
except KeyboardInterrupt:
    print("\n You have grounded this flight \n")
except :
    print("\n Just hope this program is the only thing that has crashed !\n")
