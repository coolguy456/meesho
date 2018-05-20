import os
import json
import time
from confluent_kafka import Consumer,KafkaError

class notificationQueueWorker():

    kafkaBootstrapServers = os.getenv('kafkaBootstrapServers')
    deserializer = lambda v: json.loads(v)
    topic = os.getenv('notificationTopic')

    def __init__(self):
        self.consumer = Consumer({
            'bootstrap.servers': self.kafkaBootstrapServers,
            'group.id': self.topic,
            'default.topic.config': {
                'auto.offset.reset': 'smallest'
            }
        })

    def consume(self,ordersController):
        self.consumer.subscribe([self.topic])
        while True:
            dataRetreived = self.consumer.poll(1.0)
            if dataRetreived is None:
                continue
            if dataRetreived.error():
                if dataRetreived.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(dataRetreived.error())
                    break
            data = json.loads("{}".format(dataRetreived.value().decode('utf-8')))
            try:
                time.sleep(0.1)
                databaseData = ordersController.read({'_id':data['orderID']})
                if databaseData['invoiceURL'] == 'null':
                    print data['orderID']+"@gmail.com along with sms without receipt"
                else:
                    print data['orderID'] + "@gmail.com along with sms and receipt"
                databaseData['notification'] = True
                # del databaseData['_cls']
                # databaseData['_id'] = str(databaseData['_id'])
                ordersController.update(databaseData)
            except:
                print('failed over here')
        self.consumer.close()


class invoiceQueueWorker():

    kafkaBootstrapServers = os.getenv('kafkaBootstrapServers')
    topic = os.getenv('invoiceTopic')

    def __init__(self):
        self.consumer = Consumer({
            'bootstrap.servers': self.kafkaBootstrapServers,
            'group.id': self.topic,
            'default.topic.config': {
                'auto.offset.reset': 'smallest'
            }
        })

    def consume(self,ordersController):
        self.consumer.subscribe([self.topic])
        while True:
            dataRetreived = self.consumer.poll(1.0)
            if dataRetreived is None:
                continue
            if dataRetreived.error():
                if dataRetreived.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(dataRetreived.error())
                    break
            data = json.loads("{}".format(dataRetreived.value().decode('utf-8')))
            try:
                time.sleep(0.2)
                databaseData = ordersController.read({'_id': data['orderID']})
                if databaseData['notification'] == True:
                    print "sending only invoice to " + data['orderID']
                databaseData['invoiceURL'] = 'http://' + data['orderID']
                # del databaseData['_cls']
                # databaseData['_id'] = str(databaseData['_id'])
                ordersController.update(databaseData)
                print(data)
            except:
                # print(data)
                print('failed over here')
        self.consumer.close()