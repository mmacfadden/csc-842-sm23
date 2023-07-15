from ..regex_data_detector import RexExDataDetector

detector = RexExDataDetector(
  name = "RSA Private Key",
  regex = "\\s*(\\bBEGIN\\b).*(PRIVATE KEY\\b)\\s*"
)