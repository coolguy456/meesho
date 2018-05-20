# meesho

Req: Redis, Kafka, python2.7, mongodb

Used Redis for caching and mongodb for storing data
producer.py produces data. Also accepts an argument to produce certain amount of data

notificationconsumer behaves as worker for notificationQueue 
invoiceconsumer behaves as worker for invoiceQueue

To get running completely keep running producer.py,notificationConsumer.py,invoiceConsumer.py

##################################################
scaling consumers can be done using multithreading which is possible by multithreading_consumers.py although not complete working model but a partial one
size of kafka can be obtained using command which is also not implemented but can be done easily.
