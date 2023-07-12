import importlib
import pkgutil

from .secret_detector import SecretDetector
dirname = "lib/detectors"

def get_all_secret_detectors() -> list[SecretDetector]:
  matchers = []    
  for _, package_name, _ in pkgutil.iter_modules([dirname]):
    matcher_module = importlib.import_module(f".{package_name}", package="lib.detectors")
    matchers.append(matcher_module.matcher)  

  return matchers
  