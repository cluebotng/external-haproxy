#!/usr/bin/env python3
import shutil
import subprocess
from pathlib import PosixPath


def appease_poetry():
    # Poetry expects a Python package from `setup.py install`, create a minimal one
    package_dir = PosixPath("/workspace/haproxy")
    package_dir.mkdir(parents=True)
    (package_dir / "__init__.py").open("w").close()


def main():
    appease_poetry()


if __name__ == "__main__":
    main()
