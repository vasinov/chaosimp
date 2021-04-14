# Imp: Chaos Engineering for AWS

## Benefits over Vanilla SSM/FIS

- Experiment scripts are decoupled from the config file, which means they are much more easily editable and can be re-used in multiple experiments.
- Templates and automations are managed via Cloud Formation templates, which makes it easy to control and cleanup.
- Simplified CLI API only has three namespaces for creating templates, running experiments, and setting up automations. Much less cognitive overload.
- Imp uses a unified config file syntax. In other words, you don't have to guess which property is pascal case vs. camel case vs. something else.

## Create Custom Automation Lambda Function

```commandline
aws ecr get-login-password | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com
docker tag imp-automation:latest <REPO_URL>/imp-automation:latest
docker push <REPO_URL>/imp-automation:latest
```