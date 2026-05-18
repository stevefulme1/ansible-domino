"""Shared pytest fixtures for stevefulme1.domino collection unit tests."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import sys
import types
from unittest.mock import MagicMock

import pytest

# Provide a mock requests library if not installed
try:
    import requests as _real_requests  # noqa: F401
except ImportError:
    _requests = MagicMock()
    sys.modules["requests"] = _requests

# Set up namespace package for collection imports
_collection_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
_namespace_root = os.path.abspath(os.path.join(_collection_root, os.pardir, os.pardir))
if os.path.isdir(os.path.join(_namespace_root, "ansible_collections")) and _namespace_root not in sys.path:
    sys.path.insert(0, _namespace_root)

try:
    import ansible_collections.stevefulme1.domino  # noqa: F401
except (ImportError, ModuleNotFoundError):
    for _pkg_name in ("ansible_collections", "ansible_collections.stevefulme1"):
        if _pkg_name not in sys.modules:
            _pkg = types.ModuleType(_pkg_name)
            _pkg.__path__ = []
            _pkg.__package__ = _pkg_name
            sys.modules[_pkg_name] = _pkg

    _col_mod = types.ModuleType("ansible_collections.stevefulme1.domino")
    _col_mod.__path__ = [_collection_root]
    _col_mod.__package__ = "ansible_collections.stevefulme1.domino"
    sys.modules["ansible_collections.stevefulme1.domino"] = _col_mod
    sys.modules["ansible_collections"].stevefulme1 = sys.modules["ansible_collections.stevefulme1"]
    sys.modules["ansible_collections.stevefulme1"].domino = _col_mod


@pytest.fixture
def module_args():
    """Return a base dict of common module arguments."""
    return {
        "api_url": "https://app.dominodatalab.com",
        "api_key": "test-api-key-12345",
        "validate_certs": True,
        "timeout": 30,
        "state": "present",
    }
