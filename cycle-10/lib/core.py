import importlib
import pkgutil

from .data_detector import DataDetector
from .abstract_database_scanner import AbstractDatabaseScanner
from .util import fatal_error




def get_all_secret_detectors() -> list[DataDetector]:
  detectors = []    
  for _, package_name, _ in pkgutil.iter_modules(["lib/detectors"]):
    module = importlib.import_module(f".{package_name}", package="lib.detectors")
    detectors.append(module.detector)  

  return detectors


def get_scanner(sample_size: int, db_type: str, url: str, db_name: str, username: str, password: str, verbose: bool) -> AbstractDatabaseScanner:
    detectors = get_all_secret_detectors()

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
