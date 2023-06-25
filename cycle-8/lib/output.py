import json
import airspeed
from datetime import datetime
import os

from .analyzer import AnalysisResult


class ResultFormatter:
  def __init__(self) -> None:
    self.__result = ""

  def result(self) -> str:
    return self.__result
  
  def append_line(self, line: str) -> None:
    self.__result += line + "\n"

  def newline(self) -> str:
    self.append_line("")

  def generate_output(self, result: AnalysisResult) -> str:
    pass
    

class TextResultFormatter(ResultFormatter):
    
    def __init__(self) -> None:
      super().__init__()
    
    def generate_output(self, result: AnalysisResult) -> str:
      self.append_line(f"Input File: {result.pcap_file}")
      self.append_line("TLS Requests:")

      for cert in result.tls_requests:
        self.newline()
        self.append_line(f"  Hostname: {cert.hostname}")
        self.append_line(f"  IP Address: {cert.request_ip}")
        self.append_line(f"  Valid IP Address: {cert.valid_ip_for_hostname}")
        self.append_line(f"  Valid IP For Domain: {cert.valid_ips_for_hostname}")
        self.append_line(f"  Validation Error: {cert.cert_error}")
        self.append_line(f"  Certificate Chain:")
        
        for c in cert.cert_chain.all_certs:
          self.append_line(f"    {c.cert().subject.rfc4514_string()}")
        

class JsonResultFormatter(ResultFormatter):
    
    def __init__(self) -> None:
      super().__init__()

    def generate_output(self, result: AnalysisResult) -> str:
      val = json.dumps(result.to_data())
      self.append_line(val)


class HtmlResultFormatter(ResultFormatter):
    
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
      

 