#!/usr/bin/env python3

from colorama import Fore, Style

from lib.core import get_scanner
from lib.args import process_args


def main():
  """
  Ths main entry point for the Database Scavenger.
  """

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

  table_detections = scanner.scan(args.extract)

  print(f"\n{Fore.GREEN}{len(table_detections)} Tables Scanned{Style.RESET_ALL}\n")

  for table_detection in table_detections:
    if len(table_detection.detections) > 0:
      print(f"Sensitive Data Detected in Table: {Fore.RED}{table_detection.table}{Style.RESET_ALL}")
      for detection in table_detection.detections:
        print(f" - {detection.name}")

      print("")

  print(f"\n{Fore.GREEN}Database Scan Completed!{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()