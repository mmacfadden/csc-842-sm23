
import os

from io import BytesIO
from typing import Union

from pypdf import PdfReader, PdfWriter

from .encryption import Encryption
from .util import fatal_error

from colorama import Fore, Style

def embed(source_pdf: str,
          hide: bool,
          encryption_key: Union[str, None],
          files_to_embed: list[str], 
          output_file: str) -> None:
  
  if not isinstance(source_pdf, str) or len(source_pdf) < 1:
        raise Exception("The source_pdf param must be a string of length 1 or greater.")
  
  if not isinstance(output_file, str) or len(output_file) < 1:
        raise Exception("The output_file param must be a string of length 1 or greater.")
  
  if not os.access(source_pdf, os.R_OK):
    fatal_error(f"Can not read source PDF file: {source_pdf}")
  
  print(f"Source: {source_pdf}\n")

  if encryption_key != None:
     print(Fore.CYAN + f"Embedding and encrypting files into PDF:")
  else: 
    print(Fore.CYAN + f"Embedding files into PDF")

  print(Style.RESET_ALL, end="")

  reader = PdfReader(source_pdf)
  writer = PdfWriter()
  writer.append_pages_from_reader(reader)

  enc = None

  if encryption_key != None:
    enc = Encryption(encryption_key)

  for embed_file in files_to_embed:
    
    if not os.access(embed_file, os.R_OK):
      fatal_error(f"Can not read file to embed: {embed_file}")

    with open(embed_file, "rb") as f:
        file_bytes = f.read()

        print(f"\n+ Embedding file: {embed_file}")

        basename = os.path.basename(embed_file)

        if enc != None:           
           file_bytes = enc.encrypt_data(file_bytes)
           embedded_filename = enc.encrypt_filename(basename)
           print(f"   ∟ Encrypted Filename: {embedded_filename}")
        else:
           embedded_filename = basename
           
        writer.add_attachment(embedded_filename, file_bytes)

  with BytesIO() as bytes_stream:
    writer.write(bytes_stream)
    bytes_stream.seek(0)
    bytes = bytes_stream.read()

    if hide:
      print(Fore.CYAN + f"\nHiding Embedded Files")
      print(Style.RESET_ALL)
      bytes = bytes.replace(b"/EmbeddedFiles", b"/StyleObjects")
    
  print(Fore.CYAN + f"Writing output file: {output_file}")
  print(Style.RESET_ALL)
  
  with open(output_file, "wb") as w:
      w.write(bytes)

  print(Fore.GREEN + f"Job completed!")
  print(Style.RESET_ALL)
  

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
      for i, content in enumerate(content_list):
        if enc != None:
            content = enc.decrypt_data(content)
            name = enc.decrypt_filename(name)

        print(f"+ Extracting file: {name}")
        with open(os.path.join(out_dir, f"{name}"), "wb") as fp:
          fp.write(content)
    
    print(Fore.GREEN + f"\nJob completed!")
    print(Style.RESET_ALL)