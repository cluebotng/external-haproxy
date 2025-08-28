#!/usr/bin/env python3
import json
import os
import sys
from dataclasses import dataclass
from pathlib import PosixPath
from typing import Optional, List, Union, Dict, Any


def write_config(config_path: PosixPath) -> None:
    backend_hostname = os.environ.get("WEBSERVICE_BACKEND_HOSTNAME")
    backend_port = os.environ.get("WEBSERVICE_BACKEND_PORT", "8000")

    if not backend_hostname or not backend_port:
        raise RuntimeError("Missing BACKEND_HOSTNAME or BACKEND_PORT")

    try:
        backend_port = int(backend_port)
    except ValueError:
        raise RuntimeError("BACKEND_PORT does not appear to be a valid number")

    config = ''
    config += 'defaults\n'
    config += '  mode http\n'
    config += '  timeout connect 5s\n'
    config += '  timeout client 5s\n'
    config += '  timeout server 60s\n'

    config += 'frontend ingress\n'
    config += '  bind *:8000\n'
    config += '  default_backend kubernetes\n'
    config += '  acl health_check path -i /_/health\n'
    config += '  http-request return status 200 if health_check\n'

    config += 'backend kubernetes\n'
    config += f'  server service {backend_hostname}:{backend_port} check\n'

    with config_path.open('w') as fh:
        fh.write(config)


def run_haproxy(config_path: PosixPath):
    # Note: We replace the current process, rather than running as a sub-process
    return os.execv("/layers/heroku_deb-packages/packages/usr/sbin/haproxy",
                    ["haproxy", "-f", config_path.as_posix()])


def main():
    config_path = PosixPath("/tmp/haproxy.conf")
    write_config(config_path)
    run_haproxy(config_path)


if __name__ == "__main__":
    main()
