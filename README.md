# Chaos Imp

[![PyPI Version](https://img.shields.io/pypi/v/chaosimp.svg)](https://pypi.python.org/pypi/chaosimp)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/gitbucket/gitbucket/blob/master/LICENSE)

Chaos Imp is a framework for creating, executing, and running [chaos engineering](https://principlesofchaos.org/) (CE) experiments on AWS. It provides shorthand syntax to express experiment templates, executions, and automations. With just a few lines, you can define the experiment you want and model it using YAML and shell scripts. During deployment, Chaos Imp transforms and expands your YAML and shell scripts into AWS CloudFormation syntax, enabling you to run chaos experiments faster.

Chaos Imp uses a plethora of AWS services under the hood. It glues Systems Manager Agent (SSM), Failure Injection Simulator (FIS), CloudWatch Events, and Lambda Function APIs to create an easy-to-use tool around the following parts of the CE process:

- Defining infrastructure, application, and security failure injection templates.
- Running CE experiments in a controlled way by using AWS tagging capabilities.
- Automating experiments as part of the continuous verification pipeline.

## Useful Links

- [Chaos Imp Example Templates](https://github.com/chaosops-oss/chaosimp-examples)
- [Chaos Imp IAM Policies](https://github.com/chaosops-oss/chaosimp-iam-policies)

## Installation

Chaos Imp is a Python package. To install it run:

```bash
pip install chaosimp
```

Now, you can start using scripts and classes from the `chaosimp` package. You can also run CLI commands. Chaos Imp supports four namespaces:

- `config`: `get`, `list`, and `set` operations.
- `templates`: `list`, `show`, `create`, `update`, and `delete` operations.
- `experiments`: `get`, `get-by-id`, `list`, `start`, and `stop` operations.
- `automations`: `list`, `show`, `create`, `update`, and `delete` operations.

For example, to list all of your templates run:

```bash
imp templates list
```

The CLI is self-documenting, so you can learn about any command by running:

```bash
imp <COMMAND_NAME> --help
```

## Getting Started

Check out [Chaos Imp example templates](https://github.com/chaosops-oss/chaosimp-examples) that include resource, network, and state chaos experiments.

Let's create a simple experiment that stresses CPUs of several EC2 instances.

### Experiment Boundaries

You can perform experiments on a variety of different AWS resources. Chaos Imp automatically translates resources defined in the YAML experiment template to [AWS FIS targets](https://docs.aws.amazon.com/fis/latest/userguide/targets.html).

For example, to target a subset of EC2 instances tagged with `imp: ec2-experiment` define the following target in `imp.yml`:

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

Now, let's define a custom Chaos Imp action that runs a script with `stress-ng` stressing CPUs:

```yaml
Actions:
  - Name: "stress-cpus"
    Type: "imp:run-script"
    Target: "ec2-instances"
    Parameters:
      Duration: "PT1M"
    Document:
      Path: "stress-cpu.sh"
```

This defines a Chaos Imp action that is later translated into a FIS action. To avoid confusion, you can use all FIS action types defined in the [official documentation](https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html).

Chaos Imp introduces its own namespace and action type into the mix: `imp:run-script`. This action functions just like `aws:ssm:send-command` except for you can reference a local file instead of `documentArn` and `documentVersion`.

Now, we just add an experiment script file `stress-cpu.sh`:

```bash
#!/bin/bash

sudo yum -y install stress-ng
stress-ng --cpu 0 --cpu-method matrixprod --cpu-load 100 -t 20s
```

This will install `stress-ng` and apply 100% load on all CPUs for 20 seconds.

Running scripts like that on your EC2 instances requires SSM Agent to be installed. It's installed by default on Amazon Linux 2 and Ubuntu machines. If you are using a different Linux distribution then follow the [official installation guide](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-install-ssm-agent.html).

### Creating a Template

Before creating a template, you have to create a role with a [policy](https://github.com/chaosops-oss/chaosimp-iam-policies/blob/master/ImpFis.json) that allows FIS to run actions.

You can reference this role with every template creation call by using `--role-arn` but it's much more convenient to store it in the local config:

```bash
imp config set TemplateRoleArn <ROLE_ARN>
```

We are finally ready to create our first template:

```bash
imp templates create --path . cpu-stress
```

### Running Experiments

Before running an experiment on EC2 instances those instances have to be assigned a role with [a policy](https://github.com/chaosops-oss/chaosimp-iam-policies/blob/master/ImpSsm.json) that allows them to interact with SSM. This is required for all FIS SSM actions as well as Chaos Imp special actions.

Once instances are ready, you can run an experiment based on the template we created:

```bash
imp experiments start --template cpu-stress my-cpu-experiment
```

This will create and run an experiment in FIS. If you run subsequent experiments with the same name you can list all experiment executions by running:

```bash
imp experiments get my-cpu-experiment
```

If you are interested in the specific instance of an experiment then run:

```shell
imp experiments get-by-id <EXPERIMENT_ID>
```

### Automating Experiments

Experiment automation is a work in progress. Chaos Imp uses a combination of CloudWatch Events and Lambda Functions to create automations.

Unfortunately, AWS SDK is out of date in the Lambda runtime and doesn't support FIS yet, so you'll have to create a Docker image with an updated AWS SDK in it.

First, [download](https://github.com/chaosops-oss/chaosimp/tree/master/lambda_image) `Dockerfile` and `app.py` on your machine. Then run the following commands to create and push an image to your private AWS ECR:

```bash
aws ecr get-login-password | docker login \
    --username AWS \
    --password-stdin \
    <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com

docker build -t imp-automation .
docker tag imp-automation:latest <REPO_URL>/imp-automation:latest
docker push <REPO_URL>/imp-automation:latest
```

This will become unnecessary once Lambda supports a more recent SDK.

To create an automation run:

```shell
imp automations create \
    --schedule="rate(30 minutes)" \
    --template="cpu-stress" \
    --image=<AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/imp-automation:latest \
    cpu-stress-automation
```

This will create a CloudWatch Event Rule that will kickoff a Lambda every 30 minutes. The Lambda starts a FIS experiment.