from ..codegen import CodeGenerator;
from textwrap import dedent

class WordListDomainGen(CodeGenerator):
    """
    WordListDomainGen generates domains based on a supplied list of words.
    """
    
    def __init__(self, config) -> None:
        super().__init__()
        self._count = config["count"]
        self._word_list = config["word-list"]
        self._separator = config["separator"]

    
    def generate_js_code(self) -> str:
        code = f'''   
        function generateDomain(domainIndex, seed) {{
          const words = {str(self._word_list)};
          const count = {self._count};

          let i = 0;
          let idx = (seed + domainIndex) % words.length;
          let domain = "";

          while (true) {{
            if (i >= {self._count}) {{
              break;
            }}
            
            domain += words[idx];
            if (i < count - 1 && {str(self._separator).lower()}) {{
              domain += "-";
            }}
                 

            idx = (domain.length + i) % words.length;
            i++;
          }}
          
          return domain;
        }}
        '''
        return dedent(code)
    
    def generate_py_code(self) -> str:
        return dedent(
            f"""
            def generate_domain(domain_index, seed):
              words = {str(self._word_list)}
              i = 0
              idx = (seed + domain_index) % len(words)
              domain = ""

              count = {self._count}
              while True:
                if i >= count:
                  break
               
                domain += words[idx]

                if i < count - 1 and {self._separator}:
                 domain += "-"

                idx = len(domain) + i
                idx = idx % len(words)
                i = i + 1
              
              return domain
            """
        )
    
def create_domain_generator(config):
  return WordListDomainGen(config)