class DataDetector:
    """
    The DataDetector class defines the interface of all data detectors
    that can identify if a string value may have interesting data in it.
    Each data detector has a unique name, which is a human readable string
    that describes the data that it detects.
    """
    
    def __init__(self, name: str) -> None:
        self.name = name

    def detect(self, _: str) -> bool:
        """
        Given a string value, determines if a value matches what the detector
        is looking for.
        """
        raise Exception("Subclasses must override the findSecret method")