# -*- coding: utf-8 -*-
# Copyright (c) 2025, Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Shared Domino Data Lab API client utilities."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


COMMON_ARGS = dict(
    api_url=dict(type="str", required=True),
    api_key=dict(type="str", required=True, no_log=True),
    validate_certs=dict(type="bool", default=True),
    timeout=dict(type="int", default=30),
)


class ApiClient:
    """Simple REST client for Domino Data Lab API."""

    def __init__(self, module):
        """Initialize the API client."""
        self.module = module
        self.base_url = module.params["api_url"].rstrip("/")
        self.api_key = module.params["api_key"]
        self.validate_certs = module.params["validate_certs"]
        self.timeout = module.params["timeout"]
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        self.session.verify = self.validate_certs

    def _request(self, method, path, data=None, params=None):
        """Send an HTTP request to the API."""
        url = f"{self.base_url}{path}"
        try:
            resp = self.session.request(
                method, url, json=data, params=params, timeout=self.timeout,
            )
            resp.raise_for_status()
            if resp.content:
                return resp.json()
            return None
        except requests.exceptions.HTTPError as exc:
            body = ""
            if exc.response is not None:
                body = exc.response.text
            self.module.fail_json(
                msg=f"{method} {url} failed: {body}",
            )
        except requests.exceptions.RequestException as exc:
            self.module.fail_json(msg=f"Request to {url} failed: {exc}")

    def get(self, path, params=None):
        """Send a GET request."""
        return self._request("GET", path, params=params)

    def post(self, path, data=None):
        """Send a POST request."""
        return self._request("POST", path, data=data)

    def put(self, path, data=None):
        """Send a PUT request."""
        return self._request("PUT", path, data=data)

    def patch(self, path, data=None):
        """Send a PATCH request."""
        return self._request("PATCH", path, data=data)

    def delete(self, path):
        """Send a DELETE request."""
        return self._request("DELETE", path)
