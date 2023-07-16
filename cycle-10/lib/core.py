import importlib
import pkgutil

from .data_detector import DataDetector
from .abstract_database_scanner import AbstractDatabaseScanner
from .util import fatal_error


def __get_all_data_detectors() -> list[DataDetector]:
  """
  A helper method to dynamically load all data detectors
  from the lib/detectors director.
  """
  detectors = []    
  for _, package_name, _ in pkgutil.iter_modules(["lib/detectors"]):
    module = importlib.import_module(f".{package_name}", package="lib.detectors")
    detectors.append(module.detector)  

  return detectors


def get_scanner(sample_size: int, 
                db_type: str,
                url: str,
                db_name: str, 
                username: str, 
                password: str, 
                verbose: bool) -> AbstractDatabaseScanner:
    """
    Creates a data scanner for a particular type of database. The module
    is dynamically loaded based on the database type.

    Parameters:
      sample_size:
        The number of records to query from the database when detecting data.
      db_type: 
        The type of database that is to be scanned.
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
    detectors = __get_all_data_detectors()

    try:
      scanner_module = importlib.import_module(f'.scanners.{db_type}', package="lib")
      scanner = scanner_module.create_scanner(detectors,
                                             sample_size,
                                             url, 
                                             db_name, 
                                             username, 
                                             password,
                                             verbose)
      return scanner
    except ModuleNotFoundError:
       fatal_error(f"Unrecognized database type: {db_type}")
