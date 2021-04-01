import os
import click
from action_parsers.parser import *


class ImpRunScriptParser(Parser):
    def __init__(self, name, shell_script_path):
        self.name = name
        self.shell_script_path = shell_script_path

    def to_ssm_document(self, experiment_path):
        file_path = os.path.join(experiment_path, self.shell_script_path)

        with open(click.format_filename(file_path), 'r') as stream:
            text = stream.read()
            return {
                "description": "This document was generated by Imp CLI.",
                "schemaVersion": "2.2",
                "mainSteps": [
                    {
                        "action": "aws:runShellScript",
                        "precondition": {
                            "StringEquals": ["platformType", "Linux"]
                        },
                        "name": "ImpRunShellScript",
                        "description": "Automatically generated action",
                        "inputs": {
                            "runCommand": [
                                text
                            ]
                        }
                    }
                ]
            }
