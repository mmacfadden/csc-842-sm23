import re
from .data_detector import DataDetector

class RexExDataDetector(DataDetector):
    """
    The RexExDataDetector looks for data using a single regular expression
    pattern.

    Parameters:
      name: The name of the data detector.
      regex: The string representation of the regular expression to match on.
    """
    
    def __init__(self, name: str, regex: str) -> None:
        super().__init__(name)
        self.regex = regex

    def detect(self, value: str) -> bool:
        match = re.search(self.regex, value)
        return match != None
