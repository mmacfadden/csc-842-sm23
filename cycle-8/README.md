# Cycle 8: TLS Certificate Analyzer
TBD

## Requirements
The main requirements of the project that influenced the functionality and design are as follows:

  * TBD

## Design
The tool was developed in Python for expediency's sake.

![TLS Handshake](assets/tls-handshake.png)

![Architecture](assets/architecture.png)

## Video
A demonstration video can be found on YouTube here:

[https://youtu.be/TBD](https://youtu.be/TBD)


## Dependencies and Setup
The project has the following dependencies:

* [Python 3](https://www.python.org/): >= 3.11.x
* [Pip](https://pip.pypa.io/en/stable/): >= 23.0


### Python Dependencies
Install the Python dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Usage
This section shows the usage of the tool:

### Help
The program help can be shown using the `-h` flag.

```bash
tls-analyzer.py -h
usage: tls-analyzer [-h] -p PCAP [-c CONFIG] [-f {text,json,html}] [-o OUTPUT] [-v]

A utility for finding anomalies in TLS within a PCAP file.

options:
  -h, --help            show this help message and exit
  -p PCAP, --pcap PCAP  The pcap file to read from
  -c CONFIG, --config CONFIG
                        Overrides the default config file name
  -f {text,json,html}, --format {text,json,html}
                        Specifies the output format
  -o OUTPUT, --output OUTPUT
                        Saves output to a file instead of standard out
  -v, --verbose         Triggers additional output while processing the pcap
```

TBD

## Config File
The tool will accept a config file that allows setting credentials for the various threat intelligence services that can be queried.  By default, The tool looks for the `config.yml` file in the current directory.  The `--config` option can be used to specify an alternate filename.

The config file is structured as follows:

```yaml
# An API Key for CrowdSec (https://www.crowdsec.net/)
crowd_sec_api_key: "<insert-api-key-here>"

# An API Key for Virus Total (https://www.virustotal.com/)
virus_total_api_key: "<insert-api-key-here>"
```