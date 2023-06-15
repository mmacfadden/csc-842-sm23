
import os
import zlib

from io import BytesIO
from typing import Union

from pypdf import PdfReader

from .encryption import Encryption
from .util import fatal_error

from colorama import Fore, Style

def extract(source_pdf: str,
            encryption_key: Union[str, None],
            out_dir: str) -> None:
    
  print(f"Source: {source_pdf}\n")

  if not os.access(source_pdf, os.R_OK):
    fatal_error(f"Can not read source PDF file: {source_pdf}")


  try:
    os.makedirs(out_dir, exist_ok=True)
  except:
     fatal_error("Cannot make output directory")

  enc = None

  if encryption_key != None:
    enc = Encryption(encryption_key)
  
  with open(source_pdf, "rb") as f:
      bytes = f.read()

      if bytes.find(b"/StyleObjects") >= 0:
        print(Fore.CYAN + f"\nUnhiding Embedded Files" + Style.RESET_ALL + "\n")
        bytes = bytes.replace(b"/StyleObjects", b"/EmbeddedFiles")

  reader = PdfReader(BytesIO(bytes))

  if encryption_key != None:
     print(Fore.CYAN + f"Extracting and decrypting files from PDF")
  else: 
    print(Fore.CYAN + f"Extracting files from PDF")

  print(Style.RESET_ALL, end="")


  for name in reader.attachments:
    content_list = reader.attachments[name]
    for i, compressed_file_bytes in enumerate(content_list):
      if enc != None:
          compressed_file_bytes = enc.decrypt_data(compressed_file_bytes)
          name = enc.decrypt_filename(name)

      file_bytes = zlib.decompress(compressed_file_bytes)

      print(f"+ Extracting file: {name}")
      with open(os.path.join(out_dir, f"{name}"), "wb") as fp:
        fp.write(file_bytes)
    
  print(Fore.GREEN + f"\nJob completed!")
  print(Style.RESET_ALL)