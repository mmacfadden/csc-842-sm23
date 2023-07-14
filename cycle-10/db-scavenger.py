#!/usr/bin/env python3

from lib.core import get_scanner
from lib.scanners.mongodb import MongoDbScanner
from lib.args import process_args

from colorama import Fore, Style

args = process_args()

scanner = get_scanner(
  args.sample_size,
  args.type,
  args.server,
  args.database,
  args.username,
  args.password,
  args.verbose
)

table_detections = scanner.scan()

print(f"\n{Fore.GREEN}{len(table_detections)} Tables Scanned{Style.RESET_ALL}\n")

for table_detection in table_detections:
  if len(table_detection.detections) > 0:
    print(f"Secrets Detected in Table: {Fore.RED}{table_detection.table}{Style.RESET_ALL}")
    for detection in table_detection.detections:
      print(f" - {detection.name}")

    print("")
