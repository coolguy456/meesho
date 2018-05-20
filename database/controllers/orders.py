import redis_lock
from __init__ import *
from database.models.orders import Orders
from bson import ObjectId
import json

class ordersController:

    def __init__(self):
        self.conn = conn

    def insert(self):
        order = Orders().save()
        return str(order._id)

    def update(self,data):
        id = data['_id']
        redisData = conn.get(id)
        if redisData == None:
            try:
                lock = redis_lock.Lock(conn,id)
                lock.acquire(blocking=True)
                order = Orders.objects.get({'_id': ObjectId(id)})
                order.notification = data.get("notification",order.notification)
                order.invoiceURL = data.get("invoiceURL",order.invoiceURL)
                order.save()
                conn.set(id, json.dumps(data))
                lock.release()
            except:
                print 'error in updating orders collection'
        else:
            conn.set(id,json.dumps(data))
            try:
                lock = redis_lock.Lock(conn,id)
                lock.acquire(blocking=True)
                order = Orders.objects.get({'_id': ObjectId(id)})
                order.notification = data.get("notification",order.notification)
                order.invoiceURL = data.get("invoiceURL",order.invoiceURL)
                order.save()
                lock.release()
            except:
                print 'error in updating orders collection'

    def read(self,data):
        id = data['_id']
        redisData = conn.get(id)
        if redisData == None:
            try:
                lock = redis_lock.Lock(conn, id)
                lock.acquire(blocking=True)
                order = Orders.objects.get({'_id': ObjectId(id)})
                data = order.to_son().to_dict()
                data['_id'] = str(data['_id'])
                del data['_cls']
                conn.set(id,json.dumps(data))
                lock.release()
                return data
            except:
                print 'error in reading from orders collection'
        else:
            print(redisData)
            ss = json.loads(redisData)
            return json.loads(redisData)