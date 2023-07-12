from dataclasses import dataclass

from .secret_detector import SecretDetector



@dataclass
class Detection:
   name: str
   example_value: str


@dataclass
class TableDetections:
   table: str
   detections: list[Detection]
   

class DatabaseScanner:

  def __init__(self, detectors: list[SecretDetector], sample_size: int) -> None:
     self.detectors = detectors
     self.sample_size = sample_size
    
  def scan(self) -> list[TableDetections]:
      pass
  
  
  def detectSecret(self, value: str) -> list[Detection]:
    detections = []

    for detector in self.detectors:
      if detector.detectSecret(value):
        detections.append(Detection(detector.name, value))

    return detections