from ..regex_secret_matcher import RexExSecretDetector

matcher = RexExSecretDetector(
  name = "Phone Number",
  regex = """^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$"""
)