## Configuration Management with Ansible

Ansible is a powerful configuration management tool. Configuration management is a classification of tooling used to manage system state. This includes -- but is not limited to -- files, sockets, users, groups, and software. Configuration management -- shortened to CM for the remainder of this page -- is used to track changes to system (host) state.

Ansible, Inc. is responsible for all maintainer and release duties for the Ansible project. They are a fully-owned subsidiary of Redhat, Inc. as of September 2016.

### 1.1 - Ansible Components

Ansible provides many helpful commandline utilities for performing bootstrap or day-to-day operations, documentation reference, or community interaction. Familiarize and play around with the utilities outlined in **figure 1.1a**.

Ansible has several internal components -- outlined in **figure 1.1b** -- which comprise configuration management.

A Role should describe a reusuable state. I would employ a role to: setup/manage a daemon or setup/manage a descrete configuration object (e.g. virtual site, SSL certificate).

A Play should be used to orchestrate the application of state to a system. I would employ a play to: configure an classification of host (e.g. application, database, etc.) or encapsulate a process with a given flow (e.g. to query users, allocate ACL for each user, and populate resulting token in user profile).

A Playbook is simply a collection of plays.

#### Figure 1.1a Commandline Utilities

| Utility            | Purpose                                                                                                                   |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| `ansible-doc`      | Utility to view [in a pager] module documentation (identical to docsite)                                                  |
| `ansible-galaxy`   | Utility to interact with [Ansible Galaxy](https://galaxy.ansible.com) in order to manage thrid-party roles and extensions |
| `ansible-vault`    | Utility to encrypt/decrypt, edit, and manage Ansible secrets files                                                        |
| `ansible`          | Utility to execute tasks in an ad-hoc manner against all or a subset of hosts                                             |
| `ansible-playbook` | Utility to execute playbooks against all or a subset of hosts defined in a play                                           |
| `ansible-console`  | Interactive REPL shell for running ansible tasks                                                                          |
| `ansible-pull`     | Utility to bootstrap and execute Ansible playbook from a URL or contained in SCM system                                   |

#### Figure 1.1b Internal Components

| Component      | Purpose                                                                           | Scope            |
| -------------- | --------------------------------------------------------------------------------- | ---------------- |
| Action         | A discrete unit of work to execute                                                | Task, Role, Play |
| Fact           | A quality of a host (e.g. memory, CPU configuration, network interfaces, etc.)    | Task, Role, Play |
| Variable       | A component which holds a value in memory for later use                           | Task, Role, Play |
| Task           | Wrapper for an Action which allows for looping, conditionals, etc.                | Role, Play       |
| Handler        | A callback Task to be executed upon changes to a Task                             | Role, Play       |
| Block          | Wrapper for task(s) which allows for exception handling (rescue, finally, always) | Role, Play       |
| Role           | Combination of Variable(s), Task(s), and Handler(s) which form a declared state   | Play             |
| Play           | Combination of Task(s), Role(s), Variable(s) and flow control                     |                  |
| Playbook       | A file containing Play(s)                                                         |                  |

### 1.2 - Testing Ansible (the tool)

Before we delve too deeply into usage of Ansible, we should assure ourselves that the version we choose is reliable and meets **our** standards.

Let us start by setting up an Ansible workspace. You will need `git` and `pip` installed before preceeding.

```bash
git clone git@github.com:ansible/ansible.git
cd ansible
git checkout v2.1.1.0-1
git submodule update --init -- lib/ansible/modules/core
git submodule update --init -- lib/ansible/modules/extras
pip install --user -r test/utils/tox/requirements.txt
```

Then, kick off the test suite(s).

```bash
source hacking/env-setup
py.test test/units
cd test/integration
make non_destructive
```

Familiarize yourself with the test infrastructure.

```bash
cat test/README.md
cat test/integration/README.md
```

### 1.3 - Role Testing

My approach for testing roles requires the following tools to be installed:

  - `molecule`
  - `testinfra`
  - `docker`

We start off by generating a scaffold. See **figure 1.3a** for an annotated directory tree.

```
molecule init --docker <your_new_role>
```

It will output the following. N.b. `$ANSIBLE_WORKSPACE` is a shorthand for your Ansible (CM) workspace.

```
--> Initializing role <your_new_role>...
Successfully initialized new role in $ANSIBLE_WORKSPACE/roles/<your_new_role>...
```

Then, remove unnecessary scaffold content. We will dispose of `serverspec` setup and the Galaxy metadata (fuck sharing).

```
rm -rf spec meta
```

With that out of the way, we can start work on the role itself. With `$EDITOR`, open up `README.md`. Update the introduction, requirements, and dependencies subsections.

After updating the documentation for your role, touch `tests/__init__.py` (d-under init) to make a tests package.

```
touch tests/__init__.py
```

With `$EDITOR`, open up `tests/test_default.py`. Modify the content to match the following.

```python
import unittest
import testinfra
import stat
import os

# Molecule
from molecule.command import create as molecule_create
from molecule.command import converge as molecule_converge
from molecule.command import destroy as molecule_destroy

class TestYourNewRoleDefaultCase(unittest.TestCase):
    '''
    Use molecule programmatically to create TestCase fixtures.

    Use .setUp to configure testinfra runner to target fixtures.
    '''

    @classmethod
    def setUpClass(cls):
        ''' Function that will be called before running any test in this TestCase '''
        # Change working directory so molecule can pickup `../molecule.yml`
        os.chdir()
        # Create test subjects and apply `../playbook.yml`
        molecule_create.Create(dict(), dict()).execute()
        molecule_converge.Converge(dict(), dict()).execute()

    @classmethod
    def tearDownClass(cls):
        ''' Function that will be called if .setUpClass does not raise an exception to teardown TestCase '''
        # Change working directory so molecule can pickup `../molecule.yml`
        os.chdir()
        # Destroy test subjects
        molecule_destroy.Destroy(dict(), dict()).execute()

    def setUp(self):
        ''' Function that will be called before each test '''
        self.conn = testinfra.get_backend('ansible://all', \
            ansible_inventory='%s/.molecule/ansible_inventory' % os.path.dirname(os.path.relpath(__file__))

    def test_trivial(self):
        ''' Any method prefixed by `test_` will be discovered as a test function by `py.test` '''
        # Get testinfra 'File' object in context with the backend
        File = self.conn.get_module("File")
        # Get the piece of state to test
        hosts_file = File('/etc/hosts')

        # Make assertions about the piece of state
        assert hosts_file.owner == 'root'
        assert hosts_file.group == 'root'
```

We can now run our trivial test. N.b. `-v` is a verbose flag and `-s` disables `stdout` and `stderr` capturing.

```
py.test -v -s
```

```
========================================== test session starts ==========================================
platform darwin -- Python 2.7.10, pytest-3.0.1, py-1.4.31, pluggy-0.3.1 -- /System/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python
cachedir: .cache
rootdir: $ANSIBLE_WORKSPACE/roles/proof_of_concept, inifile:
plugins: cov-2.3.1, mock-1.2, xdist-1.14, testinfra-1.4.2
collected 2 items

tests/test_default.py::TestYourNewRoleDefaultCase::test_trivial
--> Creating instances ...
--> Creating Ansible compatible image of ubuntu:latest ...
--> Creating Ansible compatible image of ubuntu:latest ...
Creating container <your_new_role>-01 with base image ubuntu:latest ...
Container created.
Creating container <your_new_role>-02 with base image ubuntu:latest ...
Container created.
--> Starting Ansible Run ...

PLAY [Test playbook for '<your_new_role>' role] *******************************

TASK [setup] *******************************************************************
ok: [<your_new_role>-01]
ok: [<your_new_role>-02]

TASK [debug] *******************************************************************
ok: [<your_new_role>-01] => {
    "msg": "Hello world!"
    }
ok: [<your_new_role>-02] => {
    "msg": "Hello world!"
    }

PLAY RECAP *********************************************************************
<your_new_role>-01                 : ok=2    changed=0    unreachable=0    failed=0
<your_new_role>-02                 : ok=2    changed=0    unreachable=0    failed=0

PASSED
tests/test_default.py::TestYourNewRoleDefaultCase::test_trivial PASSED
--> Destroying instances ...
Stopping container <your_new_role>-01 ...
Removed container <your_new_role>-01.
Stopping container <your_new_role>-02 ...
Removed container <your_new_role>-02.


======================================= 2 passed in 12.04 seconds ======================================
```

Let us consider `<your_new_role>` is intended to manage MOTD (message of the day). On debian based systems, the MOTD content is defined in `/etc/motd`. So, write a test which asserts the file exists and is globally readable. Write another test which asserts the file content is 'Welcome pleeb!'.

```python
def test_motd_file_descriptor(self):
    File = self.conn.get_module('File')
    motd_file = File('/etc/motd')

    # the file needs to exist
    assert motd_file.exists
    assert motd_file.is_file

    # the file needs to be globally-readable
    assert motd_file.mode == stat.S_IROTH

def test_motd_file_content(self):
    File = self.conn.get_module('File')
    motd_file = File('/etc/motd')

    # the file content must be 'Welcome pleeb!'
    assert motd_file.content_string == 'Welcome pleeb!'
```

The first test will always pass on a new test subject (since `/etc/motd` is a core system file). Confirm the second test fails.

Then, write the ansible tasks required.

```yaml
- name: Ensure MOTD file
  copy:
    dest: /etc/motd
    content: 'Welcome pleeb!'
    owner: root
    group: root
    mode: 0644
```

Re-run the test case and confirm the tests pass. N.b. the platform and specific versions may vary in your setup.

```
========================================== test session starts ==========================================
platform darwin -- Python 2.7.10, pytest-3.0.1, py-1.4.31, pluggy-0.3.1
rootdir: $ANSIBLE_WORKSPACE/roles/<your_new_role>, inifile:
plugins: cov-2.3.1, mock-1.2, xdist-1.14, testinfra-1.4.2
collected 2 items

tests/test_default.py ..

======================================= 2 passed in 23.63 seconds =======================================
```

Repeat the process described above until you have fully tested and declared all of the state. N.b. testinfra is **only** good at testing the post-converged state of a test subject. It cannot be used to test how, when, or why ansible is going about applying the state.

#### Figure 1.3a

```
<your_new_role>
├── README.md                    # Documentation outline for role
├── defaults
│   └── main.yml
├── handlers
│   └── main.yml
├── meta
│   └── main.yml                 # Ansible Galaxy metadata skeleton
├── molecule.yml                 # Molecule configuration file. Test subject(s), ansible setup, and molecule configuration
├── playbook.yml                 # Playbook used to apply role to test subject(s)
├── spec                         # Subdirectory to contain `serverspec` tests
│   ├── default_spec.rb          # Default `serverspec` test suite
│   └── spec_helper.rb           # `serverspec` test setup and configuration
├── tasks
│   └── main.yml
├── tests
│   ├── test_default.py          # Default `testinfra` test suite
│   └── test_default.pyc
└── vars
    └── main.yml
```

### 1.4 - Playbook Testing

My approach for testing playbooks requires the following tools to be installed:

  - `molecule`
  - `testinfra`
  - `docker`

Create a scaffold for your new playbook.

```
cat << EOF > playbooks/<your_new_playbook>
---

- name: My First TDD playbook
  hosts: <applicable_group_a>:<applicable_group_b>
  tasks:
    - debug:
EOF
```

`molecule init` is intended for role development. Therefore, it is necessary to populate the playbook test molecule configuration file by hand.

Open up `molecule.yml` in `$EDITOR` and adapt the following to your use case.

```yml
---
ansible:
  playbook: playbooks/<your_new_playbook>

docker:
  containers:
  - name: <test_subject_cluster_member_ident>-01
    ansible_groups:
    - <applicable_group_a>
    - <applicable_group_b>
    image: ubuntu
    image_version: 14.04
  - name: <test_subject_cluster_member_ident>-02
    ansible_groups:
    - <applicable_group_a>
    - <applicable_group_b>
    image: ubuntu
    image_version: 14.04
  - name: <test_subject_cluster_member_ident>-03
    ansible_groups:
    - <applicable_group_a>
    - <applicable_group_b>
    image: ubuntu
    image_version: 14.04
```

Create a subdirectory in `test/integration/playbooks` for your new playbook. Touch a `__init__.py` file to create a test module in the `tests` package.

```
mkdir test/integration/playbooks/<your_new_playbook>
touch test/integration/playbooks/<your_new_playbook>/__init__.py
```

Create a default test suite.

```
touch test/integration/playbooks/<your_new_playbook>/test_default.py
```

Open the default test suite in `$EDITOR`. Add and adapt the following.

```python
import unittest
import testinfra
import os
import stat

# Molecule
from molecule.command import create as molecule_create
from molecule.command import converge as molecule_converge
from molecule.command import destroy as molecule_destroy

def setUpModule():
    ''' Function that will be called before running any test in this test module '''
    # Change working directory so molecule can pickup `../molecule.yml`
    os.chdir()
    # Create test subjects and apply `playbooks/<your_new_playbook>`
    molecule_create.Create(dict(), dict()).execute()
    molecule_converge.Converge(dict(), dict()).execute()

def tearDownModule():
    ''' Function that will be called if .setUpModule does not raise an exception to teardown the test module '''
    # Change working directory so molecule can pickup `molecule.yml`
    os.chdir()
    # Destroy test subjects
    molecule_destroy.Destroy(dict(), dict()).execute()

class TestYourNewPlaybookApplicableGroupAHostsDefaultCase(unittest.TestCase):
    ''' TestCase to target <applicable_group_a> hosts '''

    def setUp(self):
        ''' Target testinfra tests in this suite against <applicable_group_a> '''
        self.conn = testinfra.get_backend('ansible://<applicable_group_a>', \
            ansible_inventory='%s/.molecule/ansible_inventory' % os.path.dirname(os.path.relpath(__file__))

class TestYourNewPlaybookAllHostsDefaultCase(unittest.TestCase):
    ''' TestCase to target all hosts '''

    def setUp(self):
        ''' Target testinfra tests in this suite against all '''
        self.conn = testinfra.get_backend('ansible://all', \
            ansible_inventory='%s/.molecule/ansible_inventory' % os.path.dirname(os.path.relpath(__file__))
```

### 1.5 - Playbook-Host Testing
