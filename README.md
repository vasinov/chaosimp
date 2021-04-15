# Chaos Imp

Chaos Imp is a tool for creating, executing, and continuously running [chaos engineering](https://principlesofchaos.org/) (CE) experiments on AWS.

Chaos Imp uses a plethora of AWS services and mixes them in order to create an easy-to-use tool around the following components of the CE process:

- Defining failure injections at the infrastructure, application, and security levels.
- Running CE experiments in a controlled way by using AWS access capabilities.
- Automating experiments to be run continuously.

What benefits does Chaos Imp bring to organizations when compared to SSM/FIS/Lambda?

- Experiment scripts are decoupled from the config file, which means that they are much more easily editable and can be re-used across multiple experiments.
- Templates and automations are managed via CloudFormation templates, which makes it easy to control and cleanup.
- Simplified CLI API only has three namespaces for creating `templates`, running `experiments`, and setting up `automations`. No need to worry about gluing different services together and figuring out IAM shenanigans.
- Chaos Imp uses a unified config file syntax. Think of it as [AWS SAM](https://aws.amazon.com/serverless/sam/) for chaos engineering.

## Installation

Chaos Imp is a Python package. Before installing it, create and activate a Python environment:

```bash
python3 -m venv env
. env/bin/activate
```

Then install Imp from PyPI:

```bash
pip install chaosimp
```

Now, you can use various elements from the package in your projects (namespace `chaosimp`) as well as running CLI commands with `imp`.

Check out [Chaos Imp example templates](https://github.com/chaosops/chaosimp-examples) that cover resource, network, and state chaos experiments.

## Define Experiment Boundaries

You can perform experiment on a variety of different AWS resources. Chaos Imp automatically translates resources defined in the YAML experiment template to [AWS FIS targets](https://docs.aws.amazon.com/fis/latest/userguide/targets.html).

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

This will define a FIS target that experiment actions can be applied to.

## Create Custom Automation Lambda Function

```bash
aws ecr get-login-password | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com
docker tag imp-automation:latest <REPO_URL>/imp-automation:latest
docker push <REPO_URL>/imp-automation:latest
```

## Benefits over Vanilla AWS SSM/FIS/Lambda

