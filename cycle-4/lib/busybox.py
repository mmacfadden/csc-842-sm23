import os
import tarfile
import re
import textwrap
import shutil

from .util import download_file, make, make_config, exec


class BusyBoxFileSystemBuilder:
    """
    The BusyBoxFileSystemBuilder class handles operations around building a root
    filesystem using BusyBox (plus additionally specified files).
    """

    def __init__(self, busy_box_config: dict, builds_dir: str, namespace_dir: str) -> None:
        self._version = busy_box_config["version"]
        self._namespace_dir = namespace_dir

        self._busy_box_config = busy_box_config

        filename = f"busybox-{self._version }.tar.bz2"

        self._download_dir = os.path.join(builds_dir, "busybox")
        self._download_url = f"https://busybox.net/downloads/{filename}"
        self._download_file = os.path.join(self._download_dir, filename)
       
        self._source_dir = os.path.join(self._namespace_dir, f"busybox-{self._version}")
     
    
    def download_busybox(self) -> None:
        """Downloads BusyBox if it has not already been downloaded."""
        os.makedirs(self._download_dir, exist_ok=True)

        if not os.path.exists(self._download_file):
            print(f"Downloading Busy Box {self._version} from {self._download_url}")
            download_file(self._download_url, self._download_file)
        else:
            print(f"Busy Box {self._version} already downloaded")
        

    def extract_busy_box(self) -> None:
        """
        Extracts BusyBox from the downloaded archive, if it has not already
        been extracted.
        """
        if not os.path.exists(self._source_dir):
            print(f"Extracting Busy Box {self._version} to: {self._source_dir}")
            with tarfile.open(download_file) as f:
                f.extractall(self._namespace_dir)
        else:
            print(f"Busy Box {self._version} already extracted")


    def make_busybox_config(self) -> None:
        """
        Runs a 'make defconfig' in the source directory, if the .config file
        does not already exist.  The function also, updates the configuration
        to ensure that BusyBox is statically linked.
        """
        make_config(self._source_dir, f"Busy Box {self._version}")
    
        config_path = os.path.join(self._source_dir, ".config")
        with open(config_path, "r") as config:
            lines = config.readlines()

        with open(config_path, "w") as sources:
            for line in lines:
                sources.write(re.sub(r'^# CONFIG_STATIC is not set$', 'CONFIG_STATIC=y', line))


    def make_busybox(self, rebuild: bool):
        """
        Compiles BusyBox and makes a BusyBox file system directory layout using
        'make' and 'make install'.
        """
        busy_box_build = os.path.join(self._source_dir, "_install")
        if not os.path.exists(busy_box_build) or rebuild:
            print("Building Busy Box")
            make(self._source_dir)
            exec("make install", self._source_dir)
        else:
            print(f"Busy Box {self._version} already built")


    def create_init_script(self, root_fs_build_dir: str) -> None:
        """
        Creates the /init script for booting the system.
        """

        init_extra = self._busy_box_config.get("init_extra", "")
        uid = self._busy_box_config.get("uid", 1000)

        init = textwrap.dedent(
            f"""
            #!/bin/sh
            mount -t proc none /proc
            mount -t sysfs none /sys
            mount -t devtmpfs none /dev
            mount -t tmpfs none /tmp

            {init_extra}

            setuidgid {uid} /bin/sh
            """
        ).strip()

        with open(os.path.join(root_fs_build_dir, "init"), "w") as init_file:
            init_file.write(init)


    def build_root_fs(self, root_fs_dir: str, rebuild: bool) -> str:
        """
        Builds the root file system by copying the BusyBox file layout,
        creating the init script, adding any additional user specified files,
        and creating a disk image file using cpio.
        """

        root_fs_build_dir = os.path.join(self._namespace_dir, root_fs_dir)

        if not os.path.exists(root_fs_build_dir) or rebuild:
            shutil.rmtree(root_fs_build_dir, ignore_errors=True)

            os.makedirs(root_fs_build_dir, exist_ok=True)
            
            exec(f"cp -a {self._source_dir}/_install/* {root_fs_build_dir}")

            for include in self._busy_box_config.get("includes", []):
                to = include['to']
                if to[0] == "/":
                    to = to[1:len(to)]

                cmd = f"cp -a {include['from']} {os.path.join(root_fs_build_dir, to)}"
                exec(cmd)

            exec("rm linuxrc", root_fs_build_dir)
            exec("mkdir proc sys dev tmp", root_fs_build_dir)
            
            self.create_init_script(root_fs_build_dir)
            
            exec(f"chmod +x {root_fs_build_dir}/init")


        image_path =  os.path.join(self._namespace_dir, "initramfs.cpio")
        if not os.path.exists(image_path) or rebuild:
            exec(f"find . | cpio -ov --format=newc > ../initramfs.cpio 2>/dev/null", root_fs_build_dir)

        return image_path