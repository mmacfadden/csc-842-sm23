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

        self._parser.add_argument('command', nargs="?", default="boot", choices=['config', 'build-kernel', "build-fs", 'boot'])          
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


class Configuration:

    def __init__(self, command, namespace, architecture, virtual_machine, kernel, root_fs_type, root_fs) -> None:
        self.command = command
        self.kernel = kernel
        self.architecture = architecture
        self.namespace = namespace
        self.root_fs_type = root_fs_type
        self.root_fs = root_fs
        self.virtual_machine = virtual_machine

        
        



        
        