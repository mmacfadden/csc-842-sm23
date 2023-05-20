from codegen import CodeGenerator;
from textwrap import dedent

class RandomDomainGen(CodeGenerator):
    
    def __init__(self, config) -> None:
        super().__init__()
        self._config = config

    
    def generate_js_code(self) -> str:
        length = self._config["length"]

        code = f'''
        function generateDomain(domainIndex, seed) {{
          const valid_domain_chars = "1q3ag0n8fslwkti4u6952yzbvhdpocm7ej-rx";

          let i = 0;
          let idx = (seed + domainIndex) % validDomainChars.length;
          let domain = "";

          while (true) {{
            if (i >= {length}) {{
              break;
            }}
            const ch = validDomainChars.charAt(idx);
            domain += ch;
            idx = ch.charCodeAt(0) + i;
            
            idx = idx % validDomainChars.length;

            i++;
          }}
          
          return domain;
        }}
        '''
        return dedent(code)
    
    def generate_py_code(self) -> str:
        length = self._config["length"]
        return dedent(
            f"""
            valid_domain_chars = "1q3ag0n8fslwkti4u6952yzbvhdpocm7ej-rx"

            def generate_domain(domain_index, seed):
              i = 0
              idx = (seed + domain_index) % len(valid_domain_chars)
              domain = ""

              while True:
                if i >= {length}:
                  break
               
                ch = valid_domain_chars[idx]
                domain += ch

                idx = ord(ch) + i
                idx = idx % len(valid_domain_chars)
                i = i + 1
              
              return domain
            """
        )
    
def create_domain_generator(config):
  return RandomDomainGen(config)