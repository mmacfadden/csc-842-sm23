import argparse
import os
import yaml

from .util import die


class Configuration:
    """
    Configuration is a simple data class that holds the configuration
    information for the tool
    """

    def __init__(self, 
                 command: str, 
                 namespace: str, 
                 architecture:str, 
                 virtual_machine: dict, 
                 kernel: dict, 
                 root_fs_type: str, 
                 root_fs: dict) -> None:
        self.command = command
        self.kernel = kernel
        self.architecture = architecture
        self.namespace = namespace
        self.root_fs_type = root_fs_type
        self.root_fs = root_fs
        self.virtual_machine = virtual_machine


class ConfigManager:
    """
    The ConfigManager class deals with both parsing command line arguments as
    well as loading the configuration file.
    """

    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(
          prog='auto-emulate',
          description='A simply utility to automate building Linux VMs for kernel hacking and firmware reversing',
        )

        self._parser.add_argument('command', nargs="?", default="boot", choices=['config', 'build-kernel', "build-fs", 'boot'])          
        self._parser.add_argument('-c', '--config', help="The configure file to use.", default="vm-config.yml")  


    def parse(self) -> Configuration:
        """
        Parses the command line arguments and configuration file and returns
        a configuration object.
        """
        args = self._parser.parse_args()

        command = args.command
        config_file = args.config

        if not os.path.exists(config_file):
            print("Config file not found: " + config_file)
            exit(1)
            
        with open(config_file, "r") as f:
            try:
                config = yaml.safe_load(f)

                if not "root_filesystem" in config:
                   die("root_fs missing from config")

                root_fs = config["root_filesystem"]

                if len(root_fs) != 1:
                    die("root_fs must have exactly one of: [busybox, dir]")
                    
                if "busy_box" in root_fs:
                    root_fs_type = "busy_box"
                elif "dir" in root_fs:
                   root_fs_type = "dir"
                else:
                    print(f"Invalid root_fs type: {root_fs[0]}")

                remote_debug = False

                if config.get("remote_debug"):
                    remote_debug = True

                return Configuration(
                    command,
                    config["namespace"],
                    config["architecture"],
                    config["virtual_machine"],
                    config["kernel"],
                    root_fs_type,
                    root_fs
                )

            except yaml.YAMLError as exc:
                die(exc)


        
        



        
        