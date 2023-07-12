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

scanner.scan()