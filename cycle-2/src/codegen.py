class CodeGenerator():

    def generate_js_code(self) -> str:
        raise Exception(f"{self.__class__.__name__} does no support JavaScript outputs")
    
    def generate_py_code(self) -> str:
        raise Exception(f"{self.__class__.__name__} does no support Python outputs")