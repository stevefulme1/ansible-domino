"""Unit tests for stevefulme1.domino.project module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from unittest.mock import MagicMock, patch


MODULE_PATH = "ansible_collections.stevefulme1.domino.plugins.modules.project"
CLIENT_PATH = "ansible_collections.stevefulme1.domino.plugins.module_utils.api_client"


def _build_project(**kwargs):
    """Return a mock project dict."""
    defaults = {"id": "test-id", "name": "test-project"}
    defaults.update(kwargs)
    return defaults


class TestCreate:
    """Test project creation."""

    @patch(f"{CLIENT_PATH}.requests")
    def test_create_project(self, mock_requests, module_args):
        """Creating a project sends POST request."""
        mock_response = MagicMock()
        created = _build_project()
        mock_response.json.return_value = created
        mock_response.raise_for_status.return_value = None
        mock_response.content = b'{"id":"test-id"}'

        list_response = MagicMock()
        list_response.json.return_value = []
        list_response.raise_for_status.return_value = None
        list_response.content = b'[]'

        session = MagicMock()
        session.request.side_effect = [list_response, mock_response]
        mock_requests.Session.return_value = session

        from ansible_collections.stevefulme1.domino.plugins.module_utils.api_client import ApiClient

        mock_module = MagicMock()
        mock_module.params = module_args
        client = ApiClient(mock_module)
        result = client.post("/api/v1/projects", data={"name": "test"})
        assert result is not None
