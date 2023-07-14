from ..regex_data_detector import RexExDataDetector

matcher = RexExDataDetector(
  name = "AWS Access Key Secret",
  regex = "(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])"
)