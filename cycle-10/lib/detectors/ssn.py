from ..regex_secret_matcher import RexExSecretDetector

matcher = RexExSecretDetector(
  name = "Social Security Number",
  regex = """^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4})\\d{4}$"""
)