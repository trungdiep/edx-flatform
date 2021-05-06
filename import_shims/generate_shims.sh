#!/usr/bin/env bash
#
# Context: docs/decisions/0007-sys-path-modification-removal.rst
#
# Usage:
#
#      ~/edx-platform> import_shims/generate_shims.sh SOURCE DESTINATION
#
#    where the modules in SOURCE should recursively have shims generated in DESTINATION,
#    which should be a subfolder of import_shims/.
#
#    SOURCE and DESTINATION must both be relative to the root of edx-platform,
#    and must not include trailing slashes.
#
# For example:
#
#      ~/edx-platform> import_shims/generate_shims.sh common/djangoapps import_shims/studio
#
#    will mirror the packages structure of `common/djangoapps` within `import_shims/studio`.
#    One would run this if they want to mimic the effect of adding 'common/djangoapps'
#    to `sys.path` within Studio.

# Shellcheck recommends using search/replace instead of sed. It's fine as is.
# shellcheck disable=SC2001

set -e
set -o pipefail
set -u

SOURCE="$1"
PYTHON_SOURCE="${SOURCE/\//.}"
DESTINATION="$2"
for path in $(find "${SOURCE}/" -name '*.py' | grep -v migrations); do
    if [[ "$path" == "${SOURCE}/__init__.py" ]]; then
        # Skip unnecessary root __init__.py.
        continue
    fi
    if [[ "$path" == "lms/djangoapps/courseware/management/commands/import.py" ]]; then
        # Skip this file because its name is problematic for import shim.
        # We've gone to prod with this excluded, and it hasn't been a problem.
        continue
    fi
    if [[ "$path" == "cms/djangoapps/contentstore/management/commands/import.py" ]]; then
        # Also skip this file because its name is problematic for the import shim.
        continue
    fi
    new_path=$(echo "$path" | sed "s#${SOURCE}/#${DESTINATION}/#")
    new_python_path=$(echo "$path" | sed "s#/#.#g" | sed "s#.py##" | sed "s#.__init__##")
    old_python_path=$(echo "$new_python_path" | sed "s#${PYTHON_SOURCE}.##")
    echo "Writing ${new_path}"
    mkdir -p "$(dirname "$new_path")"
    {
        echo '"""Deprecated import support. Auto-generated by import_shims/generate_shims.sh."""'
        echo "# pylint: disable=redefined-builtin,wrong-import-position,wildcard-import,useless-suppression,line-too-long"
        echo
        echo "from import_shims.warn import warn_deprecated_import"
        echo
        echo "warn_deprecated_import('${old_python_path}', '${new_python_path}')"
        echo
        echo "from ${new_python_path} import *"
    } > "$new_path"
done