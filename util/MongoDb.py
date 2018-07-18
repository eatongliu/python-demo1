from pymongo import MongoClient

from util import Properties


class MongoDb:

    def __init__(self):
        p = Properties.Properties('config/mongo.properties').getProperties()
        # 与MongDB建立连接（这是默认连接本地MongDB数据库）
        # "mongodb://root:****@dds-bp1cec91a1b9f4141122-pub.mongodb.rds.aliyuncs.com:3717,dds-bp1cec91a1b9f4142123-pub.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-5277667"
        uri = 'mongodb://' + p.get('username') + ':' + p.get('password') + '@' + p.get('hosts') + '/pydata01?replicaSet=mgset-5277667'
        client = MongoClient(uri)
        # client = MongoClient(p.get('hosts').split(','))
        # 选择一个数据库
        db = client[p.get('database')]
        self.collection = db[p.get('collection')]

    def save(self, obj):
        self.collection.save(obj)

    def find_one(self, kv):
        self.collection.find_one(kv)


mongoDb = MongoDb()
