# Cycle 6: PDF Smuggler
PDF Smuggler is a data exfiltration tool that aims to avoid detection by embedding files in [PDF Documents](https://pdfa.org/resource/iso-32000-pdf/).  The tool leverage PDF Attachment to attach files, but then hides and obfuscates the files in a way that makes them mostly invisible to users and data loss prevention tools.

PDF Smuggler is implemented in Python and is a command-line utility.  The tool has two modes **Embed** and **Extract**.  The embed function attaches and obfuscates files within an existing PDF that is to be sent out of an organization.  On the other end of the communication channel, the tool will extract the embedded files from the PDF.


## Requirements
The main requirements of the project that influenced the functionality and design are as follows:

  * The tool must be able to embed arbitrary files in an existing PDF.
  * The tool must, to the greatest extent possible, hide the embedded files within the PDF so that users and Data Loss Preventions systems won't be able to see that the PDF has attachments.
  * Embedded files should be encrypted to avoid signature detection and to make forensics harder (e.g. the organization won't be able to tell what data was exfiltrated).
  * Compression should be used to reduce the size of the resultant PDF.
  * The composed PDF should essentially look and behave like the original PDF file.
  * Given a PDF with embedded, obfuscated, compressed, and/or encrypted files, the tool must be able to extract the embedded files (with their original file names).

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
./pdf-smuggler.py -h                                                                                                                                                                                          2 ⨯
usage: pdf-smuggler.py [-h] -i INPUT [-f FILES] [-d DIRS] [--no-hide] [--no-compression] [-k KEY] -o OUTPUT {embed,extract}

This program embeds hidden files within a PDF in support of data exfiltration.

positional arguments:
  {embed,extract}       Specifies the action to perform.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        The PDF file to read from
  -f FILES, --file FILES
                        Selects a file to embed in the PDF
  -d DIRS, --dir DIRS   Selects a directory of files (non-recursive) to embed in the PDF
  --no-hide             Disables hiding the embedded files, such that they will show up in a PDF viewer.
  --no-compression      Disables compressing the embedded files.
  -k KEY, --key KEY     Provides an encryption key to encrypt the embedded files and their file names.
  -o OUTPUT, --output OUTPUT
                        Where to write output to. When embedding, the output PDF. When extracting, the directory to extract files to.
```


### Embedding Files
You can embed files into a source PDF using these examples.

**Embedding Files**

This example shows embedding specific files in the source PDF:

```bash
./pdf-smuggler.py embed \
  --input examples/pdfs/f1040.pdf \
  --file examples/files/file_to_embed.txt \
  --file examples/files/skull.png \
  --key "my key" \
  --output work/out.pdf
```

**Embedding A Directory**

This example shows embedding all files in a directory into the source PDF:

```bash
./pdf-smuggler.py embed \
  --input examples/pdfs/f1040.pdf \
  --dir examples/files/ \
  --key "my key" \
  --output work/out.pdf
```

**No Compression, Hiding of Files, or Encryption**

To aid in debugging its possible to turn off hiding the files, disable compression, and skip encryption.

```bash
./pdf-smuggler.py embed \
  --input examples/pdfs/f1040.pdf \
  --dir examples/files/ \
  --no-hide \
  --no-compression \
  --output work/out.pdf
```


## Extracting Files
The following command will extract files from a PDF.

```bash
./pdf-smuggler.py extract \
  --input work/out.pdf \
  --key "my key" \
  --output work/extracted
```
