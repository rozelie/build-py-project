#!/usr/bin/env bash

src_dir="build_py_project"
docker_name="build_py_project"
tests_dir="tests"
py_files=("$src_dir" "$tests_dir")

source ./venv/bin/activate

function run_module() { python -m "$src_dir"; }

function format() { black --line-length=100 "${py_files[@]}"; isort -rc "${py_files[@]}"; }

function lint() { mypy "${py_files[@]}"; flake8 "${py_files[@]}"; }

function tests() { pytest "${py_files[@]}"; }

function update_requirements() { pipdeptree -f --warn silence | grep -v '^ ' > requirements.txt; }

function docker_build() { docker build --tag "$docker_name" .; }

function docker_run() { docker run -i --rm "$docker_name"; }

function help() {
  cat <<EOF
Run development scripts.

Syntax: $0 [d|db|dr|f|fl|h|l|r|t|u]
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
u     Update requirements.txt.
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
        u) update_requirements ;;
        *) help; exit 1 ;;
esac
