# Ansible Role python

Library of Ansible plugins and roles for deploying various services.
See [ansible-roles](https://github.com/davidfischer-ch/ansible-roles) for additional documentation.

This repository hosts the role python and may depend of other roles and plugins of the library.

This role install Python runtimes and tools (`pip`, `setuptools` and `virtualenv`).

CPython runtimes defined in `python_versions` can be either installed by the package manager:

- Ensure the runtime(s) are listed in `python_packages`
- On RedHat, RHSM repositories will be enabled (by default)

However, if the runtime is not found, then it will be compiled and installed from source.

PyPy runtimes defined in `python_pypy_versions` will be installed from the release package.

A symbolic link to the runtime will make it available in `$PATH`.

You can reach me if you need more explanations.
I really have to update this README.

## Remarks

### Tools

- You can disable installing `setuptools` by setting `python_setuptools_version` to `''`
- You can disable installing `virtualenv` by setting `python_virtualenv_version` to `''`

### Compilation

Compiling Python from source is not fully idempotent for two reasons :

1. If `python_latest_versions` is updated, Python will not be recompiled.
2. If sudoers file doesn't export `/usr/local/bin` in PATH, Python binaries will always be recompiled.

See :
* https://github.com/davidfischer-ch/ansible-role-python/blob/master/tasks/get-versions.yml#L4
* https://github.com/davidfischer-ch/ansible-role-bootstrap/blob/master/tasks/main.yml#L48

## Dependencies

See [meta](meta/main.yml).

## Variables

TODO VARIABLES

## Examples

### Installing Python(s) from Source

Example for compiling ONLY Python 3.8 from latest current release (e.g. 3.8.2).

Note: Override `python_latest_checksums` and `python_latest_versions` to enforce a specific the version.

### Playbook

```
---

- hosts:
    - localhost
  roles:
    - python
  vars:
    python_packages: []
    python_setup_mode: standard
    python_versions: [3.8]

    python_build_flags:
      - --enable-optimizations
      - --enable-option-checking=fatal

    python_setuptools_version: latest
    python_virtualenv_version: ''  # We do not want it
```

### Installing PyPy 3.6

Example for installing ONLY PyPy 3.6 from latest current (available as pypy3.6 thanks to a symbolic link).

Note: Override `python_pypy_latest_checksums` and `python_pypy_latest_versions` to enforce a specific the version.

### Playbook

```
---

- hosts:
    - localhost
  roles:
    - python
  vars:
    build_packages: []
    python_packages: []
    python_versions: []
    python_pypy_versions: [3.6]
```

### Installing Python(s) from Source (Static)

**WARNING** This example is not yet working, compiling CPython statically with all modules available statically is hard and needs a lot of tweaking (I have at least 20 tabs open to find how to), feel free to contribute :)

Example for compiling ONLY Python 3.8 from latest current release (e.g. 3.8.2).

Note: Override `python_latest_checksums` and `python_latest_versions` to enforce a specific the version.

See: https://wiki.python.org/moin/BuildStatically
See: https://github.com/docker-library/python/blob/master/3.8/buster/slim/Dockerfile

### Playbook

```
---

- hosts:
    - localhost
  roles:
    - python
  vars:
    python_packages: []
    python_setup_mode: standard
    python_versions: [3.8]

    python_build_flags:
      - --disable-shared
      - --enable-optimizations
      - --enable-option-checking=fatal
      - LDFLAGS="-static"

    python_build_params:
      LDFLAGS: "-static"
      LINKFORSHARED: " "
```

## License

See [LICENSE.rst](LICENSE.rst).

## Authors

See [AUTHORS](AUTHORS).

2014-2019 - David Fischer
