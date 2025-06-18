#!/usr/bin/env bash
set -eu

# @cmd Publish to PyPI
#
# Invoked via "cog bump -a"
publish() {
	git push origin main --tags
	rm -rf dist/
	pip install --upgrade build twine
	python3 -m build
	twine upload dist/*
	rm -rf dist/
}

if ! command -v argc >/dev/null; then
	echo "This command requires argc. Install from https://github.com/sigoden/argc" >&2
	exit 100
fi
eval "$(argc --argc-eval "$0" "$@")"
