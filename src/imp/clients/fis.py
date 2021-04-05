import boto3
from resource_names import *
from decorators import handle_exception


class Fis:
    def __init__(self):
        self.fis_client = boto3.client('fis')

    @handle_exception
    def list(self, name):
        experiments = self.fis_client.list_experiments()["experiments"]

        return list(e for e in experiments if e["tags"].get("Name") == name)

    @handle_exception
    def get(self, id):
        return self.fis_client.get_experiment(id=id)["experiment"]

    @handle_exception
    def start(self, template_name, name):
        templates = self.fis_client.list_experiment_templates()["experimentTemplates"]
        experiment_template = next(
            (t for t in templates if t["tags"].get("Name") == fis_template_name(template_name)),
            None
        )

        if experiment_template:
            return self.fis_client.start_experiment(
                tags={
                    "Name": name
                },
                experimentTemplateId=experiment_template["id"]
            )
        else:
            raise Exception("AWS FIS template not found.")
