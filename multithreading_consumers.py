from database.controllers.orders import ordersController
from consumer import invoiceQueueWorker
controller = ordersController()
global size
size = 10
import threading
from Queue import Queue
list = [10]

def up(i,list):
    invoiceWorker = invoiceQueueWorker(i)
    invoiceWorker.consume(controller,list)
for i in range(0,list[0]):
    t1 = threading.Thread(target=up, args=(i,list))
    print(threading.active_count())
    t1.start()

list[0] = 1
import time
for i in range(0,100):
    time.sleep(1.0)
    print(threading.active_count())