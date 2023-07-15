from typing import Optional
from pymongo import MongoClient
from colorama import Fore, Style
from ..data_detector import DataDetector
from ..abstract_database_scanner import AbstractDatabaseScanner, TableDetections
from ..util import fatal_error
import os
import json


class MongoDbScanner(AbstractDatabaseScanner):

  def __init__(self, 
               detectors: list[DataDetector],
               sample_size: int,
               url: str,
               db_name: str,
               username: str,
               password: str,
               verbose: bool) -> None:
    super().__init__(detectors, sample_size, url, db_name, username, password, verbose)


  def scan(self, extract_dir: Optional[str]) -> list[TableDetections]:
    detections = []

    self._log(f"{Fore.YELLOW}Connecting to MySQL{Style.RESET_ALL}: {self.url}")
    client = MongoClient(self.url, 
                         username=self.username, 
                         password=self.password,
                         serverSelectionTimeoutMS=5000)

    try:
      client.server_info()
      self._log(f"{Fore.GREEN}Successfully Connected.{Style.RESET_ALL}")
    except Exception as e:
      fatal_error(f"Could not connect to MySQL: {e}")
    
    
    database = client[self.db_name]
    collections = database.list_collection_names()
    for collectionName in collections:
      collection = database[collectionName]
      collection_detections = self._scan_collection(collection)
      if collection_detections != None:
        detections.append(collection_detections)

        if extract_dir != None:
          self._extract_collection(collection, extract_dir)
    
    return detections


  def _scan_collection(self, collection) -> TableDetections:
    detections = {}
    docs = collection.find().limit(self.sample_size)
    for doc in docs:
      new_detections = self._scan_value(doc)
      for nd in new_detections:
        if not nd.name in detections:
          detections[nd.name] = nd
      
    return TableDetections(collection.name, detections.values())
  
  def _extract_collection(self, collection, extract_dir: Optional[str]) -> None:
    os.makedirs(extract_dir, exist_ok=True)
    collection_file = os.path.join(extract_dir, f"{collection.name}.json")
    
    with open(collection_file, "w") as out:
      out.write("[")
      docs = collection.find()
      
      first = True
      for doc in docs:
        if not first:
          out.write(",")
        
        first = False

        out.write("\n  ")
        del doc["_id"]
        out.write(json.dumps(doc))
        
      out.write("\n]")
  


def create_scanner(detectors: list[DataDetector],
                  sample_size: int,
                  url: str, 
                  db_name: str, 
                  username: str, 
                  password: str,
                  verbose: bool) -> MongoDbScanner:
  
  return MongoDbScanner(detectors, sample_size, url, db_name, username, password, verbose)
