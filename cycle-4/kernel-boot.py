#!/usr/bin/env python3

import os
import textwrap

from lib.kernel import LinuxKernelManager
from lib.busybox import BusyBoxManager
from lib.util import exec, die
from lib.config import ConfigManager


config_manager = ConfigManager()
config = config_manager.parse()


def boot(kernel_version, initrd):
    print("Booting Kernel")

    qemu_command = textwrap.dedent(
        f"""qemu-system-aarch64 \\
        -M virt -m 1024 -cpu cortex-a53 \\
        -kernel build/kernels/linux-{kernel_version}/arch/arm64/boot/Image.gz \\
        -initrd {initrd} \\
        -netdev user,id=mynet \\
        -device virtio-net-pci,netdev=mynet \\
        -nographic \\
        -no-reboot \\
        -append "panic=-1"
        """
    )

    exec(qemu_command)


##
## Kernel
##
kernel_version = config.kernel["version"]
kernel_manager = LinuxKernelManager(kernel_version, "build")
kernel_manager.download_kernel()
kernel_manager.extract_kernel()
kernel_manager.make_kernel_config()
kernel_manager.make_kernel()


##
## Root Filesystem
##
if config.root_fs_type == "busy_box":
    busy_box_version = config.root_fs["busy_box"]

    busy_box_manager = BusyBoxManager(busy_box_version, "build")
    
    busy_box_manager.download_busybox()
    busy_box_manager.extract_busy_box()
    busy_box_manager.make_busybox_config()
    busy_box_manager.make_busybox()

    initrd = busy_box_manager.build_root_fs("root_fs")

elif config.root_fs_type == "dir":
    root_dir = config.root_fs["dir"]
    working_dir = os.getcwd()
    exec(f"find . | cpio -ov --format=newc > {working_dir}/build/initramfs.cpio", root_dir)
    initrd = "build/initramfs.cpio"
else:
    die(f"Unexpected root fs type: {config.root_fs_type}")

boot(kernel_version, initrd)