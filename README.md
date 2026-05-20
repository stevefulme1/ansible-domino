> **EXPERIMENTAL** - This collection is a proof of concept and is not production ready.
> Modules may use placeholder API endpoints and have not been validated against real infrastructure.
> Do not use in production environments.

        # stevefulme1.domino

        Ansible Collection for **Domino Data Lab**.

        ## Modules

        - `stevefulme1.domino.project` -- Manage Domino projects
- `stevefulme1.domino.project_info` -- List or retrieve Domino projects
- `stevefulme1.domino.environment` -- Manage Domino compute environments
- `stevefulme1.domino.environment_info` -- List or retrieve Domino environments
- `stevefulme1.domino.model` -- Manage Domino model registrations
- `stevefulme1.domino.model_info` -- List or retrieve Domino models
- `stevefulme1.domino.endpoint` -- Manage Domino model API endpoints
- `stevefulme1.domino.endpoint_info` -- List or retrieve Domino model endpoints
- `stevefulme1.domino.hardware_tier` -- Manage Domino hardware tiers
- `stevefulme1.domino.hardware_tier_info` -- List or retrieve Domino hardware tiers
- `stevefulme1.domino.dataset` -- Manage Domino datasets
- `stevefulme1.domino.dataset_info` -- List or retrieve Domino datasets
- `stevefulme1.domino.job` -- Manage Domino jobs
- `stevefulme1.domino.job_info` -- List or retrieve Domino jobs
- `stevefulme1.domino.workspace` -- Manage Domino workspaces
- `stevefulme1.domino.workspace_info` -- List or retrieve Domino workspaces

        ## Roles

        - `domino_install` -- Install and configure Domino Data Lab
- `model_deploy` -- Deploy models to Domino endpoints
- `workspace_provision` -- Provision Domino workspaces

        ## EDA Event Source

        - `stevefulme1.domino.domino_events` -- Poll Domino Data Lab for events

        ## Requirements

        - Python >= 3.9
        - `requests` library
        - ansible-core >= 2.16

        ## Installation

        ```bash
        ansible-galaxy collection install stevefulme1.domino
        ```

        ## License

        GPL-3.0-or-later
