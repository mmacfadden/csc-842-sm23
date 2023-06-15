import argparse
from .util import fatal_error

def process_args():
  """
  This method sets up the command line parser using argparse.  After argparse
  parses the command line args, this method then performs some additional
  sanity checking to make sure the arguments passed in are valid.
  """

  parser = argparse.ArgumentParser(
                      prog='pdf-smuggler.py',
                      description='This program embeds hidden files within a PDF in support of data exfiltration.'
                      )

  parser.add_argument('-i', 
                      '--input',
                      dest="input",
                      required=True, 
                      help="The PDF file to read from")

  parser.add_argument('command', 
                      choices=["embed", "extract"],
                      help="Specifies the action to perform."
                      )

  parser.add_argument('-f', 
                      '--file', 
                      required=False, 
                      action='append', 
                      dest="files", 
                      default=[],
                      help="Selects a file to embed in the PDF")  

  parser.add_argument('-d', 
                      '--dir', 
                      required=False, 
                      action='append', 
                      dest="dirs",
                      default=[],
                      help="Selects a directory of files (non-recursive) to embed in the PDF")  

  parser.add_argument('--no-hide', 
                      required=False, 
                      default=True,
                      dest="hide",
                      action='store_false',
                      help="Disables hiding the embedded files, such that they will show up in a PDF viewer."
                      )
  
  parser.add_argument('--no-compression', 
                      required=False, 
                      default=True,
                      dest="compress",
                      action='store_false',
                      help="Disables compressing the embedded files."
                      )

  parser.add_argument('-k', '--key', 
                      required=False, 
                      default=None,
                      help="Provides an encryption key to encrypt the embedded files and their file names."
                      )

  parser.add_argument('-o', 
                      '--output', 
                      required=True, 
                      help="Where to write output to.  When embedding, the output PDF. When extracting, the directory to extract files to."
                      )

  args = parser.parse_args()


  ##
  ## Sanity Check Arguments
  ##

  if isinstance(args.key, str) and len(args.key) < 1:
    fatal_error("The --key argument must be a string of length 1 or greater.")

  if isinstance(args.output, str) and len(args.output) < 1:
    fatal_error("The --output argument must be a string of length 1 or greater.")

  if isinstance(args.input, str) and len(args.input) < 1:
    fatal_error("The --input argument must be a string of length 1 or greater.")

  for dir in args.dirs:
    if isinstance(dir, str) and len(dir) < 1:
      fatal_error("The --dir argument must be a string of length 1 or greater.")

  for file in args.files:
    if isinstance(file, str) and len(file) < 1:
      fatal_error("The --file argument must be a string of length 1 or greater.")

  return args