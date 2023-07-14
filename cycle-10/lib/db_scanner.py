from dataclasses import dataclass

from .data_detector import DataDetector


@dataclass
class Detection:
   name: str
   example_value: str


@dataclass
class TableDetections:
   table: str
   detections: list[Detection]
   

class DatabaseScanner:

  def __init__(self, 
               detectors: list[DataDetector], 
               sample_size: int,
               url: str,
               db_name: str,
               username: str,
               password: str,
               verbose: bool) -> None:
     self.detectors = detectors
     self.sample_size = sample_size
     self.url = url
     self.db_name = db_name
     self.username = username
     self.password = password
     self.verbose = verbose
    

  def scan(self) -> list[TableDetections]:
      raise Exception("The 'scan' method must be overridden by subclasses")
  
  
  def _detect_data(self, value: str) -> list[Detection]:
    detections = []

    for detector in self.detectors:
      if detector.detect(value):
        detections.append(Detection(detector.name, value))

    return detections
  
  def _scan_value(self, x: any):
    detections = []
    if isinstance(x, list):
      for v in x:
        detections.extend(self._scan_value(v))

    elif isinstance(x, dict):
      for _, v in x.items():
        detections.extend(self._scan_value(v))

    elif isinstance(x, str):
      detections.extend(self._detect_data(x))

    return detections

  def _log(self, message: str) -> None:
    if self.verbose:
       print(message)