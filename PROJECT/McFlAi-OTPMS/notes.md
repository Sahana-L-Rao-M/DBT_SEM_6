https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/HG7NV7

- [ x ] Dataset 
- [ x ] Producer
- [ x ] Consumer
- [	 ] Stream processor doesn't work


Pyspark 3.3.0
Postgres 12.14


Kafka and Spark are connected and streaming now.

God help us clean the input stream and convert it into a df, can't seem to be able to do it on the fly.

.show() doesn't work on streams, do be warned

I really don't want to write a constructor for this mess :( 

Why is this not working