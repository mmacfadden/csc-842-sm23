#!/usr/bin/env python3

import argparse
import yaml
import importlib
import os

from codegen import CodeGenerator
from date_codegen import DateCodeGenerator
from utils_codegen import UtilsCodeGenerator
from main_codegen import MainCodeGenerator


parser = argparse.ArgumentParser(
                    prog='dga-gen',
                    description='What the program does',
                    epilog='Text at the bottom of help')


parser.add_argument("config", help="foo")

parser.add_argument("output", help="The directory to output files to.")

args = parser.parse_args()


with open(args.config, 'r') as file:
  config = yaml.safe_load(file)


code_generators: list[CodeGenerator] = []

##
## Utils
## 
utils_code_gen = UtilsCodeGenerator()
code_generators.append(utils_code_gen)

##
## Dates
##
frequency = config['frequency']

date_codegen = DateCodeGenerator(frequency)
code_generators.append(date_codegen)


##
## Seed
## 

seed_config_block = config['seed']
seed_keys = seed_config_block.keys()
if len(seed_keys) != 1:
  raise  Exception("seed must have exactly on key")

seed_type = list(seed_keys)[0]
seed_config = seed_config_block[seed_type]

seed_gen_mod = importlib.import_module(f'seed.{seed_type}')
seed_gen = seed_gen_mod.create_seed_generator(seed_config)

code_generators.append(seed_gen)


##
## domain
##
domain_config_block = config['domain']
domain_keys = domain_config_block.keys()
if len(domain_keys) != 1:
  raise  Exception("domain must have exactly on key")

domain_type = list(domain_keys)[0]
domain_config = domain_config_block[domain_type]

domain_gen_mod = importlib.import_module(f'domain.{domain_type}')
domain_gen = domain_gen_mod.create_domain_generator(domain_config)

code_generators.append(domain_gen)


##
## Main
##
domains_per_tld = config["domains-per-tld"]
tlds = str(config["top-level-domains"])
main_codegen = MainCodeGenerator(tlds, domains_per_tld)
code_generators.append(main_codegen)


##
## Codegen
##
js_code = ""
py_code = ""

for code_gen in code_generators:
  js_code += code_gen.generate_js_code()
  py_code += code_gen.generate_py_code()

os.makedirs(args.output, exist_ok=True)
with open(os.path.join(args.output, "dga.js"), "w") as js_output:
   js_output.write(js_code)

with open(os.path.join(args.output, "dga.py"), "w") as py_output:
   py_output.write(py_code)