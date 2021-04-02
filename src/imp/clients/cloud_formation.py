import boto3

from decorators import handle_exception


class CloudFormation:
    def __init__(self):
        self.cf_resource = boto3.resource('cloudformation')
        self.cf_client = self.cf_resource.meta.client

    @handle_exception
    def get(self, name):
        return self.cf_client.describe_stacks(
            StackName=name
        )

    @handle_exception
    def create(self, name, template):
        return self.cf_client.create_stack(
            StackName=name,
            TemplateBody=template.to_json(),
            DisableRollback=True
        )

    @handle_exception
    def update(self, name, template):
        return self.cf_client.update_stack(
            StackName=name,
            TemplateBody=template.to_json()
        )

    @handle_exception
    def delete(self, name):
        return self.cf_client.delete_stack(
            StackName=name
        )
