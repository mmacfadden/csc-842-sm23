import textwrap

from .util import exec

def boot(namespace_dir: str, kernel_config: dict, initrd: str, remote_debug: bool) -> None:
    print("Booting Virtual Machine\n")

    kernel_version = kernel_config["version"]

    kernel_options = []

    if kernel_config.get("disable_kaslr"):
        kernel_options.append("nokaslr")

    if kernel_config.get("disable_smap"):
        kernel_options.append("nosmap")

    if kernel_config.get("disable_smep"):
        kernel_options.append("nosmep")

    if kernel_config.get("disable_pti"):
        kernel_options.append("pti=off")

    if kernel_config.get("quiet"):
        kernel_options.append("quiet")
    
    if "boot_args" in kernel_config:
        kernel_options.append(kernel_config["boot_args"])

    if remote_debug:
        debug_args = "-s -S"
    else:
        debug_args = ""

    qemu_command = textwrap.dedent(
        f"""qemu-system-aarch64 \\
        -M virt -m 1024 -cpu cortex-a53 \\
        -kernel {namespace_dir}/linux-{kernel_version}/arch/arm64/boot/Image.gz \\
        -initrd {initrd} \\
        -netdev user,id=mynet \\
        -device virtio-net-pci,netdev=mynet \\
        -nographic \\
        -no-reboot \\
        -append "panic=-1 {" ".join(kernel_options)}" \\
        {debug_args}
        """
    )

    exec(qemu_command)