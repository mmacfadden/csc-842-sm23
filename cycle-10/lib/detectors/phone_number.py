from ..regex_data_detector import RexExDataDetector

detector = RexExDataDetector(
  name = "Phone Number",
  regex = """^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$"""
)