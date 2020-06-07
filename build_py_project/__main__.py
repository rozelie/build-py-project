from enum import Enum, auto
from functools import partial
from typing import Iterable

import click

from . import path_utils, project_builder


class OptionType(Enum):
    STRING = auto()
    PATH = auto()
    CHOICE = auto()
    FLAG = auto()


def sanitize(_, __, arg: str) -> str:
    return arg.strip()


def validate_path(context, _, path):
    if not path_utils.dir_exists(path):
        raise click.BadParameter(f"Path does not exist: {path}")

    new_project_path = f"{path}/{ context.params['name']}"
    if path_utils.dir_exists(new_project_path):
        raise click.BadParameter(f"Directory already exists: {new_project_path}")

    return path[:-1] if path.endswith("/") else path


def option(
    type: OptionType, name: str, prompt: str, help: str = None, choices: Iterable[str] = None,
):
    click_option = partial(click.option, f"--{name}", prompt=prompt)
    if help:
        click_option = partial(click_option, help=help)

    if type == OptionType.STRING:
        return click_option(type=str, callback=sanitize)
    elif type == OptionType.PATH:
        return click_option(type=str, callback=validate_path)
    elif type == OptionType.CHOICE:
        return click_option(type=click.Choice(choices or []))
    elif type == OptionType.FLAG:
        return click_option(is_flag=True)


@click.command()
@option(OptionType.STRING, "name", "Project Name", "The project name.")
@option(OptionType.PATH, "path", "Project Path", "Path to new project.")
@option(OptionType.STRING, "username", "Your Name", "Your name.")
@option(OptionType.STRING, "email", "Your Email", "Your email.")
@option(OptionType.CHOICE, "type", "Project Type", choices=path_utils.get_project_types())
@option(OptionType.FLAG, "helm", "Project Type", "Include helm charts.")
def cli(name: str, path: str, username: str, email: str, type: str, helm: bool):
    builder = project_builder.ProjectBuilder(name, path, username, email, type, helm)
    builder.build()


if __name__ == "__main__":
    cli()
