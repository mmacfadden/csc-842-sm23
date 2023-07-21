from ..regex_data_detector import RexExDataDetector

detector = RexExDataDetector(
  name = "AWS Access Key Id",
  regex = "\\b((?:AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16})\\b"
)