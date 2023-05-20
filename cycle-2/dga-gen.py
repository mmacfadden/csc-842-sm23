#!/usr/bin/env python3

import argparse
import yaml

from dga.dga_generator import DgaGenerator

parser = argparse.ArgumentParser(
    prog='dga-gen',
    description='A utility for creating Domain Generation Algorithms'
)


parser.add_argument("config", help="The config file that determines how the DGAs will be constructed.")
parser.add_argument("output", help="The directory to output files to.")
args = parser.parse_args()


with open(args.config, 'r') as file:
  config = yaml.safe_load(file)


generator = DgaGenerator(config)
generator.generate(args.output)
