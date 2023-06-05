# Cycle 4: TBD
Introduction TBD

## Requirements
The main requirements of the project that influenced the functionality and design are as follows:

  * TBD

## Design


## Video
A demonstration video can be found on YouTube here:

[https://youtu.be/TBD](https://youtu.be/TBD)


## Dependencies and Setup
The project has the following dependencies:

* [Python 3](https://www.python.org/): >= 3.11.x
* [Pip](https://pip.pypa.io/en/stable/): >= 23.0
* [QEMU](https://www.qemu.org/): >= 7.2

### Python Dependencies
Install the Python dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Usage


## Configuration
The tool is configured via a yaml file.  The syntax for the configuration file is shown below:

```yaml
# Provides a namespace for the project in the build directory so that multiple
# projects do not conflict with each other.
namespace: test

# The CPU architecture to compile for and virtualize.
# Currently supported: amd64, x64
architecture: x64

# Whether to enable remote debugging when the virtual machine boots.
# Defaults to false.
remote_debug: false

# Configures the linux kernel to use and various boot parameters to pass
# to the kernel when booting the virtual machine.
kernel: 
  version: 6.3.5
  disable_kaslr: true
  disable_smap: true
  disable_smep: true
  disable_pti: true
  quiet: true
  boot_args: ""

# Configures how the root file system will be built out.
# 
# Note that only one of the following top level options may be present
# (although all are shown for documentation purposes.):
#    * busy_box
#    * dir
root_filesystem: 
  # Specifies that the root filesystem should be populated using
  # Busy Box.
  busy_box:
    # The version of BusyBox to us.
    version: 1.36.1

    # The UID to run the root shell as.
    uid: 1000
    
    # Additional files to include.
    includes:
      - from: examples/test/module/kmod.ko
        to: /
    
    # Extra command to run in the init process.
    init_extra: "insmod /kmod.ko"

  # Specifies the root files system should be build using the
  # supplied directory.
  dir: "root_fs"
```

TODOs
  - handle architecture