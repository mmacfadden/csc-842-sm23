from cryptography import x509
from cryptography.x509.oid import NameOID

from certvalidator import CertificateValidator
from certvalidator.errors import InvalidCertificateError


class Certificate:    
   def __init__(self, cert_der_bytes) -> None:
      self.__der_bytes = cert_der_bytes
      self.__cert = x509.load_der_x509_certificate(cert_der_bytes)

   def bytes(self) -> bytes:
      return self.__der_bytes

   def cert(self):
      return self.__cert


class CertificateChain:
  def __init__(self, end_cert_bytes: bytes, intermediate_cert_bytes: list[bytes]) -> None:
    self.__end_entity_cert = Certificate(end_cert_bytes)
    self.__intermediates = []
    for int_cert_bytes in intermediate_cert_bytes:
      self.__intermediates.append(Certificate(int_cert_bytes))
  
  def hostname(self) -> str:
      attrs = self.__end_entity_cert.cert().subject.get_attributes_for_oid(NameOID.COMMON_NAME)
      if len(attrs) > 0:
         return attrs[0].value
      else:
         return None
   
  def end_entity_cert(self) -> Certificate:
     return self.__end_entity_cert
  
  def intermediate_certs(self) -> list[Certificate]:
     return self.__intermediates
  
  def validate(self):
    end_cert = self.__end_entity_cert.bytes()
    intermediates = []
    for i in self.__intermediates:
      intermediates.append(i.bytes())

    validator = CertificateValidator(end_cert, intermediates)
    try:
      validator.validate_usage(set(['digital_signature']))
      return True
    except InvalidCertificateError as err:
       print(str(err))
       return False
      
   