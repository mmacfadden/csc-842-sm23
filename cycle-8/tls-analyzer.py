#!/usr/bin/env python3

from lib.analyzer import analyze_pcap
from lib.args import process_args


def main():
  args = process_args()

  analyze_pcap(args.pcap)

if __name__ == "__main__":  
  main()
