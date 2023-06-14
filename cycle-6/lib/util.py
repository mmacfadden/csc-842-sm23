from colorama import Fore, Style

def fatal_error(message: str) -> None:
    print(Fore.RED + "\nERROR: " + message)
    print(Style.RESET_ALL)
    exit(1)
    