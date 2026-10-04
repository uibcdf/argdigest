set -euo pipefail
# The shared publisher already freezes the reviewed version before conda-build.
"$PYTHON" -m pip install --no-deps --no-build-isolation --ignore-installed .
