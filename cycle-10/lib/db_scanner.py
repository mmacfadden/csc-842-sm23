from .secret_detector import SecretDetector

class DatabaseScanner:

  def __init__(self, detectors: list[SecretDetector], sample_size: int) -> None:
     self.detectors = detectors
     self.sample_size = sample_size
    
  def scan(self):
      pass
  
  def detectSecret(self, value: str) -> bool:
    for detector in self.detectors:
      if detector.detectSecret(value):
        print(f"Found {detector.name}: {value}")
        return True
    
    return False