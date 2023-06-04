# Cycle 4: TBD


# Configuration
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
  # the specified busybox version.
  busy_box: 1.36.1

  # Specifies the root files system should be build using the
  # supplied directory.
  dir: "root_fs"
```

TODOs
  - handle namespace
  - handle architecture
  - handle different root fs