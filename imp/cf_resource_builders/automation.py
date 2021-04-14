import json
import troposphere.awslambda as awslambda
import troposphere.events as events
import troposphere.iam as iam
from troposphere import GetAtt
from clients.fis import Fis
from name_constants import *
from resource_names import *

LAMBDA_RUNTIME = "python3.8"
LAMBDA_TIMEOUT = 60
LAMBDA_MEMORY_SIZE = 128


def build_assume_role(name: str) -> iam.Role:
    role = iam.Role(iam_assume_role_name(name))
    policy = iam.Policy()

    policy.PolicyName = "ImpRunExperiment"
    policy.PolicyDocument = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "fis:StartExperiment",
                    "fis:TagResource"
                ],
                "Effect": "Allow",
                "Resource": [
                    "arn:aws:fis:*:*:experiment/*",
                    "arn:aws:fis:*:*:experiment-template/*",
                ],
                "Condition": {
                    "StringEquals": {
                        f"aws:ResourceTag/{TAG_KEY_TEMPLATE}": "true"
                    }
                }
            }
        ]
    }

    role.AssumeRolePolicyDocument = {
        "Version": "2012-10-17",
        "Statement": {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    }
    role.Path = "/"
    role.Policies = [policy]

    return role


def build_lambda_function(name: str, image_uri: str) -> awslambda.Function:
    function = awslambda.Function(lambda_function_name(name))
    function_code = awslambda.Code()

    function_code.ImageUri = image_uri
    function.PackageType = "Image"
    function.Timeout = LAMBDA_TIMEOUT
    function.MemorySize = LAMBDA_MEMORY_SIZE
    function.Role = GetAtt(iam_assume_role_name(name), "Arn")
    function.Code = function_code

    return function


def build_rule(name: str, schedule: str, template_name: str) -> events.Rule:
    experiment_template = Fis().get_template(template_name)

    if experiment_template is None:
        raise Exception("AWS FIS template not found.")
    else:
        rule = events.Rule(rule_name(name))
        target = events.Target()

        target.Arn = GetAtt(lambda_function_name(name), "Arn")
        target.Id = "1"
        target.Input = json.dumps(
            {
                "experiment_name": fis_automated_experiment_name(template_name),
                "template_id": experiment_template["id"]
            }
        )

        rule.ScheduleExpression = schedule
        rule.Targets = [target]

        return rule


def build_lambda_permission(name: str) -> awslambda.Permission:
    permission = awslambda.Permission(lambda_permission_name(name))

    permission.Action = "lambda:InvokeFunction"
    permission.FunctionName = GetAtt(lambda_function_name(name), "Arn")
    permission.Principal = "events.amazonaws.com"
    permission.SourceArn = GetAtt(rule_name(name), "Arn")

    return permission
