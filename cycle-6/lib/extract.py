
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
  """
  This method extracts potentially hidden files from a PDF.
 
  Parameters:
    source_pdf:      The path to the PDF to extract the files from.
    encryption_key:  The encryption key to use to decrypt the files if
                     they were encrypted, or None if they were not.
    out_dir:         The path to the directory to extract the files to.

  Returns:
    None.
  """
    
  print(f"Source: {source_pdf}\n")

  if not os.access(source_pdf, os.R_OK):
    fatal_error(f"Can not read source PDF file: {source_pdf}")

  try:
    os.makedirs(out_dir, exist_ok=True)
  except:
     fatal_error("Cannot make output directory")

  encryption = None

  if encryption_key != None:
    encryption = Encryption(encryption_key)
  
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

  try_decompress = True

  for name in reader.attachments:
    content_list = reader.attachments[name]
    for _, compressed_file_bytes in enumerate(content_list):
      if encryption != None:
          compressed_file_bytes = encryption.decrypt_data(compressed_file_bytes)
          name = encryption.decrypt_filename(name)

      # The only way to really tell if the files were compressed is to
      # simply try to decompress them. If this fails, then we assume
      # that none of the files were compressed and don't bother to
      # try to decompress the rest of them.
      if try_decompress:
        try:
          file_bytes = zlib.decompress(compressed_file_bytes)
        except zlib.error:
          file_bytes = compressed_file_bytes
          try_decompress = False


      print(f"+ Extracting file: {name}")
      with open(os.path.join(out_dir, f"{name}"), "wb") as fp:
        fp.write(file_bytes)
    
  print(Fore.GREEN + f"\nJob completed!")
  print(Style.RESET_ALL)