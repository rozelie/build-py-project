from subprocess import PIPE, Popen
from typing import Tuple

import click

from . import path_utils


def run(command: str) -> Tuple[str, str, int]:
    click.echo(f"\tcmd: {command}")
    handle = Popen(command.split(), stdout=PIPE, stderr=PIPE, close_fds=True)
    stdout, stderr = handle.communicate()
    return (
        stdout.decode("utf8").strip(),
        stderr.decode("utf8").strip(),
        handle.returncode,
    )


def mkdir(dir_path: str):
    run(f"mkdir {dir_path}")


def cp(source: str, target: str, unpack=False):
    source = f"{source}/" if unpack else source
    run(f"cp -r {source} {target}")


def rm_dir(dir_path: str):
    run(f"rm -rf {dir_path}")


def rename_dir(dir_path: str, new_name: str):
    run(f"mv {dir_path} {path_utils.get_parent(dir_path)}/{new_name}")
