from codegen import CodeGenerator;
from textwrap import dedent;

class UtilsCodeGenerator(CodeGenerator):
    
    def __init__(self) -> None:
        super().__init__()

    
    def generate_js_code(self):
       return dedent(
       """
       function unpackString(arr) {{
          const u8 = new Uint8Array(arr.buffer);
          const idx = u8.findIndex((i) => i === 0);
          const unpadded = u8.slice(0, idx);
          const td = new TextDecoder();
          const str = td.decode(unpadded);
          return str;
       }}
       """    
       )
            
       
    
    def generate_py_code(config):
        return ""