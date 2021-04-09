import boto3
from troposphere import Template

from constants import *
from decorators import handle_exception


class CloudFormation:
    def __init__(self):
        self.cf_resource = boto3.resource('cloudformation')
        self.cf_client = self.cf_resource.meta.client

    @handle_exception
    def list(self, resource_type: str) -> list:
        return [
            s for s in self.cf_client.describe_stacks()["Stacks"]
            if any(t["Key"] == TAG_KEY_RESOURCE_TYPE and t["Value"] == resource_type for t in s["Tags"])
        ]

    @handle_exception
    def get(self, name):
        return self.cf_client.describe_stacks(
            StackName=name
        )["Stacks"][0]

    @handle_exception
    def create(self, name: str, original_name: str, template: Template, resource_type: str):
        return self.cf_client.create_stack(
            StackName=name,
            TemplateBody=template.to_json(),
            DisableRollback=True,
            Tags=[
                {
                    "Key": TAG_KEY_RESOURCE_TYPE,
                    "Value": resource_type
                },
                {
                    "Key": TAG_KEY_ORIGINAL_NAME,
                    "Value": original_name
                }
            ]
        )

    @handle_exception
    def update(self, name: str, original_name: str, template: Template, resource_type: str):
        return self.cf_client.update_stack(
            StackName=name,
            TemplateBody=template.to_json()
        )

    @handle_exception
    def delete(self, name: str):
        return self.cf_client.delete_stack(
            StackName=name
        )
