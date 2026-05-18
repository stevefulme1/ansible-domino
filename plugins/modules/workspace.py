# -*- coding: utf-8 -*-
# Copyright (c) 2025, Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing Domino Data Lab workspace resources."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: workspace
short_description: Manage Domino workspaces
description:
    - Create, update, and delete Domino Data Lab workspace resources.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    project_id:
        description:
            - The project id for the Domino Data Lab resource.
        type: str
        required: true
    name:
        description:
            - The name for the Domino Data Lab resource.
        type: str
    hardware_tier_id:
        description:
            - The hardware tier id for the Domino Data Lab resource.
        type: str
    environment_id:
        description:
            - The environment id for the Domino Data Lab resource.
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
- name: Create a workspace
  stevefulme1.domino.workspace:
    api_url: "https://app.dominodatalab.com"
    api_key: "my-api-key"
    project_id: "example"
    state: present

- name: Delete a workspace
  stevefulme1.domino.workspace:
    api_url: "https://app.dominodatalab.com"
    api_key: "my-api-key"
    project_id: "example"
    state: absent
"""

RETURN = r"""
workspace:
    description: The workspace resource details.
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
        result = client.get("/api/v1/workspaces")
        items = result if isinstance(result, list) else result.get("data", result.get("items", []))
        for item in items:
            if item.get("project_id") == params.get("project_id"):
                return item
    except Exception:
        pass
    return None


def create_resource(client, params):
    """Create a new resource."""
    payload = {k: v for k, v in params.items() if v is not None and k not in (
        "api_url", "api_key", "validate_certs", "timeout", "state",
    )}
    return client.post("/api/v1/workspaces", data=payload)


def update_resource(client, existing, params):
    """Update an existing resource."""
    resource_id = existing.get("id", existing.get("workspace_id", ""))
    payload = {k: v for k, v in params.items() if v is not None and k not in (
        "api_url", "api_key", "validate_certs", "timeout", "state",
    )}
    return client.put(f"/api/v1/workspaces/{resource_id}", data=payload)


def delete_resource(client, existing):
    """Delete a resource."""
    resource_id = existing.get("id", existing.get("workspace_id", ""))
    client.delete(f"/api/v1/workspaces/{resource_id}")


def needs_update(params, existing):
    """Check if existing resource needs updating."""
    check_fields = ['name', 'hardware_tier_id', 'environment_id']
    for field in check_fields:
        desired = params.get(field)
        if desired is not None and existing.get(field) != desired:
            return True
    return False


def main():
    argument_spec = dict(
        project_id=dict(type="str", required=True),
        name=dict(type="str"),
        hardware_tier_id=dict(type="str"),
        environment_id=dict(type="str"),
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
        module.exit_json(changed=True, workspace=resource)
        return

    if needs_update(params, existing):
        if module.check_mode:
            module.exit_json(changed=True)
        resource = update_resource(client, existing, params)
        module.exit_json(changed=True, workspace=resource)
        return

    module.exit_json(changed=False, workspace=existing)


if __name__ == "__main__":
    main()
