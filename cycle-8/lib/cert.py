from typing import Union
from dataclasses import dataclass

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization

from certvalidator import CertificateValidator
from certvalidator.errors import InvalidCertificateError, PathValidationError, PathBuildingError


@dataclass
class CertValidationError:
  """
  The CertValidationError represents an issue with validating a certificate.
  It contains both a machine readable code, as well as a human readable message.
  """

  code: str
  msg: str

  def to_data(self): 
    return {
      "msg": self.msg,
      "code": self.code
    }

class Certificate:    
  def __init__(self, cert_der_bytes) -> None:
    self.__der_bytes = cert_der_bytes
    self.__cert = x509.load_der_x509_certificate(cert_der_bytes)

  def bytes(self) -> bytes:
   return self.__der_bytes

  def cert(self):
    return self.__cert
   
  def subject(self): 
    return self.__cert.subject.rfc4514_string()
 
  def issuer(self): 
    return self.__cert.issuer.rfc4514_string()
  
  def not_valid_before(self):
    return self.__cert.not_valid_before
  
  def not_valid_after(self):
    return self.__cert.not_valid_after
  
  def pem(self): 
    return self.__cert.public_bytes(serialization.Encoding.PEM).decode("utf8")

  
  def to_data(self) -> dict[str, any]:
    return {
      "subject": self.subject(),
      "pem": self.pem()
    }


class CertificateChain:
  """
  The CertificateChain class represents an SSL Certificate Chain that starts
  with the end_entity (e.g. the server), and then a set of intermediate certs
  that represent a signing chain from that entity cert to the root.
  """

  def __init__(self, end_cert_bytes: bytes, intermediate_cert_bytes: list[bytes]) -> None:
    """
    Creates s new CertificateChain.

    Parameters:
      end_cert_bytes:
        The DER encoded bytes of the end entity certificate.

      intermediate_cert_bytes:
        A list of bytes objects representing the DER encoded intermediates
        certs.
    """
    self.__end_entity_cert = Certificate(end_cert_bytes)
    self.__intermediates = []
    for int_cert_bytes in intermediate_cert_bytes:
      self.__intermediates.append(Certificate(int_cert_bytes))
  
  def entity_subject(self) -> str:
      """
      Returns the subject of the end entity certificate.
      """
      attrs = self.__end_entity_cert.cert().subject.get_attributes_for_oid(NameOID.COMMON_NAME)
      if len(attrs) > 0:
         return attrs[0].value
      else:
         return None
   
  def end_entity_cert(self) -> Certificate:
     """
     Returns the parsed end entity cert.
     """
     return self.__end_entity_cert
  
  def intermediate_certs(self) -> list[Certificate]:
     """
     Returns a list of parsed intermediate certs.
     """
     return self.__intermediates
  
  @property
  def all_certs(self) -> list[Certificate]:
     """
     Returns all certs in order, starting from the end entity cert, followed
     by the intermediate certs.
     """
     all = self.__intermediates.copy()
     all.insert(0, self.__end_entity_cert)
     return all
  
  def to_data(self) -> list[dict[str, any]]:
     """
     Returns a raw data (dict) representation of the cert chain.
     """
     return list(map(lambda x: x.to_data(), self.all_certs))
  

  def validate(self, hostname: str) -> Union[CertValidationError, None]:
    """
    Validates the SSL certificate.

    Parameters:
      hostname: The hostname that was requested by the client.  Used to
                check if the certificate covers that hostname.

    Returns:
      None if there are no errors.  Otherwise, will return a 
      CertValidationError describing the first issue found.
    """
    end_cert = self.__end_entity_cert.bytes()
    intermediates = []
    for i in self.__intermediates:
      intermediates.append(i.bytes())

    validator = CertificateValidator(end_cert, intermediates)
    try:
      validator.validate_tls(hostname)
      validator.validate_usage(set(['digital_signature']))
      return None
    except InvalidCertificateError as err:
      e_string = str(err).lower()
      code = "invalid-cert"

      if "self-signed" in e_string:
        code = "self-signed"
      elif "weak" in e_string:
        code = "weak-algo"
      elif "valid hostnames include" in e_string:
        code = "invalid-hostname"
      elif "securing TLS" in e_string:
        code = "invalid-usage"  

      return CertValidationError(code, str(err))
    
    except PathValidationError as err:
      e_string = str(err).lower()
      code = "path-validation"

      if "expired" in e_string:
        code = "expired"

      return CertValidationError(code, str(err))
      
    except PathBuildingError as err:
      e_string = str(err).lower()
      code = "path-build"

      if "no issuer matching" in e_string:
        code = "untrusted-root"
      
      return CertValidationError(code, str(err))
    
    except err:
      return str(err)
   