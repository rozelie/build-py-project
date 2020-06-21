import logging
import os
import sys
from typing import Any, Optional

from .printer import print_green
from .user_config import UserConfig

logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    stream=sys.stdout,
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


def from_env(env_var: str, default: Any = None, exit_if_missing=True) -> Optional[Any]:
    try:
        return os.environ[env_var]
    except KeyError:
        if exit_if_missing:
            logger.info(f"Missing env var for {env_var}")
            sys.exit(1)

        return default


class AppConfig:
    def __init__(self):
        self.app_name = "Build Py Project"
        print_green(self.app_name)

        self.user_config = UserConfig.from_file()


app_config = AppConfig()
