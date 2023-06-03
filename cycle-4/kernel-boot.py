#!/usr/bin/env python3

import requests
import os
import tarfile
import yaml
import argparse
import subprocess
import re
import textwrap
import shutil


parser = argparse.ArgumentParser(
                    prog='kernel-booter',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('command')          
parser.add_argument('-c', '--config', help="The configure file to use.", default="vm-config.yml")  

args = parser.parse_args()

config_file = args.config

##
## Functions
##
def load_config(config_file):
    
    if not os.path.exists(config_file):
        print("Config file not found: " + config_file)
        exit(1)
        
    with open(config_file, "r") as f:
        try:
            config = yaml.safe_load(f)
            return config
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)

def build_kernel_url(version: str) -> str:
    v = version[0]
    return f"https://cdn.kernel.org/pub/linux/kernel/v{v}.x/linux-{version}.tar.xz"


def download_kernel(version) -> str:
    os.makedirs("build/kernels", exist_ok=True)

    kernel_download_file = f"build/kernels/linux-{version}.tar.xz"

    if not os.path.exists(kernel_download_file):
        kernel_url = build_kernel_url(version)
        print(f"Downloading kernel from: {kernel_url}")
        download_file(kernel_url, kernel_download_file)
    else:
        print("Kernel already downloaded")

    return kernel_download_file


def extract_kernel(version: str, download_file) -> str:
    extract_dir = f"build/kernels/linux-{version}"

    if not os.path.exists(extract_dir):
        print("Extracting kernel to: " + extract_dir)
        os.makedirs(extract_dir, exist_ok=True)
        with tarfile.open(download_file) as f:
            f.extractall("kernels")
    else:
        print("Kernel already extracted")

    return extract_dir


def make_config(source_dir, label):
    config_file = os.path.join(source_dir, ".config")

    if not os.path.exists(config_file):
        print("Config file not found, generating default config")
        p = subprocess.Popen(["make", "defconfig"], cwd=source_dir)
        p.wait()
    else:
        print(f"{label} configuration already exists")

def download_file(download_url, target_file) -> str:
    r = requests.get(download_url, allow_redirects=True)
    with open(target_file, "wb") as output_file:
        output_file.write(r.content)


def download_busybox(busy_box_version):
    os.makedirs("build/busybox", exist_ok=True)
    busy_box_file = f"busybox-{busy_box_version}.tar.bz2"
    download = f"build/busybox/{busy_box_file}"

    if not os.path.exists(download):
        busy_box_url = f"https://busybox.net/downloads/{busy_box_file}"
        print(f"Downloading busy box from {busy_box_url}")
        download_file(busy_box_url, download)
    else:
        print("Busy box already downloaded")

    return download
    

def extract_busy_box(version: str, download_file) -> str:
    extract_dir = f"build/busybox/busybox-{version}"
    if not os.path.exists(extract_dir):
        print("Extracting Busy Box to: " + extract_dir)
        with tarfile.open(download_file) as f:
            f.extractall("build/busybox")
    else:
        print("Kernel already extracted")

    return extract_dir

def make(kernel_dir):
    p = subprocess.Popen(["make", "-j2"], cwd=kernel_dir)
    p.wait()


def make_kernel(kernel_dir):
    kernel_build = os.path.join(kernel_dir, "arch/arm64/boot/Image.gz")
    if not os.path.exists(kernel_build):
        print("building kernel")
        make(kernel_dir)
    else:
        print("Kernel already built")
        

def update_busy_box_config(busybox_source_dir):
    config_path = os.path.join(busybox_source_dir, ".config")
    with open(config_path, "r") as config:
        lines = config.readlines()

    with open(config_path, "w") as sources:
        for line in lines:
            sources.write(re.sub(r'^# CONFIG_STATIC is not set$', 'CONFIG_STATIC=y', line))

def make_busybox(busybox_source_dir):
    busy_box_build = os.path.join(busybox_source_dir, "_install")
    if not os.path.exists(busy_box_build):
        print("building busy box")
        make(busybox_source_dir)
        exec("make install", busybox_source_dir)
    else:
        print("Busy Box already built")

def exec(command: str, working_dir="."):
    p = subprocess.Popen(command, shell=True, cwd=working_dir)
    p.wait()
    

def write_init(uid: int, root_fs_build_dir) -> str:
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

def build_root_fs(root_fs_dir):

    root_fs_build_dir = os.path.join("build", root_fs_dir)

    shutil.rmtree(root_fs_build_dir, ignore_errors=True)

    os.makedirs(root_fs_build_dir, exist_ok=True)
    
    exec(f"cp -av {busybox_source_dir}/_install/* {root_fs_build_dir}")
    exec("rm linuxrc", root_fs_build_dir)
    exec("mkdir proc sys dev tmp", root_fs_build_dir)
    write_init(1000, root_fs_build_dir)
    # exec(f"cp init.template.sh {root_fs_build_dir}/init")
    exec(f"chmod +x {root_fs_build_dir}/init")

    exec(f"find . | cpio -ov --format=newc > ../initramfs.cpio", root_fs_build_dir)


def boot(kernel_version):
    print("Booting Kernel")

    qemu_command = textwrap.dedent(
        f"""qemu-system-aarch64 \
        -M virt -m 1024 -cpu cortex-a53 \
        -kernel build/kernels/linux-{kernel_version}/arch/arm64/boot/Image.gz \
        -initrd build/initramfs.cpio \
        -netdev user,id=mynet \
        -device virtio-net-pci,netdev=mynet \
        -nographic -no-reboot \
        -append "panic=-1"
        """
    )

    exec(qemu_command)

config = load_config(config_file)


kernel_version = config["kernel_version"]
downloaded_kernel_file = download_kernel(kernel_version)
kernel_dir = extract_kernel(kernel_version, downloaded_kernel_file)

make_config(kernel_dir, "Kernel")

make_kernel(kernel_dir)

busy_box_version = config["root_filesystem"]["busy_box"]

downloaded_busybox_archive = download_busybox(busy_box_version)
busybox_source_dir = extract_busy_box(busy_box_version, downloaded_busybox_archive)

make_config(busybox_source_dir, "Busybox")
update_busy_box_config(busybox_source_dir)

make_busybox(busybox_source_dir)


root_fs_dir = "root_fs"

build_root_fs(root_fs_dir)
boot(kernel_version)
