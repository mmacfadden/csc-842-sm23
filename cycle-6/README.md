# Cycle 6: PDF-Embed


## Requirements
The main requirements of the project that influenced the functionality and design are as follows:

TBD

## Design
TBD

## Video
A demonstration video can be found on YouTube here:

[https://youtu.be/TBD](https://youtu.be/bNNDqdyTBDa3Sw)


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
usage: pdf-embed.py [-h] -p PDF [-f FILES] [-d DIRS] [-c] [-k KEY] -o OUTPUT {embed,extract}

What the program does

positional arguments:
  {embed,extract}       Specifies the action to perform.

options:
  -h, --help            show this help message and exit
  -p PDF, --pdf PDF     The PDF file to read from
  -f FILES, --file FILES
                        Selects a file to embed in the PDF
  -d DIRS, --dir DIRS   Selects a directory of files (non-recursive) to embed in the PDF
  -c, --cloak           Hides the embedded files, such that they will not show up in a PDF viewer.
  -k KEY, --key KEY     Provides an encryption key to encrypt the embedded files and their file names.
  -o OUTPUT, --output OUTPUT
                        Where to write output to. When embedding, the output PDF. When extracting, the directory to extract files to.
```


### Embed
```bash
./pdf-embed.py embed \
  -p examples/pdfs/f1040.pdf \
  -o work/out.pdf \
  -f examples/files/file_to_embed.txt \
  -f examples/files/skull.png \
  -k "my key" \
  -c
```

```bash
./pdf-embed.py embed \
  -p examples/pdfs/f1040.pdf \
  -o work/out.pdf \
  -d examples/files/ \
  -k "my key" \
  -c
```

## Extract
```bash
./pdf-embed.py extract \
  -p work/out.pdf \
  -k "my key" \
  -o work/extracted
```

./pdf-embed.py embed \
  -p examples/pdfs/f1040.pdf \
  -o work/out.pdf \
  -d examples/files/ \
  -k "my key" \
  -c