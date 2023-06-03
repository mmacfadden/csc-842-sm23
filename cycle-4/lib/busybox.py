import os
import tarfile
import re
import textwrap
import shutil

from .util import download_file, make, make_config, exec


class BusyBoxManager:

    def __init__(self, version, builds_dir) -> None:
        self._version = version
        self._build_dir = os.path.join(builds_dir, "busybox")
        filename = f"busybox-{version}.tar.bz2"
        self._download_url = f"https://busybox.net/downloads/{filename}"
        self._download_file = os.path.join(self._build_dir, filename)
        self._source_dir = os.path.join(self._build_dir, f"busybox-{version}")
        
    def download_busybox(self) -> None:
        os.makedirs(self._build_dir, exist_ok=True)

        if not os.path.exists(self._download_file):
            print(f"Downloading Busy Box {self._version} from {self._download_url}")
            download_file(self._download_url, self._download_file)
        else:
            print("Busy box already downloaded")
        

    def extract_busy_box(self) -> None:
        if not os.path.exists(self._source_dir):
            print(f"Extracting Busy Box {self._version} to: {self._source_dir}")
            with tarfile.open(download_file) as f:
                f.extractall("build/busybox")
        else:
            print(f"Busy Boxy {self._version} already extracted")

    def make_busybox_config(self) -> None:
        make_config(self._source_dir, f"BusyBox {self._version}")
    
        config_path = os.path.join(self._source_dir, ".config")
        with open(config_path, "r") as config:
            lines = config.readlines()

        with open(config_path, "w") as sources:
            for line in lines:
                sources.write(re.sub(r'^# CONFIG_STATIC is not set$', 'CONFIG_STATIC=y', line))

    def make_busybox(self):
        busy_box_build = os.path.join(self._source_dir, "_install")
        if not os.path.exists(busy_box_build):
            print("building busy box")
            make(self._source_dir)
            exec("make install", self._source_dir)
        else:
            print("Busy Box already built")


    def write_init(self, uid: int, root_fs_build_dir) -> str:
        init = textwrap.dedent(
            f"""
            #!/bin/sh
            mount -t proc none /proc
            mount -t sysfs none /sys
            mount -t devtmpfs none /dev
            mount -t tmpfs none /tmp

            setuidgid {uid} /bin/sh
            """
        ).strip()

        with open(os.path.join(root_fs_build_dir, "init"), "w") as init_file:
            init_file.write(init)

    def build_root_fs(self, root_fs_dir) -> str:

        root_fs_build_dir = os.path.join("build", root_fs_dir)

        shutil.rmtree(root_fs_build_dir, ignore_errors=True)

        os.makedirs(root_fs_build_dir, exist_ok=True)
        
        exec(f"cp -a {self._source_dir}/_install/* {root_fs_build_dir}")
        exec("rm linuxrc", root_fs_build_dir)
        exec("mkdir proc sys dev tmp", root_fs_build_dir)
        self.write_init(1000, root_fs_build_dir)
        exec(f"chmod +x {root_fs_build_dir}/init")

        exec(f"find . | cpio -ov --format=newc > ../initramfs.cpio 2>/dev/null", root_fs_build_dir)

        return "build/initramfs.cpio"