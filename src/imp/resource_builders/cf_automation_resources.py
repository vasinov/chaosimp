import troposphere.iam as iam
import troposphere.awslambda as awslambda
import troposphere.events as events
from troposphere import GetAtt

from resource_names import *


def build_assume_role(name: str) -> iam.Role:
    role = iam.Role(iam_assume_role_name(name))

    role.AssumeRolePolicyDocument = {
        "Statement": {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    }

    return role


def build_lambda_function(name: str) -> awslambda.Function:
    function = awslambda.Function(lambda_function_name(name))
    function_code = awslambda.Code()

    function_code.ZipFile = "def imp_handler(event, context):\n  message = \"Hello Lambda World!\"\n  return message\n"

    function.Runtime = "python3.8"
    function.Handler = "index.imp_handler"
    function.Role = GetAtt(iam_assume_role_name(name), "Arn")
    function.Code = function_code

    return function


def build_rule(name: str, schedule: str) -> events.Rule:
    rule = events.Rule(rule_name(name))
    target = events.Target()

    target.Arn = GetAtt(lambda_function_name(name), "Arn")
    target.Id = "1"

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
