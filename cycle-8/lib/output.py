import json
import airspeed
from datetime import datetime
from colorama import Fore, Style

from .analyzer import AnalysisResult


class ResultFormatter:
  """
  The ResultFormatter is essentially an abstract class that defines
  the shape of all output formatters.  Subclasses will control how
  the results of the TLS analysis are converted to some textual
  representation.
  """
  def __init__(self) -> None:
    self.__result = ""

  def result(self) -> str:
    """
    Returns the formatted result as a string.
    """
    return self.__result
  
  def append_line(self, line: str) -> None:
    """
    Appends the specified text followed by a newline, to the result.
    """
    self.__result += line + "\n"

  def newline(self) -> str:
    """
    Appends a blank newline to the result.
    """
    self.append_line("")

  def generate_output(self, result: AnalysisResult) -> str:
    """
    Generate the output.  This is the primary method to be
    overridden by subclasses.
    """
    pass
    

class TextResultFormatter(ResultFormatter):
  """
  Generates a plain text, human readable output intended to be
  printed to the console.
  """
  
  def __init__(self) -> None:
    super().__init__()
  
  def generate_output(self, result: AnalysisResult) -> str:
    report_time =  datetime.now().strftime("%m/%d/%Y @ %H:%M:%S")
    self.append_line(Fore.CYAN + f"Input File:   {Style.RESET_ALL} {result.pcap_file}")
    self.append_line(Fore.CYAN + f"Report Time:  {Style.RESET_ALL} {report_time}")
    self.append_line(Fore.CYAN + "TLS Requests:" + Style.RESET_ALL)

    cert_number = 1
    for cert in result.tls_requests:
      self.newline()
      cert_error = None
      if cert.cert_error != None:
        cert_error = Fore.RED + cert.cert_error.msg + Style.RESET_ALL

      self.append_line(f"# {cert_number})")
      cert_number += 1

      self.append_line(f"  Hostname: {Fore.YELLOW}{cert.hostname}{Style.RESET_ALL}")
      self.append_line(f"  IP Address: {cert.request_ip}")
      self.append_line(f"  Valid IP Address: {cert.valid_ip_for_hostname}")
      self.append_line(f"  Valid IP For Domain: {cert.valid_ips_for_hostname}")
      self.append_line(f"  Validation Error: {cert_error}")
      self.append_line(f"  Certificate Chain:")
      
      for c in cert.cert_chain.all_certs:
        self.append_line(f"    {Fore.GREEN}{c.cert().subject.rfc4514_string()}{Style.RESET_ALL}")
      

class JsonResultFormatter(ResultFormatter):
  """
  Transforms the results into a JSON object, serialized to
  a string.  It is intended to be ingested by down stream 
  tools.
  """
    
  def __init__(self) -> None:
    super().__init__()

  def generate_output(self, result: AnalysisResult) -> str:
    val = json.dumps(result.to_data())
    self.append_line(val)


class HtmlResultFormatter(ResultFormatter):
  """
  Generates a HTML page, which shows the results in more detail.  This
  output would likely be written to a file.  This formatter uses the
  airspeed module which supports a Velocity template type syntax to
  fill in a template located in the templates/report.html file.
  """
    
  def __init__(self) -> None:
    super().__init__()

  def generate_output(self, result: AnalysisResult) -> str:
    with open("templates/report.html", "r") as f:
      template = airspeed.Template(f.read())

    report_time =  datetime.now().strftime("%m/%d/%Y @ %H:%M:%S")
    total_request_count = len(result.tls_requests)

    value = template.merge({
      "pcap_file": result.pcap_file,
      "tls_requests": result.tls_requests,
      "report_time": report_time,
      "total_requests": total_request_count
    })
    self.append_line(value)
