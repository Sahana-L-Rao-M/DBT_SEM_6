from json import loads
from kafka import KafkaConsumer
import sys

consumer = KafkaConsumer(
        sys.argv[1],
        bootstrap_servers= ['localhost : 9092'],
        #auto_offset_reset = 'earliest',
        #enable_auto_commit = True,
        #group_id = 'my-group',
        #value_deserializer = lambda x : loads(x.decode('utf-8'))
        )
try:
    for message in consumer:
        print(message)
except KeyboardInterrupt:
    print("\n Airport Closed \n ")
#except:
#    print("\n Catastrophe ! \n")


