import argparse
import os
import yaml

from .util import die

class ConfigManager:

    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(
                            prog='kernel-booter',
                            description='What the program does',
                            epilog='Text at the bottom of help')

        self._parser.add_argument('command', default="boot")          
        self._parser.add_argument('-c', '--config', help="The configure file to use.", default="vm-config.yml")  

    def parse(self): 
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

                return Configuration(
                    command,
                    config["kernel"],
                    config["architecture"],
                    config["namespace"],
                    root_fs_type,
                    root_fs
                )

            except yaml.YAMLError as exc:
                die(exc)


class Configuration:

    def __init__(self, command, kernel, architecture, namespace, root_fs_type, root_fs) -> None:
        self.command = command
        self.kernel = kernel
        self.architecture = architecture
        self.namespace = namespace
        self.root_fs_type = root_fs_type
        self.root_fs = root_fs

        
        



        
        