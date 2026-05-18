# -*- coding: utf-8 -*-
# Copyright (c) 2025, Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module to query Domino Data Lab hardware_tier resources."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: hardware_tier_info
short_description: List or retrieve Domino hardware tiers
description:
    - Retrieve information about Domino Data Lab hardware_tier resources.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    hardware_tier_id:
        description:
            - The hardware tier id for the Domino Data Lab resource.
        type: str
extends_documentation_fragment:
    - stevefulme1.domino.common
requirements:
    - "python >= 3.9"
    - "requests"
"""

EXAMPLES = r"""
- name: List all hardware_tiers
  stevefulme1.domino.hardware_tier_info:
    api_url: "https://app.dominodatalab.com"
    api_key: "my-api-key"
"""

RETURN = r"""
hardware_tiers:
    description: List of hardware_tier resources.
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
        hardware_tier_id=dict(type="str"),
    )
    argument_spec.update(COMMON_ARGS)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    if not HAS_REQUESTS:
        module.fail_json(msg="The 'requests' library is required. Install with: pip install requests")

    client = ApiClient(module)

    result = client.get("/api/v1/hardware_tiers")
    items = result if isinstance(result, list) else result.get("data", result.get("items", []))
    module.exit_json(changed=False, hardware_tiers=items)


if __name__ == "__main__":
    main()
