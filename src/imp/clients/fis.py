import boto3

from constants import *
from resource_names import *
from decorators import handle_exception


class Fis:
    def __init__(self):
        self.fis_client = boto3.client('fis')

    @handle_exception
    def list(self, experiment_name: str) -> list:
        experiments = self.fis_client.list_experiments()["experiments"]

        if experiment_name:
            return list(
                e for e in experiments
                if e["tags"].get(TAG_KEY_EXPERIMENT) and e["tags"].get(TAG_KEY_ORIGINAL_NAME) == experiment_name
            )
        else:
            return list(
                e for e in experiments if e["tags"].get(TAG_KEY_EXPERIMENT)
            )

    @handle_exception
    def get_by_id(self, experiment_id: str):
        return self.fis_client.get_experiment(id=experiment_id)["experiment"]

    @handle_exception
    def get_latest_by_name(self, experiment_name: str):
        experiments = self.fis_client.list_experiments()["experiments"]

        return list(e for e in experiments if e["tags"].get("Name") == fis_experiment_name(experiment_name))[0]

    @handle_exception
    def start(self, template_name: str, experiment_name: str):
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
                    "Name": fis_experiment_name(experiment_name),
                    TAG_KEY_EXPERIMENT: "true",
                    TAG_KEY_ORIGINAL_NAME: experiment_name
                },
                experimentTemplateId=experiment_template["id"]
            )["experiment"]

    @handle_exception
    def stop(self, experiment_id: str):
        self.fis_client.stop_experiment(
            id=experiment_id
        )
