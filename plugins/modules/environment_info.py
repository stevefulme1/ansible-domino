# -*- coding: utf-8 -*-
# Copyright (c) 2025, Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module to query Domino Data Lab environment resources."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: environment_info
short_description: List or retrieve Domino environments
description:
    - Retrieve information about Domino Data Lab environment resources.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    environment_id:
        description:
            - The environment id for the Domino Data Lab resource.
        type: str
extends_documentation_fragment:
    - stevefulme1.domino.common
requirements:
    - "python >= 3.9"
    - "requests"
"""

EXAMPLES = r"""
- name: List all environments
  stevefulme1.domino.environment_info:
    api_url: "https://app.dominodatalab.com"
    api_key: "my-api-key"
"""

RETURN = r"""
environments:
    description: List of environment resources.
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
        environment_id=dict(type="str"),
    )
    argument_spec.update(COMMON_ARGS)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    if not HAS_REQUESTS:
        module.fail_json(msg="The 'requests' library is required. Install with: pip install requests")

    client = ApiClient(module)

    result = client.get("/api/v1/environments")
    items = result if isinstance(result, list) else result.get("data", result.get("items", []))
    module.exit_json(changed=False, environments=items)


if __name__ == "__main__":
    main()
