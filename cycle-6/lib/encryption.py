from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
import base64


class Encryption:
    """
    The Encryption encapsulates the logic used to encrypt files and filenames
    within the PDF file.  It uses AES 256 to encrypt data.  The class also
    performs cryptographic key derivation using the scrypt algorithm defined
    in RFC 7914.  This allows a short, user defined string to be used as
    a key.
    """
    
    def __init__(self, key: str, char_encoding: str = "utf8") -> None:
      """
      Creates a new Encryption instance. 
     
      Parameters:
        key: The string key to derive an encryption key from. 
        char_encoding: The character encoding to use for strings. 

      Returns:
        A new Encryption instance
      """

      if not isinstance(key, str) or len(key) < 1:
        raise Exception("The key must be a string of length 1 or greater.")

      
      # The character encoding to convert between string and binary
      # representations of data.
      self.__char_encoding = char_encoding

      # Key is passed in as a string, but most encryption libraries
      # want binary data. We assume UTF8 encoding.
      key_bytes = key.encode(self.__char_encoding)

      # For actual encryption, where you are concerned about keeping the data
      # private, you would ideally want a randomized salt and a per-message
      # nonce.  However, this means you would need to store these. Since
      # we aren't really concerned with actual data privacy, and are just
      # using encryption to mask the data to avoid signature detection,
      # we just hard code them here.
      self.__nonce = b'b8P\xdc\x968\xc9\xdaB\xeb\x87\xa6bT\xbe\xe7'

      salt = b"8"*16
      cost = 2**14
      key_len = 32  # In bytes, so 32 bytes = 256 bits for AES 256.
      block_size=8
      parallelization = 1

      self.__key = scrypt(key_bytes, salt, key_len, N=cost, r=block_size, p=parallelization)
        
      

    def encrypt_filename(self, filename: str) -> str:
      """
      Encrypts a filename to be embedded into a PDF. 
     
      Parameters:
        filename: The original filename to encrypt. 

      Returns:
        The encrypted filename, encoded in a Base 16 string.
      """

      if not isinstance(filename, str) or len(filename) < 1:
        raise Exception("The filename must be a string of length 1 or greater.")

      filename_bytes = filename.encode(self.__char_encoding)
      filename_encrypted = self.encrypt_data(filename_bytes)
      filename_encrypted_b16 = base64.b16encode(filename_encrypted)
      encrypted_filename = filename_encrypted_b16.decode(self.__char_encoding)
      return encrypted_filename
    

    def decrypt_filename(self, encoded_filename: str) -> str:
      """
      Decrypts a filename that was embedded into the PDF. 
     
      Parameters:
        encoded_filename: The Base 16 encoded and encrypted filename. 

      Returns:
        The decoded and decrypted filename.
      """

      if not isinstance(encoded_filename, str) or len(encoded_filename) < 1:
        raise Exception("The encoded_filename must be a string of length 1 or greater.")

      encoded_filename_bytes = encoded_filename.encode(self.__char_encoding)
      encrypted_filename_bytes = base64.b16decode(encoded_filename_bytes)
      filename_bytes = self.decrypt_data(encrypted_filename_bytes)
      filename = filename_bytes.decode(self.__char_encoding)
      return filename
        
    
    def encrypt_data(self, plaintext: bytes) -> bytes:
      """
      Encrypts data using AES 256. 
     
      Parameters:
        plaintext: The original data to encrypt as bytes. 

      Returns:
        The encrypted data as bytes.
      """

      if not isinstance(plaintext, bytes) or len(plaintext) < 1:
        raise Exception("The plaintext must be a bytes object of length 1 or greater.")
      
      cipher = self.__create_cipher()
      ciphertext = cipher.encrypt(plaintext)
      return ciphertext
    
    
    def decrypt_data(self, ciphertext: bytes) -> bytes:
      """
      Decrypts data using AES 256. 
     
      Parameters:
        ciphertext: The encrypted data to decrypt. 

      Returns:
        The decrypted data as bytes.
      """

      if not isinstance(ciphertext, bytes) or len(ciphertext) < 1:
        raise Exception("The plaintext must be a bytes object of length 1 or greater.")
      
      cipher = self.__create_cipher()
      plaintext = cipher.decrypt(ciphertext)
      return plaintext
    
    
    def __create_cipher(self) -> AES: 
      """
      A helper method to create an AES cipher.

      Returns:
        A new AES cipher instance.
      """
      cipher = AES.new(self.__key, AES.MODE_EAX, nonce=self.__nonce)
      return cipher
