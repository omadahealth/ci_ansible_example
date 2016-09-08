## Introduction

### 0.1 - Documentation Introduction

This set of documentation aspires to outline the process for test-driven Ansible development. It may not be comprehensive, but it should be enough to get **you** started and contributing! It will *not* cover systems provisioning, network design, or other related topics as they are beyond scope.

We assume **you** have a fundamental understanding with python (this documentation will skip the basics and focus more on development lifecycle). We will discuss testing with `unittest`, `pytest`, `testinfra`, and `molecule`. See **figure 0.1a** for the functionality of these tools.

In addition, we will put together a continuous deployment pipeline with Jenkins 2.x.

Testing and continuously deploying your configuration management will lead to a [provably] reliable platform.

#### Figure 0.1a

| Tool Name   | Tool Function                                               | Tool Documentation                              |
| ----------- | ----------------------------------------------------------- | ----------------------------------------------- |
| `unittest`  | xUnit-based python test framework                           | https://docs.python.org/2/library/unittest.html |
| `pytest`    | Python test framework which extends fixtures                | http://doc.pytest.org/en/latest                 |
| `testinfra` | Pytest plugin for testing config management tooling         | http://testinfra.readthedocs.io/en/latest       |
| `molecule`  | System (or container) provisioning tool for Ansible testing | http://molecule.readthedocs.io/en/latest        |
