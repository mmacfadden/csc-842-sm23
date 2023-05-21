import importlib
import os

from .codegen import CodeGenerator
from .date_codegen import DateCodeGenerator
from .utils_codegen import UtilsCodeGenerator
from .main_codegen import MainCodeGenerator

class DgaGenerator():
  """
  The DgaGenerator is the main class that implements the logic of writing
  Domain Generation Algorithms.
  """
  
  def __init__(self, config: dict) -> None:
    """
     Parameters
    ----------
    config : dict
        The configuration data the controls DGA generation.
    """
    self._config = config
    pass


  def generate(self, output: str) -> None:
    print()
    
    code_generators: list[CodeGenerator] = []

    code_generators.append(self._util_generator())
    code_generators.append(self._date_generator())
    code_generators.append(self._seed_generator())
    code_generators.append(self._domain_generator())
    code_generators.append(self._main_generator())

    js_code = ""
    py_code = ""

    for code_gen in code_generators:
      js_code += code_gen.generate_js_code()
      py_code += code_gen.generate_py_code()

    os.makedirs(output, exist_ok=True)
    js_out_path = os.path.join(output, "dga.js")
    with open(js_out_path, "w") as js_output:
       js_output.write(js_code)
       print(f"JavaScript DGA output to: {js_out_path}")

    py_output_path = os.path.join(output, "dga.py")
    with open(py_output_path, "w") as py_output:
       py_output.write(py_code)
       print(f"Python DGA output to: {py_output_path}")

    print()

  def _util_generator(self) -> CodeGenerator:
    utils_code_gen = UtilsCodeGenerator()
    return utils_code_gen
    

  def _date_generator(self) -> CodeGenerator:
    frequency = self._config['frequency']
    date_codegen = DateCodeGenerator(frequency)
    return date_codegen
    

  def _seed_generator(self) -> CodeGenerator:
    seed_config_block = self._config['seed']
    seed_keys = seed_config_block.keys()
    if len(seed_keys) != 1:
      raise  Exception("seed must have exactly on key")

    seed_type = list(seed_keys)[0]
    seed_config = seed_config_block[seed_type]

    seed_gen_mod = importlib.import_module(f'.seed.{seed_type}', package="dga")
    seed_gen = seed_gen_mod.create_seed_generator(seed_config)

    return seed_gen

    
  def _domain_generator(self) -> CodeGenerator:
    domain_config_block = self._config['domain']
    domain_keys = domain_config_block.keys()
    if len(domain_keys) != 1:
      raise  Exception("domain must have exactly on key")

    domain_type = list(domain_keys)[0]
    domain_config = domain_config_block[domain_type]

    domain_gen_mod = importlib.import_module(f'.domain.{domain_type}', package="dga")
    domain_gen = domain_gen_mod.create_domain_generator(domain_config)
    
    return domain_gen

    
  def _main_generator(self) -> CodeGenerator:
    domains_per_tld = self._config["domains-per-tld"]
    tlds = str(self._config["top-level-domains"])

    main_names = {}
    for lang, config in self._config.get("languages", {}).items():
      function_name = config.get("function-name")
      if function_name != None:
        main_names[lang] = function_name
      
    main_codegen = MainCodeGenerator(tlds, domains_per_tld, main_names)
    return main_codegen
  