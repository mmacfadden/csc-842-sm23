import jwt
from ..regex_data_detector import RexExDataDetector

class JwtDetector(RexExDataDetector):
    
  def __init__(self) -> None:
    super().__init__("JWT", "^[A-Za-z0-9_-]{2,}(?:\.[A-Za-z0-9_-]{2,}){2}$")


  def detect(self, value: str) -> bool:
    if super().detect(value):
      try:
        jwt.decode(value, options={"verify_signature": False})
        return True
      except:
        return False
    else:
      return False

detector = JwtDetector()