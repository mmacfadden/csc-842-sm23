from dataclasses import dataclass
from typing import Optional
from .data_detector import DataDetector

@dataclass
class Detection:
   """
   The Detection class signifies that a certain Data Detector
   has found matching data in a table / collection.  The detection
   identifies the name of the detector that matched the data and
   an example of the data that was found.
   """

   name: str
   example_value: str


@dataclass
class TableDetections:
   """
   The TableDetections records which detections (if any) were found
   in a given table (or collection, etc.).
   """
   table: str
   detections: list[Detection]
   

class AbstractDatabaseScanner:
  """
  The AbstractDatabaseScanner is the base class of all database scanner
  and provides the core logic for looking through a database to detect
  data of interest.
  """

  def __init__(self, 
               detectors: list[DataDetector], 
               sample_size: int,
               url: str,
               db_name: str,
               username: str,
               password: str,
               verbose: bool) -> None:
    """
    Creates a new SQL Based Database scanner.

    Parameters:
      detectors:
        The set of data detectors to scan the database with.
      sample_size:
        The number of records to query from the database when detecting data.
      url:
        The url to connect to the database with (generally a host name and port)
      db_name:
        The name of the database / schema to connect to.
      username:
        The username of the user to authenticate with.
      password:
        The password of the user to connect with.
      verbose:
        Whether or not to output additional information.
    """

    self.detectors = detectors
    self.sample_size = sample_size
    self.url = url
    self.db_name = db_name
    self.username = username
    self.password = password
    self.verbose = verbose
    

  def scan(self, extract_dir: Optional[str]) -> list[TableDetections]:
    """
    This is the main 'interface' method for the AbstractDatabaseScanner. This
    method will scan the configured database for data of interest and return
    the results.

    Parameters:
      extract_dir:
        If set to a string value (instead of None), the the scan method
        will also extract the interesting data it finds to the specified
        directory.
    """
    raise Exception("The 'scan' method must be overridden by subclasses")
  
  
  ##
  ## Method intended to be used by subclasses.
  ##

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