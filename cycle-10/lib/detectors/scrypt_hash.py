from ..regex_data_detector import RexExDataDetector

matcher = RexExDataDetector(
  name = "Scrypt",
  regex = "^\\$s0\\$[0-9a-f]{5,8}\\$[a-zA-Z0-9/+]{22}[a-zA-Z0-9/+=]{2}\\$[a-zA-Z0-9/+]{42}[a-zA-Z0-9/+=]{2}$"
)