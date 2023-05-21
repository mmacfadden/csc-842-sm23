#!/usr/bin/env python3

import argparse
import yaml
import os

from dga.dga_generator import DgaGenerator

##
## Argument Processing
##
parser = argparse.ArgumentParser(
    prog='dga-builder',
    description='A utility for building Domain Generation Algorithms'
)

parser.add_argument("config", help="The config file that determines how the DGAs will be constructed.")
parser.add_argument("output", help="The directory to output files to.")
args = parser.parse_args()


##
## Read the config file
##
if not os.access(args.config, os.R_OK):
  print(f"Error: Config file not found: {args.config}")
  exit(1)

with open(args.config, 'r') as file:
  config = yaml.safe_load(file)


##
## Generate Code
##
generator = DgaGenerator(config)
generator.generate(args.output)
