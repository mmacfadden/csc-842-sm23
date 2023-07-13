class SecretDetector:
    
    def __init__(self, name: str) -> None:
        self.name = name

    def detect_secret(self, _: str) -> bool:
        raise Exception("Subclasses must override the findSecret method")