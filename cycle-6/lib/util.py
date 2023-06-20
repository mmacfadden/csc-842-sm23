from colorama import Fore, Style

def fatal_error(message: str, exit_code: int = 1) -> None:
  """
  A helper method to print an error message and exit.

  Parameters:
    message:   The error message to display.
    exit_code: The exit code to exit the process with.
  """
  
  print(Fore.RED + "\nERROR: " + message)
  print(Style.RESET_ALL)
  exit(exit_code)
    