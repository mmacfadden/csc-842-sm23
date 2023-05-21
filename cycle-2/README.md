# Cycle 2: Domain Generation Algorithm Builder
This project provides a [Domain Generation Algorithm](https://en.wikipedia.org/wiki/Domain_generation_algorithm) (DGA) Builder.  DGAs are often used by malware to connect back to a command and control server.  The DGA Builder simplifies and automates building DGAs across multiple languages.  A configuration file specifies how the DGA should be constructed and the DGA Builder then generates code to implement a DGA using those options.

The project was built using Python 3.11.


## Requirements

## Design

![Architecture](assets/architecture.png)

## Video
A demonstration video can be found on YouTube here:

http://youtube.com


## Running
The DGA Builder can be run by executing the [dga-builder.py](dga-builder.py) script.  The command line script takes a configuration file as an input as well as the directory to output generated DGAs to.

The command line script has a built-in help menu that can be displayed using `-h` option.

```bash
./dga-builder.py -h
usage: dga-builder [-h] config output

A utility for building Domain Generation Algorithms

positional arguments:
  config      The config file that determines how the DGAs will be constructed.
  output      The directory to output files to.

options:
  -h, --help  show this help message and exit
```

The DGA Builder can be run using one of the example config files located in the [example-config](example-config) directory.

```bash
./dga-builder.py example-configs/weather-words.yml out

JavaScript DGA output to: out/dga.js
Python DGA output to: out/dga.py

```

## Config File

```yaml
# Specifies which top-level domains to generate domains within.
top-level-domains:
  - re
  - ru
  - xyz
  - za

# How many domains to generate per top-level domain.
domains-per-tld: 2

# How frequently should the domains be rotated. Valid values are 'week' and 'month'.
# Whichever value is chosen, the DGAs will use the current and previous periods so
# that two periods are always active.
frequency: week  

# Specifies the method that should be used to obtain the random seed for domain
# generation.
#
# Note: Only one seed method should be used, although all are shown here together.
seed:

  # Use historical stock price to generate domains. The stock symbol is specified.
  stock:
    symbol: AAPL
  
  # Use historical weather information to generate domains. The method takes a
  # latitude and longitude (in decimal format) of a location to get the historical
  # weather for, along with a metric to use. Valid metrics are:
  #   - temperature_2m_max
  #   - temperature_2m_min
  weather:
    lat: 52.52
    lng: 13.41
    metric: temperature_2m_max

# Specifies the method that should be used to generate domain names given the
# random seed.
#
# Note: Only one seed method should be used, although all are shown here together.
domain:

  # Generates pseudorandom domains of a specified length.
  random:
    length: 10

  # Generates domains from a word list.
  words:
    count: 4
    separator: true
    word-list:
      - extravagant
      - gravitational
      - idiomatic
      - foundationalism
      - polysyllabic
      - subordinating
      - goldenberries
      - sycophantic
      - metabolism
      - ontological
      - disestablishment
      - jurisprudence
      - fantastical
      - expeditionary
      - subliminal
      - stratospheric
      - conjunctions
      - geothermal
      - intergalactic
      - supersonic

# Configures language specific options.
languages:
  javascript:
    function-name: generateDomains
  python:
    function-name: generate_domains
```
