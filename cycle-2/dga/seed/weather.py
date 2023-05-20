from ..codegen import CodeGenerator;
from textwrap import dedent

class WeatherSeedCodeGenerator(CodeGenerator):
    """
    WeatherSeedCodeGenerator generates a random seed from historical weather
    data.
    """
    
    def __init__(self, config) -> None:
        super().__init__()
        self._lat = config["lat"]
        self._lng = config["lng"]
        self._metric = config["metric"]

    
    def generate_js_code(self) -> str:
        code = f'''
        async function getSeed(date) {{
          date = date.toISOString().split('T')[0]
          const url = `https://archive-api.open-meteo.com/v1/archive?latitude={self._lat}&longitude={self._lng}&start_date=${{date}}&end_date=${{date}}&daily={self._metric}&timezone=America%2FLos_Angeles`;
          const resp = await fetch(url);
          const respJson = await resp.json();
          return Math.floor(respJson.daily["{self._metric}"][0] * 10);
        }}
        '''
        return dedent(code)
    
    def generate_py_code(self) -> str:
        return dedent(
          f"""
          import urllib.request, json, math
          def get_seed(date):
            url = f"https://archive-api.open-meteo.com/v1/archive?latitude={self._lat}&longitude={self._lng}&start_date={{str(date)}}&end_date={{str(date)}}&daily={self._metric}&timezone=America%2FLos_Angeles"
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
            return math.floor(data["daily"]["{self._metric}"][0] * 10)
          """
        )
    
def create_seed_generator(config):
    return WeatherSeedCodeGenerator(config)