# -*- coding: utf-8 -*-
# Copyright (c) 2025, Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Documentation fragment for Domino Data Lab common options."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment:
    """Common documentation fragment for Domino Data Lab modules."""

    DOCUMENTATION = r"""
options:
    api_url:
        description:
            - The URL of the Domino Data Lab API.
            - Can also be set via the C(DOMINO_API_URL) environment variable.
        type: str
        required: true
    api_key:
        description:
            - The API key for authentication.
            - Can also be set via the C(DOMINO_API_KEY) environment variable.
        type: str
        required: true
        no_log: true
    validate_certs:
        description:
            - Whether to validate SSL certificates.
        type: bool
        default: true
    timeout:
        description:
            - API request timeout in seconds.
        type: int
        default: 30
"""
