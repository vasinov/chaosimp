import troposphere.iam as iam
import troposphere.awslambda as awslambda
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


def build_lambda(name: str) -> awslambda.Function:
    function = awslambda.Function(lambda_function_name(name))
    function_code = awslambda.Code()

    function_code.ZipFile = "def imp_handler(event, context):\n  message = \"Hello Lambda World!\"\n  return message\n"

    function.Runtime = "python3.8"
    function.Handler = "index.imp_handler"
    function.Role = GetAtt(iam_assume_role_name(name), "Arn")
    function.Code = function_code

    return function
