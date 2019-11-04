# Ansible Role python

Library of Ansible plugins and roles for deploying various services.
See [ansible-roles](https://github.com/davidfischer-ch/ansible-roles) for additional documentation.

This repository hosts the role python and may depend of other roles and plugins of the library.

## Remarks

### Compilation

Compiling Python from source is not fully idempotent for two reasons :

1. If `python_latest_versions` is updated, Python will not be recompiled.
2. If sudoers file doesn't export /usr/local/bin in path, Python binaries will always be recompiled.

See :
* https://github.com/davidfischer-ch/ansible-role-python/blob/master/tasks/get-versions.yml#L4
* https://github.com/davidfischer-ch/ansible-role-bootstrap/blob/master/tasks/main.yml#L48

## Dependencies

See [meta](meta/main.yml).

## Variables

TODO VARIABLES

## License

See [LICENSE.rst](LICENSE.rst).

## Authors

See [AUTHORS](AUTHORS).

2014-2019 - David Fischer
