#!/usr/bin/env bash

src_dir="{{ PROJECT_NAME }}"
docker_name="{{ PROJECT_NAME }}"
tests_dir="tests"
py_files="$src_dir $tests_dir"

source ./venv/bin/activate
function use_venv() { source ./venv/bin/activate; echo "Running '$1'..."; $1; deactivate; }

function run_module() { use_venv "python -m $src_dir"; }

function format() { use_venv "black --line-length=100 $py_files"; use_venv "isort -rc $py_files"; }

function lint() { use_venv "mypy $py_files"; use_venv "flake8 $py_files"; }

function tests() { use_venv "pytest $tests_dir"; }

function docker_build() { docker build --tag "$docker_name" .; }

function docker_run() { docker run -i --rm "$docker_name"; }

function help() {
  cat <<EOF
Run development scripts.

Syntax: $0 [d|db|dr|f|fl|h|l|r|t]
Options:
d     Docker build and docker run.
db    Docker build.
dr    Docker run.
f     Format code with black and isort.
fl    Format and lint.
h     View this help message.
l     Lint with mypy and flake8.
r     Run python module locally in venv.
t     Run pytest in tests directory.
EOF
}

case "$1" in
        d) docker_build && docker_run ;;
        db) docker_build ;;
        dr) docker_run ;;
        f) format ;;
        fl) format; lint; ;;
        h) help; exit ;;
        l) lint ;;
        r) run_module ;;
        t) tests ;;
        *) help; exit 1 ;;
esac
