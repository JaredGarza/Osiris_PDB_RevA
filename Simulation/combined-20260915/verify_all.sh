#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
exec python verify_all.py "$@"
