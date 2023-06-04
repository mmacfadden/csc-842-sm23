#!/usr/bin/env python3

import os

from lib.kernel import LinuxKernelManager
from lib.busybox import BusyBoxManager
from lib.util import exec, die
from lib.config import ConfigManager
from lib.qemu import boot

BUILD_DIR = ".build"
NAMESPACES_DIR = "namespaces"

##
## Config Parsing
##
config_manager = ConfigManager()
config = config_manager.parse()

namespace_dir = os.path.join(BUILD_DIR, NAMESPACES_DIR, config.namespace)

##
## Kernel
##
if config.command == "boot" or config.command == "build-kernel":
    kernel_version = config.kernel["version"]
    kernel_manager = LinuxKernelManager(kernel_version, BUILD_DIR, namespace_dir)
    kernel_manager.download_kernel()
    kernel_manager.extract_kernel()
    kernel_manager.make_kernel_config()
    kernel_manager.make_kernel(config.command == "build-kernel")


##
## Root Filesystem
##
if config.command == "boot" or config.command == "build-fs":
    rebuild_fs = config.command == "build-fs"

    if config.root_fs_type == "busy_box":
        busy_box_version = config.root_fs["busy_box"]

        busy_box_manager = BusyBoxManager(busy_box_version, BUILD_DIR, namespace_dir)
        
        busy_box_manager.download_busybox()
        busy_box_manager.extract_busy_box()
        busy_box_manager.make_busybox_config()
        busy_box_manager.make_busybox(rebuild_fs)

        initrd = busy_box_manager.build_root_fs("root_fs", rebuild_fs)

    elif config.root_fs_type == "dir":
        root_dir = config.root_fs["dir"]
        working_dir = os.getcwd()
        exec(f"find . | cpio -ov --format=newc > {working_dir}/build/initramfs.cpio", root_dir)
        initrd = "build/initramfs.cpio"
    else:
        die(f"Unexpected root fs type: {config.root_fs_type}")

##
## Boot
##
if (config.command == "boot"):
    boot(namespace_dir, config.kernel, initrd, config.remote_debug)
