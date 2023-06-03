import requests
import subprocess
import os

def download_file(download_url, target_file) -> str:
    r = requests.get(download_url, allow_redirects=True)
    with open(target_file, "wb") as output_file:
        output_file.write(r.content)

def make(working_dir):
    exec("make -j2", working_dir)

def make_config(source_dir, label):
    config_file = os.path.join(source_dir, ".config")

    if not os.path.exists(config_file):
        print("Config file not found, generating default config")
        exec("make defconfig", source_dir)
    else:
        print(f"{label} configuration already exists")

def exec(command: str, working_dir="."):
    p = subprocess.Popen(command, shell=True, cwd=working_dir)
    p.wait()

def die(message) -> None:
    print(message)
    exit(1)
    