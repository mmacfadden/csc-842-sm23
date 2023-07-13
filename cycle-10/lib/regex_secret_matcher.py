import re
from .secret_detector import SecretDetector

class RexExSecretDetector(SecretDetector):
    
    def __init__(self, name: str, regex: str) -> None:
        super().__init__(name)
        self.regex = regex

    def detect_secret(self, value: str) -> bool:
        match = re.search(self.regex, value)
        return match != None