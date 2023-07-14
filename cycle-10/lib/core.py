import importlib
import pkgutil

from .data_detector import DataDetector
from .db_scanner import DatabaseScanner


dirname = "lib/detectors"

def get_all_secret_detectors() -> list[DataDetector]:
  matchers = []    
  for _, package_name, _ in pkgutil.iter_modules([dirname]):
    matcher_module = importlib.import_module(f".{package_name}", package="lib.detectors")
    matchers.append(matcher_module.matcher)  

  return matchers


def get_scanner(sample_size: int, db_type: str, url: str, db_name: str, username: str, password: str, verbose: bool) -> DatabaseScanner:
    detectors = get_all_secret_detectors()

    scanner_module = importlib.import_module(f'.scanners.{db_type}', package="lib")
    scanner = scanner_module.create_scanner(detectors,
                                           sample_size,
                                           url, 
                                           db_name, 
                                           username, 
                                           password,
                                           verbose)
    return scanner    
