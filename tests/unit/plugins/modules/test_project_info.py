"""Unit tests for stevefulme1.domino.project_info module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from unittest.mock import MagicMock, patch


MODULE_PATH = "ansible_collections.stevefulme1.domino.plugins.modules.project_info"
CLIENT_PATH = "ansible_collections.stevefulme1.domino.plugins.module_utils.api_client"


class TestInfo:
    """Test project_info info retrieval."""

    @patch(f"{CLIENT_PATH}.requests")
    def test_list_projects(self, mock_requests, module_args):
        """Listing projects returns items."""
        mock_response = MagicMock()
        mock_response.json.return_value = [{"id": "1", "name": "test"}]
        mock_response.raise_for_status.return_value = None
        mock_response.content = b'[{"id":"1"}]'
        mock_requests.Session.return_value.request.return_value = mock_response

        from ansible_collections.stevefulme1.domino.plugins.module_utils.api_client import ApiClient

        mock_module = MagicMock()
        mock_module.params = module_args
        client = ApiClient(mock_module)
        result = client.get("/api/v1/projects")
        assert result is not None
