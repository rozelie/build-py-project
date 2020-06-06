import pathlib

import nox
from nox.sessions import Session

CWD = pathlib.Path(__file__).parent.absolute()

SRC_DIR = "PROJECT_NAME"
DOCKER_NAME = "PROJECT_NAME"
TESTS_DIR = "tests"
NOX_FILE = "noxfile.py"
PYTHON_RUNTIME = f"{CWD}/venv/bin/python"
APP_ENV_VARS = []

PY_FILES = " ".join([SRC_DIR, TESTS_DIR, NOX_FILE])

nox.options.python = PYTHON_RUNTIME


def run(session: Session, args: str):
    session.run(*args.split(" "), external=True)


@nox.session
def format(session):
    run(session, f"black --line-length=100 {PY_FILES}")
    run(session, f"isort -rc {PY_FILES}")


@nox.session
def mypy(session):
    run(session, f"mypy {PY_FILES}")


@nox.session
def flake8(session):
    run(session, f"flake8 {PY_FILES}")


@nox.session
def tests(session):
    run(session, f"pytest {TESTS_DIR}")


@nox.session
def local_run(session):
    run(session, f"{PYTHON_RUNTIME} -m {SRC_DIR}")


@nox.session
def docker_build(session):
    run(session, f"docker build --tag {DOCKER_NAME} {CWD}")


@nox.session
def docker_run(session):
    if APP_ENV_VARS:
        env_args = " ".join([f"--env {env_var}" for env_var in APP_ENV_VARS])
        run(session, f"docker run -i --rm {env_args} {DOCKER_NAME}")

    run(session, f"docker run -i --rm {DOCKER_NAME}")
