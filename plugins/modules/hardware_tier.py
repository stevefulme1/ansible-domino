# -*- coding: utf-8 -*-
# Copyright (c) 2025, Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing Domino Data Lab hardware_tier resources."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: hardware_tier
short_description: Manage Domino hardware tiers
description:
    - Create, update, and delete Domino Data Lab hardware_tier resources.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    name:
        description:
            - The name for the Domino Data Lab resource.
        type: str
        required: true
    cores:
        description:
            - The cores for the Domino Data Lab resource.
        type: str
    memory_gb:
        description:
            - The memory gb for the Domino Data Lab resource.
        type: str
    gpu_count:
        description:
            - The gpu count for the Domino Data Lab resource.
        type: str
    state:
        description:
            - The desired state of the resource.
        type: str
        choices:
            - present
            - absent
        default: present
extends_documentation_fragment:
    - stevefulme1.domino.common
requirements:
    - "python >= 3.9"
    - "requests"
"""

EXAMPLES = r"""
- name: Create a hardware_tier
  stevefulme1.domino.hardware_tier:
    api_url: "https://app.dominodatalab.com"
    api_key: "my-api-key"
    name: "example"
    state: present

- name: Delete a hardware_tier
  stevefulme1.domino.hardware_tier:
    api_url: "https://app.dominodatalab.com"
    api_key: "my-api-key"
    name: "example"
    state: absent
"""

RETURN = r"""
hardware_tier:
    description: The hardware_tier resource details.
    returned: On success when state is present.
    type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.domino.plugins.module_utils.api_client import (
    COMMON_ARGS,
    ApiClient,
    HAS_REQUESTS,
)


def find_resource(client, params):
    """Find existing resource by identifier."""
    try:
        result = client.get("/api/v1/hardware_tiers")
        items = result if isinstance(result, list) else result.get("data", result.get("items", []))
        for item in items:
            if item.get("name") == params.get("name"):
                return item
    except Exception:
        pass
    return None


def create_resource(client, params):
    """Create a new resource."""
    payload = {k: v for k, v in params.items() if v is not None and k not in (
        "api_url", "api_key", "validate_certs", "timeout", "state",
    )}
    return client.post("/api/v1/hardware_tiers", data=payload)


def update_resource(client, existing, params):
    """Update an existing resource."""
    resource_id = existing.get("id", existing.get("hardware_tier_id", ""))
    payload = {k: v for k, v in params.items() if v is not None and k not in (
        "api_url", "api_key", "validate_certs", "timeout", "state",
    )}
    return client.put(f"/api/v1/hardware_tiers/{resource_id}", data=payload)


def delete_resource(client, existing):
    """Delete a resource."""
    resource_id = existing.get("id", existing.get("hardware_tier_id", ""))
    client.delete(f"/api/v1/hardware_tiers/{resource_id}")


def needs_update(params, existing):
    """Check if existing resource needs updating."""
    check_fields = ['cores', 'memory_gb', 'gpu_count']
    for field in check_fields:
        desired = params.get(field)
        if desired is not None and existing.get(field) != desired:
            return True
    return False


def main():
    argument_spec = dict(
        name=dict(type="str", required=True),
        cores=dict(type="str"),
        memory_gb=dict(type="str"),
        gpu_count=dict(type="str"),
        state=dict(type="str", choices=["present", "absent"], default="present"),
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
    state = params["state"]

    existing = find_resource(client, params)

    if state == "absent":
        if existing is None:
            module.exit_json(changed=False)
        if module.check_mode:
            module.exit_json(changed=True)
        delete_resource(client, existing)
        module.exit_json(changed=True)
        return

    if existing is None:
        if module.check_mode:
            module.exit_json(changed=True)
        resource = create_resource(client, params)
        module.exit_json(changed=True, hardware_tier=resource)
        return

    if needs_update(params, existing):
        if module.check_mode:
            module.exit_json(changed=True)
        resource = update_resource(client, existing, params)
        module.exit_json(changed=True, hardware_tier=resource)
        return

    module.exit_json(changed=False, hardware_tier=existing)


if __name__ == "__main__":
    main()
