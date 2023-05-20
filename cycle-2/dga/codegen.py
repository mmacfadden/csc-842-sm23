class CodeGenerator():
    """
    An abstract class that defines the interface for a generic capability to
    generate code across multiple languages.  By default this class simply
    raises and Exception when the code generation methods are called.
    Subclasses will override the generation methods.
    """
    
    def generate_js_code(self) -> str:
        """
        Generates code for JavaScript.
        """
        raise Exception(f"{self.__class__.__name__} does no support JavaScript outputs")
    
    def generate_py_code(self) -> str:
        """
        Generates code for Python.
        """
        raise Exception(f"{self.__class__.__name__} does no support Python outputs")