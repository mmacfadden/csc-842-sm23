from codegen import CodeGenerator;
from textwrap import dedent

class WeatherSeedCodeGenerator(CodeGenerator):
    
    def __init__(self, config) -> None:
        super().__init__()
        self._config = config

    
    def generate_js_code(self) -> str:
        lat = self._config["lat"]
        lng = self._config["lng"]
        metric = self._config["metric"]

        code = f'''
        async function getSeed(date) {{
          date = date.toISOString().split('T')[0]
          const url = `https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lng}&start_date=${{date}}&end_date=${{date}}&daily={metric}&timezone=America%2FLos_Angeles`;
          console.log(url);
          const resp = await fetch(url);
          const respJson = await resp.json();
          return respJson.daily["{metric}"][0];
        }}
        '''
        return dedent(code)
    
    def generate_py_code(config) -> str:
        return dedent(
            """"""
        )
    
def create_seed_generator(config):
    return WeatherSeedCodeGenerator(config)