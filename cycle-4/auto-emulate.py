#!/usr/bin/env python3

import os

from lib.kernel import LinuxKernelBuilder
from lib.busybox import BusyBoxFileSystemBuilder
from lib.util import exec, die
from lib.config import ConfigManager
from lib.qemu import boot

##
## Constants
##
BUILD_DIR = ".build"
NAMESPACES_DIR = "namespaces"

##
## Config Parsing
##
config_manager = ConfigManager()
config = config_manager.parse()

namespace_dir = os.path.join(BUILD_DIR, NAMESPACES_DIR, config.namespace)


##
## Kernel Download and build
##
if config.command == "boot" or config.command == "build-kernel":
    kernel_version = config.kernel["version"]
    kernel_builder = LinuxKernelBuilder(kernel_version, BUILD_DIR, namespace_dir)
    kernel_builder.download_kernel()
    kernel_builder.extract_kernel()
    kernel_builder.make_kernel_config()
    kernel_builder.make_kernel(config.command == "build-kernel")


##
## Root Filesystem Handling
##
if config.command == "boot" or config.command == "build-fs":
    rebuild_fs = config.command == "build-fs"

    if config.root_fs_type == "busy_box":
        busy_box_config = config.root_fs["busy_box"]

        busy_box_manager = BusyBoxFileSystemBuilder(busy_box_config, BUILD_DIR, namespace_dir)
        
        busy_box_manager.download_busybox()
        busy_box_manager.extract_busy_box()
        busy_box_manager.make_busybox_config()
        busy_box_manager.make_busybox(rebuild_fs)

        initrd = busy_box_manager.build_root_fs("root_fs", rebuild_fs)

    elif config.root_fs_type == "dir":
        root_dir = config.root_fs["dir"]
        working_dir = os.getcwd()
        initramfs = os.path.join(working_dir, namespace_dir, "initramfs.cpio")
        exec(f"find . | cpio -ov --format=newc > {initramfs} 2>/dev/null", root_dir)
        initrd = initramfs
    else:
        die(f"Unexpected root fs type: {config.root_fs_type}")


##
## VM Boot
##
if (config.command == "boot"):
    boot(namespace_dir, config.kernel, config.virtual_machine, initrd)
