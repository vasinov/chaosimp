# Chaos Imp

Chaos Imp is a tool for engineers and DevOps to create, execute, and continuously run chaos engineering (CE) experiments on AWS.

Chaos Imp uses a plethora of AWS services and mixes them to create a painless operational experience. With Chaos Imp, an engineer can setup an experiment in a single YAML file with arbitrary shell scripts.

## Install

Chaos Imp is a Python package and a CLI. First, create and activate a Python environment:

```commandline
python3 -m venv env
. env/bin/activate
```

Then install Imp from PyPI:

```commandline
pip install chaosimp
```

Now, you can use various elements from the package in your projects (namespace `chaosimp`) as well as running CLI commands.

## Getting Started

Checkout

## Create Custom Automation Lambda Function

```commandline
aws ecr get-login-password | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com
docker tag imp-automation:latest <REPO_URL>/imp-automation:latest
docker push <REPO_URL>/imp-automation:latest
```

## Benefits over Vanilla AWS SSM/FIS/Lambda

- Experiment scripts are decoupled from the config file, which means they are much more easily editable and can be re-used in multiple experiments.
- Templates and automations are managed via Cloud Formation templates, which makes it easy to control and cleanup.
- Simplified CLI API only has three namespaces for creating templates, running experiments, and setting up automations. Much less cognitive overload.
- Imp uses a unified config file syntax. In other words, you don't have to guess which property is pascal case vs. camel case vs. something else.