from pymongo import MongoClient


class StorageManager:

        def __init__(self, address, port, database_name):
            print('mongo init')
            self.client = MongoClient(address, port)
            self.db = self.client[database_name]

        def insert(self, collection_name, data):
            return self.db[collection_name].insert(data)

        def save(self, collection_name, data):
            return self.db[collection_name].save(data)

        def remove(self, collection_name, query):
            return self.db[collection_name].remove(query)

        def find(self, collection_name, query, projection=None, limit=0, skip_num=0, sort=None):
            if sort:
                data = self.db[collection_name].find(query, projection).skip(skip_num).limit(limit).sort(sort)
            else:
                data = self.db[collection_name].find(query, projection).skip(skip_num).limit(limit)
            return data

        def update(self, collection_name, query, update):
            return self.db[collection_name].update(query, update, upsert=False, multi=True)

        def count(self, collection_name):
            return self.db[collection_name].count()

        def distinct(self, collection_name, field, query):
            return self.db[collection_name].distinct(field, query)


if __name__ == "__main__":
    ip = '10.0.3.23'
    port = 27017
    db = 'test'

    sm = StorageManager(ip, port, db)
    print(sm.insert('test', {'id': 'test'}))
