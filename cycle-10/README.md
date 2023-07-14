# Cycle 10: TBD



## Requirements
The main requirements of the project that influenced the functionality and design are as follows:

  * TBD

## Design
The tool was developed in Python for expediency's sake.

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
./db-scavenger.py -h
usage: db-scavenger [-h] -t TYPE [-n SAMPLE_SIZE] -s SERVER -d DATABASE -u USERNAME -p PASSWORD [-e EXTRACT] [-v]

A tool that searches a database for sensitive data and supports extracting data of interest.

options:
  -h, --help            show this help message and exit
  -t TYPE, --type TYPE  Specifies the configuration file
  -n SAMPLE_SIZE, --sample-size SAMPLE_SIZE
                        Specifies the configuration file
  -s SERVER, --server SERVER
                        Specifies the configuration file
  -d DATABASE, --database DATABASE
                        Specifies the configuration file
  -u USERNAME, --username USERNAME
                        The username to log into the database with.
  -p PASSWORD, --password PASSWORD
                        Specifies the configuration file
  -e EXTRACT, --extract EXTRACT
                        Saves output to a file instead of standard out
  -v, --verbose         Triggers additional output
```

### MySQL
```bash
./db-scavenger.py -t mysql -s "localhost" -d csc842 -u admin -p admin -v
```

### MongoDB
```bash
./db-scavenger.py -t mongodb -s "localhost" -d csc842 -u admin -p admin -v
```

### PostgreSQL
```bash
./db-scavenger.py -t postgres -s "localhost" -d csc842 -u admin -p admin -v
```
