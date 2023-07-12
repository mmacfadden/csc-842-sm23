from ..regex_secret_matcher import RexExSecretDetector

matcher = RexExSecretDetector(
  name = "AWS Access Key Secret",
  regex = "(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])"
)