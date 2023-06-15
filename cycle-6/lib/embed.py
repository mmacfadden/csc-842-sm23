
import os
import zlib

from io import BytesIO
from typing import Union

from pypdf import PdfReader, PdfWriter

from .encryption import Encryption
from .util import fatal_error

from colorama import Fore, Style

class PdfFileEmbedder:
  """
  The PdfFileEmbedder handles the logic of embedding, encrypting, and hiding
  files within an existing PDF.  A source PDF is used, but not modified, and
  a copy is generated with files hidden in it.
  """

  def __init__(self, source_pdf: str,) -> None:
     """
     Creates a new PdfFileEmbedder that will use a specified PDF as the source
     file.  The source file must exist and be readable.
     """
     if not isinstance(source_pdf, str) or len(source_pdf) < 1:
          raise Exception("The source_pdf param must be a string of length 1 or greater.")
     
     self.__source_pdf = source_pdf
     

  def embed_files_in_pdf(self,
                         files_to_embed: list[str], 
                         output_file: str,
                         hide_files: bool = False,
                         compress_files: bool = False,
                         encryption_key: Union[str, None] = None
                         ) -> None:
    """
    Uses the configured Source PDF and embeds files into it, creating a 
    new output PDF.

    Parameters:
      files_to_embed: The list of files to embed in the source pdf.
      output_file:    The path to write the resultant file to. 
      hide_files:     Wether to hide / obfuscate the files in the target PDF.
      encryption_key: The encryption key to use to encrypt the embedded files
                      of None, if encryption is not to be performed.

    Returns:
      None
    """
    
    if not isinstance(output_file, str) or len(output_file) < 1:
      raise Exception("The output_file param must be a string of length 1 or greater.")
     
    print(f"Source: {self.__source_pdf}\n")

    if encryption_key != None:
       print(Fore.CYAN + f"Embedding and encrypting files into PDF:")
    else: 
      print(Fore.CYAN + f"Embedding files into PDF")

    print(Style.RESET_ALL, end="")

    writer = self.__clone_writer_from_pdf()
    self.__embed_files(writer, files_to_embed, compress_files, encryption_key)
    pdf_bytes = self.__serialize_pdf(writer)

    if hide_files:
      pdf_bytes = self.__hide_embedded_files(pdf_bytes)
    
    print(Fore.CYAN + f"Writing Output File " + Style.RESET_ALL)
    print(f"  ∟ Filename:   {output_file}")
    print(f"  ∟ Total Size: {len(pdf_bytes):,} Bytes \n")
    
    with open(output_file, "wb") as w:
        w.write(pdf_bytes)

    print(Fore.GREEN + f"Job completed!")
    print(Style.RESET_ALL)


  def __clone_writer_from_pdf(self) -> PdfWriter:
    """
    Initializes a PDFWriter by opening the source PDF reading it in
    and copying the contents into a new PDFWriter.

    Returns:
      A new PDFWriter initialized with the contents of the source PDF.
    """

    if not os.access(self.__source_pdf, os.R_OK):
      fatal_error(f"Can not read source PDF file: {self.__source_pdf}")

    reader = PdfReader(self.__source_pdf)
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    return writer
  

  def __embed_files(self,
                    writer: PdfWriter, 
                    files_to_embed: list[str],
                    compress_files: bool,
                    encryption_key: Union[str, None]
                   ) -> None:
    """
    Embeds files into the PDF, and encrypts them if required.

    Parameters:
      writer:          The PDRWriter to write the files to.
      files_to_embed:  A list of paths to files to embed. 
      encryption_key:  An encryption key to use to encrypt the embedded files
                       with, if encryption is desired.
    Returns:
      None
    """

    enc = None
    
    if encryption_key != None:
      enc = Encryption(encryption_key)

    for file_to_embed in files_to_embed:
       self.__embed_file(writer, file_to_embed, compress_files, enc)

      
  def __embed_file(self,
                   writer: PdfWriter, 
                   file_to_embed: str,
                   compress_file: bool,
                   encryption: Union[Encryption, None]
                  ) -> None:
    """
    Embeds a single file into the PDF, and encrypts them if required.

    Parameters:
      writer:          The PDRWriter to write the file to.
      file_to_embed:   The path to the file to embed.
      encryption_key:  An encryption key to use to encrypt the embedded file
                       with, if encryption is desired.
    Returns:
      None
    """

    if not os.access(file_to_embed, os.R_OK):
        fatal_error(f"Can not read file to embed: {file_to_embed}")

    with open(file_to_embed, "rb") as f:
          file_bytes = f.read()

          print(f"\n+ Embedding file: {file_to_embed}")

          basename = os.path.basename(file_to_embed)
     
          if compress_file:
            file_bytes = zlib.compress(file_bytes)

          if encryption != None:           
             file_bytes = encryption.encrypt_data(file_bytes)
             embedded_filename = encryption.encrypt_filename(basename)
             print(f"   ∟ Encrypted Filename: {embedded_filename}")
          else:
             embedded_filename = basename
             
          writer.add_attachment(embedded_filename, file_bytes)


  def __serialize_pdf(self, writer: PdfWriter) -> bytes:
    """
    Serializes the PDF into a bytes object.

    Parameters:
      writer: The PDRWriter to write containing the PDF.
    Returns:
      The PDF represented as bytes.
    """

    with BytesIO() as bytes_stream:
      writer.write(bytes_stream)
      bytes_stream.seek(0)
      pdf_bytes = bytes_stream.read()
    
    return pdf_bytes


  def __hide_embedded_files(self, pdf_bytes: bytes) -> bytes:
    """
    Hides / obfuscates the embedded files within the PDF.

    Parameters:
      pdf_bytes: The serialized PDF bytes.
    Returns:
      The updated pdf bytes.
    """

    print(Fore.CYAN + f"\nHiding Embedded Files")
    print(Style.RESET_ALL)
    hidden_bytes = pdf_bytes.replace(b"/EmbeddedFiles", b"/StyleObjects")

    return hidden_bytes
