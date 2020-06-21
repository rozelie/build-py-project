import sys

import yaml

from . import commands
from .path_utils import expand_home_dir, file_exists
from .printer import print_err, print_info

CONFIG_PATH = f"{expand_home_dir()}/.build_py_project_config"


def write_new_config():
    print_info(f"Writing new config file to {CONFIG_PATH}")
    config_values = {"username": None, "email": None, "path": None}
    with open(CONFIG_PATH, "w") as new_config:
        yaml.dump(config_values, new_config)


class UserConfig:
    def __init__(self, username: str = None, email: str = None, path: str = None, **kwargs):
        self.username = username
        self.email = email
        self.path = path

    @classmethod
    def from_file(cls):
        if not file_exists(CONFIG_PATH):
            write_new_config()

        with open(CONFIG_PATH, "r") as config_file:
            try:
                print_info(f"Loading config from {CONFIG_PATH}")
                return cls(**yaml.safe_load(config_file))
            except yaml.YAMLError:
                print_err(f"Error in parsing config yaml at: {CONFIG_PATH}")
                user_in = input(
                    "Please fix parsing error to continue, or enter [w] to create a new config file: "
                )
                if user_in.lower() == "w":
                    commands.rm_file(CONFIG_PATH)
                    return UserConfig.from_file()

                sys.exit(1)

    def update_empty_config_values(self, username: str, email: str, path: str):
        self.username = self.username or username
        self.email = self.email or email
        self.path = self.path or path
        with open(CONFIG_PATH, "w") as new_config:
            yaml.dump(self.__dict__, new_config)
