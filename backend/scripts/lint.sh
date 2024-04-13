#!/usr/bin/env bash

set -e
set -x

mypy app
ruff app --fix
ruff format app
