import json
import os
from confluent_kafka import Producer
import os
from dotenv import Dotenv
configurations = Dotenv('configurations.ini')
os.environ.update(configurations)

from database.controllers.orders import ordersController

controller = ordersController()

class producer:

    kafkaBootstrapServers = os.getenv('kafkaBootstrapServers')
    topics = [os.getenv('notificationTopic'), os.getenv('invoiceTopic')]

    def __init__(self):
        self.producer =  Producer({
            'bootstrap.servers': self.kafkaBootstrapServers
        })

    def produce(self,count):
        for i in range(0,count):
            orderID = controller.insert()
            for topic in self.topics:
                data = json.dumps({'orderID':orderID}).encode('utf-8')
                self.producer.produce(topic, data)
        self.producer.flush()

p1 = producer()
p1.produce(10)
