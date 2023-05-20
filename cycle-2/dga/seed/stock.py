from ..codegen import CodeGenerator;
from textwrap import dedent

class StockSeedCodeGenerator(CodeGenerator):
    
    def __init__(self, config) -> None:
        super().__init__()
        self._config = config

    
    def generate_js_code(self) -> str:
        stock_symbol = self._config["symbol"]

        code = f'''
        async function getSeed(date) {{
          date = date.toISOString().split('T')[0]
          const url = `https://api.marketdata.app/v1/stocks/candles/D/{stock_symbol}/?countback=1&to=${{date}}&dateformat=timestamp`;
          const resp = await fetch(url);
          const respJson = await resp.json();
          return Math.floor(respJson.c[0] * 10);
        }}
        '''
        return dedent(code)
    
    def generate_py_code(self) -> str:
        stock_symbol = self._config["symbol"]

        return dedent(
            f"""
            import urllib.request, json, math
            def get_seed(date):             
              url = f"https://api.marketdata.app/v1/stocks/candles/D/{stock_symbol}/?countback=1&to={{str(date)}}&dateformat=timestamp"
              response = urllib.request.urlopen(url)
              data = json.loads(response.read())
              return math.floor(data["c"][0] * 10)
            """
        )
    

def create_seed_generator(config):
    return StockSeedCodeGenerator(config)