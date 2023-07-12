from pymongo import MongoClient

from ..secret_detector import SecretDetector
from ..db_scanner import DatabaseScanner

class MongoDbScanner(DatabaseScanner):

  def __init__(self, 
               detectors: list[SecretDetector],
               sample_size: int,
               url: str,
               db_name: str,
               username: str,
               password: str) -> None:
    super().__init__(detectors, sample_size)
    self.url = url
    self.db_name = db_name
    self.username = username
    self.password = password

  def scan(self):
    client = MongoClient(self.url, username=self.username, password=self.password)
    db = client[self.db_name]
    self.iterateCollections(db)

  def iterateCollections(self, database):
    collections = database.list_collection_names()
    for collectionName in collections:
      self.scanCollection(database[collectionName])


  def scanCollection(self, collection):
    docs = collection.find()
    for doc in docs:
      self.scanValues(doc)


  def scanValues(self, x: any):
     if isinstance(x, list):
        for v in x:
          self.scanValues(v)

     elif isinstance(x, dict):
       for k, v in x.items():
         self.scanValues(v)

     elif isinstance(x, str):
       return self.detectSecret(x)
