from ..regex_secret_matcher import RexExSecretDetector

matcher = RexExSecretDetector(
  name = "RSA Private Key",
  regex = "\\s*(\\bBEGIN\\b).*(PRIVATE KEY\\b)\\s*"
)