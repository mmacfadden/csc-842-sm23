from pymongo import MongoClient
from colorama import Fore, Style
from ..secret_detector import SecretDetector
from ..db_scanner import DatabaseScanner, TableDetections


class MongoDbScanner(DatabaseScanner):

  def __init__(self, 
               detectors: list[SecretDetector],
               sample_size: int,
               url: str,
               db_name: str,
               username: str,
               password: str,
               verbose: bool) -> None:
    super().__init__(detectors, sample_size, url, db_name, username, password, verbose)


  def scan(self) -> list[TableDetections]:
    detections = []

    self._log(f"{Fore.YELLOW}Connecting to MySQL{Style.RESET_ALL}: {self.url}")
    client = MongoClient(self.url, username=self.username, password=self.password)
    self._log(f"{Fore.GREEN}Successfully Connected.{Style.RESET_ALL}")
    
    database = client[self.db_name]
    collections = database.list_collection_names()
    for collectionName in collections:
      collection_detections = self.scan_collection(database[collectionName])
      if collection_detections != None:
        detections.append(collection_detections)
    
    return detections


  def scan_collection(self, collection) -> TableDetections:
    detections = {}
    docs = collection.find().limit(self.sample_size)
    for doc in docs:
      new_detections = self.scan_values(doc)
      for nd in new_detections:
        if not nd.name in detections:
          detections[nd.name] = nd
      
    return TableDetections(collection.name, detections.values())

  def scan_values(self, x: any):
    detections = []
    if isinstance(x, list):
      for v in x:
        detections.extend(self.scan_values(v))

    elif isinstance(x, dict):
      for _, v in x.items():
        detections.extend(self.scan_values(v))

    elif isinstance(x, str):
      detections.extend(self.detect_secret(x))

    return detections
  

def create_scanner(detectors: list[SecretDetector],
                  sample_size: int,
                  url: str, 
                  db_name: str, 
                  username: str, 
                  password: str,
                  verbose: bool) -> MongoDbScanner:
  
  return MongoDbScanner(detectors, sample_size, url, db_name, username, password, verbose)
