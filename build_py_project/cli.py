from enum import Enum, auto
from functools import partial
from typing import Callable, Iterable

import click

from . import path_utils, project_builder
from .app_config import app_config


class OptionType(Enum):
    STRING = auto()
    PATH = auto()
    CHOICE = auto()
    FLAG = auto()


def sanitize(_, __, arg: str) -> str:
    return arg.strip()


def validate_path(context, _, path) -> str:
    if not path_utils.dir_exists(path):
        raise click.BadParameter(f"Path does not exist: {path}")

    new_project_path = f"{path}/{context.params['name']}"
    if path_utils.dir_exists(new_project_path):
        raise click.BadParameter(f"Directory already exists: {new_project_path}")

    return path[:-1] if path.endswith("/") else path


def option(
    type: OptionType,
    name: str,
    prompt: str,
    help: str = None,
    choices: Iterable[str] = None,
    default: str = None,
) -> Callable:
    click_option = partial(click.option, f"--{name}", prompt=prompt)
    if help:
        click_option = partial(click_option, help=help)

    if default:
        click_option = partial(click_option, default=default)

    if type == OptionType.STRING:
        return click_option(type=str, callback=sanitize)
    elif type == OptionType.PATH:
        return click_option(type=str, callback=validate_path)
    elif type == OptionType.CHOICE:
        return click_option(type=click.Choice(choices or []))
    elif type == OptionType.FLAG:
        return click_option(is_flag=True)

    return click.option


@click.command()
@option(OptionType.STRING, "name", "Project Name", "The project name.")
@option(
    OptionType.PATH,
    "path",
    "Project Path",
    "Path to new project.",
    default=app_config.user_config.path,
)
@option(
    OptionType.STRING,
    "username",
    "Your Name",
    "Your name.",
    default=app_config.user_config.username,
)
@option(
    OptionType.STRING, "email", "Your Email", "Your email.", default=app_config.user_config.email
)
@option(OptionType.CHOICE, "type", "Project Type", choices=path_utils.get_project_types())
@option(OptionType.FLAG, "helm", "Helm Charts", "Include helm charts.")
def run(name: str, path: str, username: str, email: str, type: str, helm: bool):
    builder = project_builder.ProjectBuilder(name, path, username, email, type, helm)
    builder.build()

    app_config.user_config.update_empty_config_values(username, email, path)
