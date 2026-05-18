# -*- coding: utf-8 -*-
# Copyright (c) 2025, Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module to query Domino Data Lab workspace resources."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: workspace_info
short_description: List or retrieve Domino workspaces
description:
    - Retrieve information about Domino Data Lab workspace resources.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    project_id:
        description:
            - The project id for the Domino Data Lab resource.
        type: str
    workspace_id:
        description:
            - The workspace id for the Domino Data Lab resource.
        type: str
extends_documentation_fragment:
    - stevefulme1.domino.common
requirements:
    - "python >= 3.9"
    - "requests"
"""

EXAMPLES = r"""
- name: List all workspaces
  stevefulme1.domino.workspace_info:
    api_url: "https://app.dominodatalab.com"
    api_key: "my-api-key"
"""

RETURN = r"""
workspaces:
    description: List of workspace resources.
    returned: always
    type: list
    elements: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.domino.plugins.module_utils.api_client import (
    COMMON_ARGS,
    ApiClient,
    HAS_REQUESTS,
)


def main():
    argument_spec = dict(
        project_id=dict(type="str"),
        workspace_id=dict(type="str"),
    )
    argument_spec.update(COMMON_ARGS)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    if not HAS_REQUESTS:
        module.fail_json(msg="The 'requests' library is required. Install with: pip install requests")

    client = ApiClient(module)
    params = module.params

    if params.get("project_id"):
        result = client.get(f"/api/v1/workspaces/{params['project_id']}")
        module.exit_json(changed=False, workspaces=[result] if result else [])
    else:
        result = client.get("/api/v1/workspaces")
        items = result if isinstance(result, list) else result.get("data", result.get("items", []))
        module.exit_json(changed=False, workspaces=items)


if __name__ == "__main__":
    main()
