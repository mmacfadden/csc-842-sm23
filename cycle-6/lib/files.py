import os

def compute_files(files: list[str], dirs: list[str]) -> list[str]:
  all_files = set(files.copy())
  
  for dir in dirs:
    files_in_dir = os.listdir(dir)
    for f in files_in_dir:
       file_path = os.path.join(dir, f)
       if not os.path.isdir(file_path):
          all_files.add(file_path)
    
  return all_files