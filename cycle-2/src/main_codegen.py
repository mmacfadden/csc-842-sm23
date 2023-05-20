from codegen import CodeGenerator;
from textwrap import dedent;

class MainCodeGenerator(CodeGenerator):
    
    def __init__(self, tlds, domains_per_tld, main_names) -> None:
        super().__init__()
        self._tlds = tlds
        self._domains_per_tld = domains_per_tld
        self._main_names: dict = main_names

    
    def generate_js_code(self) -> str:
      main =  self._main_names.get("javascript", "generateDomains")
      return dedent(
        f"""
        const tlds = {self._tlds};

        async function {main}() {{
          const domains = [];
          let domainIdx = 0;

          const dates = getDates();

          for (d of dates) {{
            const seed = await getSeed(d);
            for (let tld of tlds) {{
              for (let i = 0; i < {self._domains_per_tld}; i++) {{
                const domain = generateDomain(domainIdx++, seed);
                domains.push(domain + "." + tld);
              }}
            }}
          }}
          
          return domains;
        }}

         {main}().then(p => console.log(p)).catch(e => console.error(e));
        """  
      )
    
    def generate_py_code(self) -> str:
        main =  self._main_names.get("python", "generateDomains")

        return dedent(
            f"""
            tlds = {self._tlds}

            def {main}():
              domains = []
              domain_idx = 0

              dates = get_dates()

              for d in dates:
                seed = get_seed(d)
                for tld in tlds:
                  for  i in range(0, {self._domains_per_tld}):
                    domain = generate_domain(domain_idx, seed)
                    domain_idx = domain_idx + 1
                    domains.append(domain + "." + tld)
                   
              return domains
            

            print( {main}())
            """
        )