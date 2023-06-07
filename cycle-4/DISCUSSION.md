# Introduction
This project automates the process of creating a lightweight virtual machine using a specific Linux Kernel and supplied root file system.  The tool allows the user to declaratively specify what version of the Linux Kernel is required and how to build the root filesystem.  The tool will download and build the necesary artificats and boot a virtual machine.  The tool also allows the user to customize the kernel and root file system as needed.

When reverse engineering IoT firmware, it is common to get ahold of a root disk image. May of these IoT devices use a MIPS or ARM based Linux OS. When getting ahold of the Firmware, you can often determine the Linux Kernel version.  The ability to supply the firmware's root file system, combine it with the correct Linux Kernel, and boot a virtual machine to emulate the firmware is a very useful tool in the reverse engineering process.

# Interest / Motivation
This project came out of my experiences in CSC 848 (Advanced Software Exploitation) and CSC-844 (Advanced Reverse Engineering). These classes got me into reverse engineering and kernel hacking.  In both classes, and since then, I have had to routinely virtualize or emulate firmware from device vendors. It always seemed more painful that it needed to be to firmware virtualized.  There were a series of routine steps that I had to do over and over again each time.  Not to mention never quite remembering all the commands for QEMU. Each time I would do this, there was a lot of googling to remember exactly how to compile the kernel for a target architecture, create a root filesystem, etc.

Thus this project focused on simplifying that work flow so that I could more quickly get to the firmware analysis or kernel hacking.  Now, I can get a system up and running with only a few minutes of active work.

# Three Main Ideas
The three main ideas for the project are as follows:

1. **Automation**: The main objective of the project was to automate repetitive tasks that have many steps. Several tasks like building a Linux kernel can take quite some time, which requires the user to wait and/or monitor the task to know when to go on to the next task. With this tool, you can basically fire and forget.  When the process is done, you will have a booted virtual machine.  The tool combines operations ranging from compiling kernels, compiling busybox, making file systems, booting VMs with QEMU, etc.

2. **Declarative Configuration**: It of course would be possible to write a simple shell script to automate some of the work. However, this would lead to mixing the logic of the system with the configuration and/or copying and pasting the shell script for different projects w/ different kernels.  The goal of this project was to provide a configuration file that declaratively specifies what the configuration of the system should be and the tool takes care of the rest.  This means you can effectively throw away the build system, and recreate it.  The configuration files can be easily checked into version control independently of the tool

3. **Firmware Emulation and Kernel Hacking**: When I chose this project, I was aware that the tool itself was a little outside the traditional security tool set.  It doesn't deal with network analysis, or exploits, etc.  However, for me, this tool will significantly improve my firmware reverse engineering and kernel module exploitation workflow.  Both activities involve a lot of trial and error, and being able to quickly iterate without tedious, repetitive tasks will increase the speed of the entire process.

# Future Directions
This project lent itself to starting small and continually adding functionality as I tried to boot different systems, firmware, etc.  The code is organized in a way that makes extending over time pretty easy. The main future features I see based on where the project is today are:

  * **Support Different Compilers**: At the moment, only the default compiler for the system is supported.  On my current Kali Linux box that is GCC 12.  Some Linux Kernels (such as 4.x) were intended to be compiled with something like GCC 9.x.  I'd like to extend the Kernel configuration to specify what compilers to use.
  * **Support Different CPU Architectures**: There is a placeholder in the configuration for the CPU architecture to build for.  Right now, this configuration is ignored and the Kernel is built for whatever architecture you are on.  Ideally the Kernel could be cross compiled to the target Architecture and then QEMU would boot the appropriate type of virtual machine.  This is completely doable, just not within the time frame of the project.
  * **Additional Filesystem Modules**: Right now the tool supports building the root filesystem from BusyBox (with additional files), or using a directory.  There are lots of other common use cases including a disk image like SquashFS, or a raw DD image.  This can be easily added in the future, and would help support more firmware reverse engineering scenarios.
  

# Source Code
The source code is located on GitHub hat the URL below.  The repository's README contains additional technical details about the project.:

https://github.com/mmacfadden/csc-842-sm23/tree/master/cycle-4/


# Video
A demonstration / walkthrough video has been posted to YouTube here:

https://youtu.be/bNNDqdya3Sw
