import os
from dotenv import Dotenv
configurations = Dotenv('configurations.ini')
os.environ.update(configurations)
from database.controllers.orders import ordersController
from consumer import invoiceQueueWorker
controller = ordersController()
invoiceWorker = invoiceQueueWorker()
invoiceWorker.consume(controller)