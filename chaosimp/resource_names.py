import re
import humps


def cf_template_name(name: str) -> str:
    return re.sub(r'[\W_]', '', humps.pascalize(f"imp_template_{name}"))


def cf_automation_name(name: str) -> str:
    return re.sub(r'[\W_]', '', humps.pascalize(f"imp_automation_{name}"))


def lambda_function_name(name: str) -> str:
    return re.sub(r'[\W_]', '', humps.pascalize(f"lambda_function_{name}"))


def lambda_permission_name(name: str) -> str:
    return re.sub(r'[\W_]', '', humps.pascalize(f"lambda_permission_{name}"))


def rule_name(name: str) -> str:
    return re.sub(r'[\W_]', '', humps.pascalize(f"rule_{name}"))


def iam_assume_role_name(name: str) -> str:
    return re.sub(r'[\W_]', '', humps.pascalize(f"assume_role_{name}"))


def ssm_document_name(template_name: str, name: str, is_logical: bool) -> str:
    if is_logical:
        return re.sub(r'[\W_]', '', humps.pascalize(f"ssm_doc_{template_name}_{name}"))
    else:
        return re.sub(r'[\W_]', '', humps.pascalize(f"imp_{template_name}_{name}"))


def fis_template_name(name: str, is_logical: bool) -> str:
    if is_logical:
        return re.sub(r'[\W_]', '', humps.pascalize(f"fis_template_{name}"))
    else:
        return re.sub(r'[\W_]', '', humps.pascalize(f"imp_{name}"))


def fis_experiment_name(name: str) -> str:
    return re.sub(r'[\W_]', '', humps.pascalize(f"imp_{name}"))


def fis_automated_experiment_name(name: str) -> str:
    return re.sub(r'[\W_]', '', humps.pascalize(f"imp_automation_{name}"))


def fis_action_name(name: str) -> str:
    return re.sub(r'[\W_]', '', humps.pascalize(f"fis_action_{name}"))


def fis_target_name(template_name: str, name: str) -> str:
    return re.sub(r'[\W_]', '', humps.pascalize(f"fis_target_{template_name}_{name}"))