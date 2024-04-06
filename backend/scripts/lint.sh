#!/usr/bin/env bash

# output log to Github actions
exec > >(tee -ia /dev/tty)

set -e
set -x

mypy app
ruff app
ruff format app --check
