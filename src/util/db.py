from pymongo import MongoClient, ASCENDING, DESCENDING

import logging
_logger = logging.getLogger(__name__)

class InvalidDBException(Exception):
    pass

class CollectionIsExistException(Exception):
    def __init__(self, msg):
        _logger.info('collection is existed, msg=%r' % msg)
    pass

class CollectionNotExistException(Exception):
    pass

class Collection(object):
    def __init__(self, name, db):
        self.__name = name
        collection = db.get_collection(name)
        if not collection:
            collection = db.create_collection(name)
            collection.create_index([('date', ASCENDING)])
        self.__collection = collection

    def insert_and_update(self, key, value, **kwargs):
        if not self.__collection:
            raise CollectionNotExistException()
        for attr_name, attr_value in kwargs.iteritems():
            self.__collection.update_one({key: value}, 
                                        {'$set': {attr_name: attr_value}},
                                        upsert=True)

    def find(self):
        return self.__collection.find()
        
    def find_one(self, key_field, descendent=True):
        if descendent:
            cursor = self.__collection.find().sort(key_field, -1).limit(1)
        else:
            cursor = self.__collection.find().sort(key_field, 1).limit(1)
        if cursor and cursor.count() > 0:
            _logger.info('find last one record, record info=%r' % cursor[0])
            return cursor[0]
        return None
        
class DB(object):
    def __init__(self, db, host='127.0.0.1', port=27017):
        self.__conn = MongoClient(host, port)
        self.__db = self.__conn[db]

    def get_collections(self):
        if self.__db:
            return self.__db.collection_names()
        return None

    def get_collection(self, collection):
        if self.__db:
            if collection in self.__db.collection_names():
                return self.__db[collection]
        return None

    def create_collection(self, collection):
        if not self.__db:
            raise InvalidDBException

        try:
            return self.__db.create_collection(collection)
        except:
            raise CollectionIsExistException('collection(%s) is already exists' % collection)

    def drop_collection(self, collection):
        if not self.__db:
            raise InvalidDBException
        try:
            self.__db.drop_collection(collection)
        except:
            raise CollectionNotExistException()

if __name__ == "__main__":
    db = DB('stock')
    print db.get_collections()
    print db.get_collection("hello")
    try:
        db.create_collection("hello")
    except:
        pass
    collection = Collection("002657", db)
    collection.insert_and_update("date", "2016-05-30", open="17")
    collection.insert_and_update("date", "2016-05-30", close="17")
    collection.insert_and_update("date", "2016-05-31", close="17")
    collection.insert_and_update("date", "2016-05-31", open="17")
    other = {"other":"NA"}
    collection.insert_and_update("date", "2016-05-31", **other)
    print collection.find_one("date")
    print db.get_collections()
    db.drop_collection("hello")
    print db.get_collections()
