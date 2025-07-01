#!/bin/sh

# Get directory of this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
XTRADER_DIR="$SCRIPT_DIR/../xtrader"

cd "$XTRADER_DIR" || exit 1


# Remove unused imports/variables (F403, F405, F841)
autoflake --in-place --remove-all-unused-imports --remove-unused-variables -r .

# Fix import order (E402)
isort .

# Auto-format code (E501, E203, etc.)
black --line-length 79 .

# Fix docstrings
docformatter --in-place -r .

# Fix bare except (E722), None comparisons (E711), etc.
ruff check --fix .
