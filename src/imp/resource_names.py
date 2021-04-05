import re
import humps


def cf_template_name(name):
    return re.sub(r'[\W_]', '', humps.pascalize(f"imp_{name}"))


def ssm_document_name(template_name, name, is_logical):
    if is_logical:
        return re.sub(r'[\W_]', '', humps.pascalize(f"ssm_doc_{template_name}_{name}"))
    else:
        return re.sub(r'[\W_]', '', humps.pascalize(f"imp_{template_name}_{name}"))


def fis_template_name(name, is_logical):
    if is_logical:
        return re.sub(r'[\W_]', '', humps.pascalize(f"fis_template_{name}"))
    else:
        return re.sub(r'[\W_]', '', humps.pascalize(f"imp_{name}"))


def fis_experiment_name(name):
    return re.sub(r'[\W_]', '', humps.pascalize(f"imp_{name}"))


def fis_action_name(name):
    return re.sub(r'[\W_]', '', humps.pascalize(f"fis_action_{name}"))


def fis_target_name(template_name, name):
    return re.sub(r'[\W_]', '', humps.pascalize(f"fis_target_{template_name}_{name}"))