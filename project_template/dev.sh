#!/bin/bash

help() {
   echo "Run development scripts."
   echo
   echo "Syntax: $0 [d|db|dr|f|h|r|t]"
   echo "Options:"
   echo "d     Docker build and docker run."
   echo "db    Docker build."
   echo "dr    Docker run."
   echo "f     Format code with black and isort."
   echo "h     View this help message."
   echo "l     Lint with mypy and flake8."
   echo "r     Run python module locally in venv."
   echo "t     Run pytest in tests directory."
   echo
}

noxSessions() {
  sessions=("$@")
  source ./venv/bin/activate
  nox --reuse-existing-virtualenvs --sessions "${sessions[@]}"
  deactivate
}

case "$1" in
        d) sessions=("docker_build" "docker_run") ;;
        db) sessions=("docker_build") ;;
        dr) sessions=("docker_run") ;;
        f) sessions=("format") ;;
        h) help; exit ;;
        l) sessions=("mypy" "flake8") ;;
        r) sessions=("local_run") ;;
        t) sessions=("tests") ;;
        *) help; exit 1 ;;
esac

noxSessions "${sessions[@]}"
