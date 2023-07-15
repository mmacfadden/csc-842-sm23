from ..regex_data_detector import RexExDataDetector

detector = RexExDataDetector(
  name = "AWS Access Key Id",
  regex = "(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])"
)