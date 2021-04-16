# Chaos Imp

[![PyPI Version](https://img.shields.io/pypi/v/chaosimp.svg)](https://pypi.python.org/pypi/chaosimp)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/gitbucket/gitbucket/blob/master/LICENSE)

Chaos Imp is a framework for creating, executing, and running [chaos engineering](https://principlesofchaos.org/) (CE) experiments on AWS. It provides shorthand syntax to express experiment templates, executions, and automations. With just a few lines, you can define the experiment you want and model it using YAML and shell scripts. During deployment, Chaos Imp transforms and expands your YAML and shell scripts into AWS CloudFormation syntax, enabling you to run chaos experiments faster.

Chaos Imp uses a plethora of AWS services under the hood. It glues SSM, FIS, Events, and Lambda APIs to create an easy-to-use tool around the following components of the CE process:

- Defining infrastructure, application, and security failure injection templates.
- Running CE experiments in a controlled way by using AWS access capabilities.
- Automating experiments to be run continuously.

What benefits does Chaos Imp bring to organizations when compared to SSM/FIS/Lambda?

- Experiment scripts are decoupled from YAML, which means that they are much more easily editable and can be re-used across multiple experiments.
- Templates and automations are automatically managed via CloudFormation templates, which makes it easy to control and cleanup.
- CLI API is very minimalist. It has three namespaces for creating `templates`, running `experiments`, and setting up `automations`. No need to worry about gluing different services together and resolving IAM shenanigans.
- Chaos Imp uses unified config file syntax. Think of it as [AWS SAM](https://aws.amazon.com/serverless/sam/) for chaos engineering.

## Installation

Chaos Imp is a Python package. To install it run:

```bash
pip install chaosimp
```

Now, you can start using scripts and classes from the `chaosimp` package. You can also run CLI commands. Chaos Imp supports four namespaces:

- config
- templates
- experiments
- automations

`config` is used for Chaos Imp-specific configuration. It supports `get`, `list`, and `set` operations. All other namespaces support the following operations:

- list
- show
- create
- update
- delete

For example, to list all of your templates simply run:

```shell
imp templates list
```

The CLI is self-documenting, so you can learn about any command by running:

```shell
imp <COMMAND_NAME> --help
```

## Creating Templates

Check out [Chaos Imp example templates](https://github.com/chaosops-oss/chaosimp-examples) that include resource, network, and state chaos experiments.

Let's create a simple experiment that stresses CPUs of several EC2 instances.

### Experiment Boundaries

You can perform experiments on a variety of different AWS resources. Chaos Imp automatically translates resources defined in the YAML experiment template to [AWS FIS targets](https://docs.aws.amazon.com/fis/latest/userguide/targets.html).

For example, to target a subset EC2 instances tagged with `imp: ec2-experiment` define the following target in `imp.yml:

```yaml
Targets:
  - Name: "ec2-instances"
    ResourceType: "aws:ec2:instance"
    ResourceTags:
      - Key: "imp"
        Value: "ec2-experiment"
    SelectionMode: "ALL"
```

This defines a FIS target that experiment actions can be applied to.

### Actions

Now, let's define an action

## Create Custom Automation Lambda Function

```bash
aws ecr get-login-password | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com
docker tag imp-automation:latest <REPO_URL>/imp-automation:latest
docker push <REPO_URL>/imp-automation:latest
```
