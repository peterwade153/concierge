"""Pytest bootstrap.

Ensures the ``backend`` package directory is importable regardless of the
directory pytest is invoked from (e.g. ``pytest`` from the repo root vs.
``pytest`` from inside ``backend/``).
"""

import os
import sys

_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)