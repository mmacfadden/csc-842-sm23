from pymongo import MongoClient

from ..secret_detector import SecretDetector
from ..db_scanner import DatabaseScanner, TableDetections


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

  def scan(self) -> list[TableDetections]:
    detections = []
    client = MongoClient(self.url, username=self.username, password=self.password)
    database = client[self.db_name]
    collections = database.list_collection_names()
    for collectionName in collections:
      collection_detections = self.scanCollection(database[collectionName])
      if collection_detections != None:
        detections.append(collection_detections)
    
    return detections


  def scanCollection(self, collection) -> TableDetections:
    docs = collection.find().limit(self.sample_size)
    for doc in docs:
      detections = self.scanValues(doc)
      ## TODO make it so that we actually aggregate these and de-duplicate
      ## across samples
      if len(detections) > 0:
        return (TableDetections(collection.name, detections))
      
    return None

  def scanValues(self, x: any):
    detections = []
    if isinstance(x, list):
      for v in x:
        detections.extend(self.scanValues(v))
         

    elif isinstance(x, dict):
      for _, v in x.items():
        detections.extend(self.scanValues(v))
      

    elif isinstance(x, str):
      detections.extend(self.detectSecret(x))


    return detections
