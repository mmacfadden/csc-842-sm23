import requests
import subprocess
import os


##
## A collection of helper methods use in multiple places.
## 

def download_file(download_url: str, target_file: str) -> None:
    """
    A helper method to download a file from a URL to a specified file
    on the file system.
    """
    r = requests.get(download_url, allow_redirects=True)
    with open(target_file, "wb") as output_file:
        output_file.write(r.content)


def make(source_dir: str) -> None:
    """
    Runs make in a source directory using two threads.
    """
    exec("make -j2", source_dir)


def make_config(source_dir: str, label: str) -> None:
    """
    A helper method that runs "make defconfig" if a config file is not already
    present in the source directory.
    """

    config_file = os.path.join(source_dir, ".config")

    if not os.path.exists(config_file):
        print("Config file not found, generating default config")
        exec("make defconfig", source_dir)
    else:
        print(f"{label} configuration already exists")


def exec(command: str, working_dir: str =".") -> None:
    """
    A helper method that synchronously executes a shell command
    in a specified working directory.
    """
    p = subprocess.Popen(command, shell=True, cwd=working_dir)
    p.wait()


def die(message: str) -> None:
    """
    A helper method to print a message and exit with an error code.
    """
    print(message)
    exit(1)
    