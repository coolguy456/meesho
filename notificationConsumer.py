import os
from dotenv import Dotenv
configurations = Dotenv('configurations.ini')
os.environ.update(configurations)
from database.controllers.orders import ordersController
from consumer import notificationQueueWorker
controller = ordersController()
notificationWorker = notificationQueueWorker()
notificationWorker.consume(controller)