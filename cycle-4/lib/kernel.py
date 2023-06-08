import os
import tarfile

from .util import download_file, make, make_config

class LinuxKernelBuilder:
    """
    The LinuxKernelBuilder class handles operations around building a specific
    Linux Kernel from scratch.
    """


    def __init__(self, version: str, build_dir: str, namespace_dir: str) -> None:
        self._version = version
        self._namespace_dir = namespace_dir

        self._download_dir = os.path.join(build_dir, "kernels")
        self._download_url = f"https://cdn.kernel.org/pub/linux/kernel/v{self._version[0]}.x/linux-{self._version}.tar.xz"
        self._download_file = os.path.join(self._download_dir, f"linux-{self._version}.tar.xz")
        
        self._source_dir = os.path.join(self._namespace_dir, f"linux-{self._version}")


    def download_kernel(self) -> None:
        """
        This method downloads the Linux source from kernel.org if it has not
        been downloaded yet.
        """
        os.makedirs(self._download_dir, exist_ok=True)

        if not os.path.exists(self._download_file ):
            print(f"Downloading Linux Kernel Version {self._version} from: {self._download_url}")
            download_file(self._download_url, self._download_file )
        else:
            print(f"Linux Kernel {self._version} already downloaded")


    def extract_kernel(self) -> str:
        """
        Extracts he kernel source if it hasn't already been extracted.
        """
        if not os.path.exists(self._source_dir):
            print(f"Extracting Linux Kernel {self._version} to: " + self._source_dir) 
            with tarfile.open(self._download_file) as f:
                f.extractall(self._namespace_dir)
        else:
            print(f"Linux Kernel {self._version} already extracted")

    
    def make_kernel_config(self) -> None:
        """
        Uses 'make defconfig' to generate a default configuration for the kernel
        if a config has not already been generated.
        """
        make_config(self._source_dir, f"Linux Kernel {self._version}")


    def make_kernel(self, rebuild: bool) -> None:
        """
        Builds the kernel if it hasn't already been built, or if a rebuild is
        requested.
        """
        kernel_build = os.path.join(self._source_dir, "arch/arm64/boot/Image.gz")
        if not os.path.exists(kernel_build) or rebuild:
            print(f"Building Linux Kernel {self._version}")
            make(self._source_dir)
        else:
            print(f"Linux Kernel {self._version} already built")
       