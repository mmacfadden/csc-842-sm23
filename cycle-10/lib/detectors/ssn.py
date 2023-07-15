from ..regex_data_detector import RexExDataDetector

detector = RexExDataDetector(
  name = "Social Security Number",
  regex = """^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4})\\d{4}$"""
)