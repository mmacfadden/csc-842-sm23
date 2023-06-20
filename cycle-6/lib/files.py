import os

def compute_files(files: list[str], dirs: list[str]) -> list[str]:
  """
  A helper method to compute the total set of files that will be included
  in the PDF.  This disallows duplicates.

  Parameters:
    files: A list of specific files to include.
    dirs:  A list of directories to include files from.
  
  Returns:
    A list of resolved file paths to include.
  """
  all_files = set(files.copy())
  
  for dir in dirs:
    files_in_dir = os.listdir(dir)
    for f in files_in_dir:
       file_path = os.path.join(dir, f)
       if not os.path.isdir(file_path):
          all_files.add(file_path)
    
  return list(all_files)