import boto3
from resource_names import *
from decorators import handle_exception


class Fis:
    def __init__(self):
        self.fis_client = boto3.client('fis')

    @handle_exception
    def list(self, experiment_name):
        experiments = self.fis_client.list_experiments()["experiments"]

        return list(e for e in experiments if e["tags"].get("Name") == fis_experiment_name(experiment_name))

    @handle_exception
    def get_by_id(self, experiment_id):
        return self.fis_client.get_experiment(id=experiment_id)["experiment"]

    @handle_exception
    def get_latest_by_name(self, experiment_name):
        experiments = self.fis_client.list_experiments()["experiments"]

        return list(e for e in experiments if e["tags"].get("Name") == fis_experiment_name(experiment_name))[0]

    @handle_exception
    def start(self, template_name, experiment_name):
        templates = self.fis_client.list_experiment_templates()["experimentTemplates"]
        experiment_template = next(
            (t for t in templates if t["tags"].get("Name") == fis_template_name(template_name, False)),
            None
        )

        if experiment_template is None:
            raise Exception("AWS FIS template not found.")
        else:
            return self.fis_client.start_experiment(
                tags={
                    "Name": fis_experiment_name(experiment_name)
                },
                experimentTemplateId=experiment_template["id"]
            )["experiment"]

    @handle_exception
    def stop(self, experiment_id):
        self.fis_client.stop_experiment(
            id=experiment_id
        )
