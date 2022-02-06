# Ansible Role Python

Library of Ansible plugins and roles for deploying various services.
See [ansible-roles](https://github.com/davidfischer-ch/ansible-roles) for additional documentation.

This repository hosts the role Python and may depend of other roles and plugins of the library.

This role install Python runtimes and tools (`pip`, `setuptools` and `virtualenv`).

CPython runtimes defined in `python_versions` can be either installed by the package manager:

- Ensure the runtime(s) are listed in `python_packages`
- On RedHat, RHSM repositories will be enabled (by default)

However, if the runtime is not found, then it will be compiled and installed from source.

PyPy runtimes defined in `python_pypy_versions` will be installed from the release package.

A symbolic link to the runtime will make it available in `$PATH`.

You can reach me if you need more explanations.

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

### Global

#### do_become

Default: `yes`

Set it to `no` if you are building a container or you do not have/need `sudo` superpowers.

#### python_dynamic_defaults

Feed `dynamic_defaults` with sane defaults based on multiple criterias (Distribution, Release, etc).
This will populate variables such as  `python_*_packages`, `python_setup_mode`, `python_versions`, ...

#### python_packages

Default: Dynamically set from `python_dynamic_defaults`

#### python_rhsm_repositories

Define RHSM repositories to enable if setup mode is `rhsm`.

Default: Dynamically set from `python_dynamic_defaults`

On RedHat 7.* the variable is set to:

```
python_rhsm_repositories:
  - rhel-7-server-optional-rpms
  - rhel-server-rhscl-7-rpms
```

On other distributions, the variable is kept undefined.

#### python_setup_mode

See the introduction section for further details.

Default: Dynamically set from `python_dynamic_defaults`

Choices:
  - `rhsm` : Enable RHSM repositories (on RedHat by default) and install only from it
  - `standard` : Install from source if the interpreter is not found (see introduction section)

#### python_versions

Define the CPython interpreters to *install* / *manage*, for example: `[2.7, 3.8]`.

Default: Dynamically set from `python_dynamic_defaults`

### CPython

#### python_build_environment

Any environment variables to influence the build.

Default: `{}`

Example:

```
python_build_environment:
  LD_LIBRARY_PATH: /opt/openssl-1.1.1b/lib
```

#### python_build_flags

Any flags to influence the build.

Default: `{}`

Example:

```
python_build_flags:
  - --enable-optimizations          # https://stackoverflow.com/questions/41405728
  - --enable-option-checking=fatal  # https://www.gnu.org/software/autoconf/manual/autoconf-2.69/html_node/Option-Checking.html
  - --with-openssl=/opt/openssl-1.1.1b/lib
```

#### python_build_install_dependencies_of

This role will conveniently use the package manager to install Python build dependencies.

This is convenient for most users as this list may change over time and is probably quite long.

Set it to an empty string to skip this feature and take full control of packages using ONLY `python_build_packages`.

Default: `python` <- is the package name

Translated to `apt-get build-dep python` on APT powered distributions.

Translated to `yum-builddep --assumeyes python` on YUM powered distributions.

#### python_build_packages

Extra packages (e.g. libraries) to install when building the CPython interpreter(s) from sources.

Default: Dynamically set from `python_dynamic_defaults`

#### python_build_params

Any parameters to influence the build.

Default: `{ '--jobs': '{{ ansible_processor_cores }}' }`

#### python_default_path

#### python_default_version

Influence the task copying pip(verion) as pip, see `python_pip_path`.

Default: `'{{ python_versions|first }}'`

#### python_download_environment

Any environment variables required to download artifacts (source code, etc).

For example you can define a proxy, see `python_pip_environment`.

Default: `'{{ python_pip_environment }}'`

#### python_latest_checksums

Maps version to the checksum of the latest release available for that version.

I periodically update this list so if you want to be 100% idempotent, you have to override it.

For example, `3.8` will be mapped to `3.8.2` with a checksum of `md5:f9f3768f757e34b342dbc06b41cbc844`.

Default: A dict mapping version to MD5 checksum.

#### python_latest_versions

Maps version to the *full* version number of the latest release available for that version.

I periodically update this list so if you want to be 100% idempotent, you have to override it.

For example, `3.8` will be mapped to `3.8.2` with a checksum of `md5:f9f3768f757e34b342dbc06b41cbc844`.

Default: A dict mapping version to the full version (including minor).

#### python_paths

Let you the choice to define the paths to Python interpreters (influence interpreters discovery and pip installs).

Can be defined to force building a Python interpreter from source :)

Any version not defined here will be mapped to `python_default_path`.

Default: `{}`

Example:

```
python_paths:
  3.8: '/my/own-pythons/bin/python3.8'
```

### PyPy

#### python_pypy_release_url

Define the URL to retrieve PyPy releases.

Default: `https://bitbucket.org/pypy/pypy/downloads/{{ python_pypy_release_name }}.{{ python_pypy_release_extension }}`

#### python_pypy_release_extension

Release's extension part of `python_pypy_release_url`.

Default: Dynamically set from `python_dynamic_defaults`

#### python_pypy_release_flavor

Release's flavor part of `python_pypy_release_url`.

Default: Dynamically set from `python_dynamic_defaults`

#### python_pypy_release_name

Release's name part of `python_pypy_release_url`.

Default: `pypy{{ item }}-v{{ python_pypy_latest_versions[item|string] }}-{{ python_pypy_release_flavor }}`

#### python_pypy_versions

Define the PyPy interpreters to install from package, for example: `[3.6]`.

Default: `[]`

### PIP

#### python_get_pip_options

Any extra options to pass to `get-pip.py`.

Default: `[]`

#### python_pip_environment

Any environment variable required for PIP to be successful.

For example you can define a proxy and/or a mirror for the packages.

Default: `{}`

Example :

```
python_pip_environment:

  HTTP_PROXY: http://some-proxy.com:3128
  HTTPS_PROXY: http://some-proxy.com:3128
  NO_PROXY: localhost,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16

  http_proxy: http://some-proxy.com:3128
  https_proxy: http://some-proxy.com:3128
  no_proxy: localhost,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16

  PIP_INDEX_URL: https://some-repository.com/pip
  PIP_TRUSTED_HOST: some-repository.com
```

#### python_pip_path

Path to *default* pip binary (will be copied from pip(python_default_version)).

Default: Either `/usr/bin/pip` (if rhsm) or `/usr/local/bin/pip` (if standard).

#### python_pip_umask

Define umask when installing packages with `pip`.

See https://github.com/MindPointGroup/RHEL7-CIS/issues/61#issuecomment-396690333.

Default: `'022'`

#### python_pip_version

Which version of `pip` to install using `get-pip.py`, `''` means latest.

Default: `''`

### Tools

#### python_setuptools_version

Define the version of `setuptools` package to install using `pip`.

Set it to an empty string to skip this step.

Default: `latest`

#### python_virtualenv_version

Define the version of `virtualenv` package to install using `pip`.

Set it to an empty string to skip this step.

Default: `latest`

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

### Installing Python 3.8 from Source without sudo rights

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
    do_become: no  # Do not sudo
    prefix_directory: /opt/non-root-path
    local_source_directory: '{{ prefix_directory }}/src'

    # Disable packages management, hope required dependencies are installed
    build_packages: []
    python_build_install_dependencies_of: ''
    python_build_packages: []
    python_packages: []

    # CPython

    python_build_flags:
      - --enable-optimizations          # https://stackoverflow.com/questions/41405728
      - --enable-option-checking=fatal  # https://www.gnu.org/software/autoconf/manual/autoconf-2.69/html_node/Option-Checking.html
      - --prefix={{ prefix_directory }}

    python_setup_mode: standard
    python_versions: [3.8]
    python_paths:
      3.8: '{{ prefix_directory }}/bin/python3.8'

    # PIP

    python_get_pip_options:
      - --prefix={{ prefix_directory }}

    python_pip_path: '{{ prefix_directory }}/bin/pip'
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

2014-2022 - David Fischer
