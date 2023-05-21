#!/usr/bin/env python3

import importlib, sys

dga_file = sys.argv[1]
dga_mod_name = dga_file.replace("/", ".").replace("\\", ".")

dga_mod = importlib.import_module(dga_mod_name, package = "dga")

print("\n".join(dga_mod.generate_domains()))