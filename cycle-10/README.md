# Cycle 10: Databases Scavenger
The Database Scavenger is tool / framework that searches Databases for data of interest.  Examples include AWS Access Keys, emails, Social Security numbers, etc.  The tool supports multiple databases and is easily extendable to search for various kinds of data.  The tool also has the ability to extract the data it identifies as interesting.

The objective is to quickly identify and extract data from a database that is unfamiliar to you, either to understand if your database has sensitive data (defensive cyber) or to find an exfiltrate sensitive data (offensive cyber).

The currently supported databases include:

  * MySQL
  * PostgreSQL
  * MongoDB


## Requirements
The main requirements of the project that influenced the functionality and design are as follows:

  * The tool must support multiple SQL and NoSQL databases.
  * The tool must be easily extendable to add support for additional databases over time.
  * The tool must allow searching for all kinds of interesting data using a variety of mechanisms.
  * The tool must support easily adding detectors for additional data over time.
  * The tool must allow the user to extract the data it finds from the database.

## Design
The tool was developed in Python as a command line interface (CLI).  The two major abstractions are the Database Scanners and the Data Detectors.

  * **Database Scanner**: The Database Scanner interface abstracts the logic of connecting to the database and iterating over the data.  Most databases organize data into tables, collections, or some other logical grouping.  A subclass is created for each supported database.  Each subclass will connect to the database, figure out what tables/collections exist and then iterate over the rows, columns, documents, etc. When the specific database scanner has a row or document it then uses the data detectors to see if the table/document contains data of interest.
  * **Data Detector**: The Data Detector is a simple functional interface that is given a single value extracted from the database and determines if that value represents data of interest.  Subclasses or instances of Data Detectors can be added to the system to look for different types of data.

![Architecture](assets/architecture.png)

The separation of the Database Scanner and Data Detectors concepts means that the same set of Data Detectors will work for any database the system supports.  Both Data Detectors and Database Scanners are dynamically imported meaning that they can be added to the system without having to change any code in the core of the system.

### Sampling
One other key concept is that databases can contain a lot of data.  For example, if a particular table has 10M rows, it may be impractical to iterate over every row to see if there is any data of interest.  In MOST databases tables and documents are fairly homogenous.  Meaning that if a record in a table contains an AWS Access Key, it's likely that the other rows will as well.  So instead of looking at all rows / document we sample a specified number of them. The default value is 10, but this can be set using the `--sample-size` flag. 

## Video
A demonstration video can be found on YouTube here:

[https://youtu.be/Ub7mYhkB3eE](https://youtu.be/Ub7mYhkB3eE)


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
  -t TYPE, --type TYPE  Specifies the type of database you are connecting to
  -n SAMPLE_SIZE, --sample-size SAMPLE_SIZE
                        Specifies the number of records from each table to query to detect data
  -s SERVER, --server SERVER
                        Specifies the database server to connect to
  -d DATABASE, --database DATABASE
                        Specifies the database name to connect to
  -u USERNAME, --username USERNAME
                        The username to log into the database with
  -p PASSWORD, --password PASSWORD
                        The password to log into the database with
  -e EXTRACT, --extract EXTRACT
                        Extracts detected data from the database to a specified file
  -v, --verbose         Triggers additional output
```

### MySQL

The example below shows connecting to a MySQL Database.

```bash
./db-scavenger.py -t mysql -s "localhost" -d csc842 -u admin -p admin -v
```

### MongoDB

The example below shows connecting to a MySQL Database.

```bash
./db-scavenger.py -t mongodb -s "localhost" -d csc842 -u admin -p admin -v
```

### PostgreSQL

The example below shows connecting to a PostgreSQL Database.

```bash
./db-scavenger.py -t postgres -s "localhost" -d csc842 -u admin -p admin -v
```

### Extraction Example

The example below shows connecting to a PostgreSQL Database and then extracting the interesting data.

```bash
./db-scavenger.py -t postgres -s "localhost" -d csc842 -u admin -p admin -v -e /.extracted/postgres
```
