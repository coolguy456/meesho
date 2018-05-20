from pymodm import MongoModel, fields

class Orders(MongoModel):
    notification = fields.BooleanField(default = False)
    invoiceURL = fields.CharField(default = "null")
    userId = fields.CharField(default = "rootuser")
