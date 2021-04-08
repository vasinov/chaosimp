import boto3
from troposphere import Template

from constants import *
from decorators import handle_exception


class CloudFormation:
    def __init__(self):
        self.cf_resource = boto3.resource('cloudformation')
        self.cf_client = self.cf_resource.meta.client

    @handle_exception
    def list(self) -> list:

        return [
            s for s in self.cf_client.describe_stacks()["Stacks"]
            if any(t["Key"] == IMP_TAG_KEY for t in s["Tags"])
        ]

    @handle_exception
    def get(self, name):
        return self.cf_client.describe_stacks(
            StackName=name
        )["Stacks"][0]

    @handle_exception
    def create(self, name: str, original_name: str, template: Template):
        return self.cf_client.create_stack(
            StackName=name,
            TemplateBody=template.to_json(),
            DisableRollback=True,
            Tags=[
                {
                    "Key": IMP_TAG_KEY,
                    "Value": "true"
                },
                {
                    "Key": IMP_ORIGINAL_NAME_KEY,
                    "Value": original_name
                }
            ]
        )

    @handle_exception
    def update(self, name: str, _, template: Template):
        return self.cf_client.update_stack(
            StackName=name,
            TemplateBody=template.to_json()
        )

    @handle_exception
    def delete(self, name: str):
        return self.cf_client.delete_stack(
            StackName=name
        )
