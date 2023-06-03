import os
import tarfile

from .util import download_file, make, make_config

class LinuxKernelManager:

    def __init__(self, version: str, build_dir: str) -> None:
        self._version = version
        self._kernels_build_dir = os.path.join(build_dir, "kernels")
        self._download_url = f"https://cdn.kernel.org/pub/linux/kernel/v{self._version[0]}.x/linux-{self._version}.tar.xz"
        self._download_file = os.path.join(self._kernels_build_dir, f"linux-{self._version}.tar.xz")
        self._source_dir = os.path.join(self._kernels_build_dir, f"linux-{self._version}")

    def download_kernel(self) -> None:
        os.makedirs(self._kernels_build_dir, exist_ok=True)

        if not os.path.exists(self._download_file ):
            print(f"Downloading Linux Kernel Version {self._version} from: {self._download_url}")
            download_file(self._download_url, self._download_file )
        else:
            print(f"Linux Kernel {self._version} already downloaded")


    def extract_kernel(self) -> str:
        if not os.path.exists(self._source_dir):
            print(f"Extracting Linux Kernel {self._version} to: " + self._source_dir) 
            with tarfile.open(self._download_file) as f:
                f.extractall(self._kernels_build_dir)
        else:
            print(f"Linux Kernel {self._version} already extracted")

    
    def make_kernel_config(self):
        make_config(self._source_dir, f"Linux Kernel {self._version}")

    def make_kernel(self):
        kernel_build = os.path.join(self._source_dir, "arch/arm64/boot/Image.gz")
        if not os.path.exists(kernel_build):
            print(f"Building Linux Kernel {self._version}")
            make(self._source_dir)
        else:
            print(f"Linux Kernel {self._version} already built")
       