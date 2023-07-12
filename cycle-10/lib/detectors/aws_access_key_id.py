from ..regex_secret_matcher import RexExSecretDetector

matcher = RexExSecretDetector(
  name = "AWS Access Key Id",
  regex = "(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])"
)