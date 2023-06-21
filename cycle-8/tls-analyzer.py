#!/usr/bin/env python3

from lib.analyzer import CertificateAnalyzer
from lib.args import process_args


def main():
  args = process_args()

  
  analyzer = CertificateAnalyzer(args.pcap)
  result = analyzer.analyze()

  print(result)

if __name__ == "__main__":  
  main()
