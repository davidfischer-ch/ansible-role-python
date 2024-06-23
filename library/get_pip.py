import os
import re

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r"""
---
module: get_pip
author: "David Fischer (@davidfischer-ch)"
short_description: Install pip using get-pip.py.
options:
  executable:
    required: true
    description:
      - The path to get-pip.py
  options:
    required: false
  python:
    required: true
    description:
      - The python to use
  umask:
    required: false
    description:
      - The umask to use
  version:
    required: false
    description:
      - Pip version to install
"""

EXAMPLES = r"""
- get_pip:
    executable: '{{ local_source_directory }}/get-pip-{{ item }}.py'
    python: python3.7
    version: 19.3.1
"""


def main():
    module = AnsibleModule(
        argument_spec=dict(
            executable=dict(required=True, type='path'),
            options=dict(required=False, type='list'),
            python=dict(required=True),
            umask=dict(default=None),
            version=dict(default=None)
        ),
        supports_check_mode=False
    )
    executable, options, python, umask, version = (
        module.params[k] for k in ('executable', 'options', 'python', 'umask', 'version')
    )
    umask = int(umask, 8) if isinstance(umask, str) else umask
    diff = install_pip(module, executable, python, umask, version, options)
    module.exit_json(changed=diff['after'] != diff['before'], diff=diff)


def install_pip(module, get_pip, python, umask, version, options=None):
    cmd = [python, get_pip] + (options or []) + ['pip' + ('==' + version if version else '')]
    rc, stdout, stderr = module.run_command(cmd, check_rc=True, umask=umask)
    after = re.search(r' installed (pip-\S+)', stdout)
    before = re.search(r' uninstalled (pip-\S+)', stdout)
    return {
        'after': (after.groups()[0] if after else '') + os.linesep, 'after_header': 'pip',
        'before': (before.groups()[0] if before else '') + os.linesep, 'before_header': 'pip',
    }


if __name__ == '__main__':
    main()
