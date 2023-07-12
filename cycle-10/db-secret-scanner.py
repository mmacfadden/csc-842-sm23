#!/usr/bin/env python3


from lib.core import get_all_secret_detectors

from lib.scanners.mongodb import MongoDbScanner

detectors = get_all_secret_detectors()

scanner = MongoDbScanner(
    detectors,
    5,
    "localhost",
    "csc842",
    "admin",
    "admin"
)

detections = scanner.scan()

for detection in detections:
  print(f"Secrets Detected in Table: {detection.table}")
  for td in detection.detections:
    print(f" - {td.name}")

  print("")
