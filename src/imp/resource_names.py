import humps


def ssm_document_name(name):
    return humps.pascalize(f"imp-ssm-doc-{name}")


def fis_template_name(name):
    return humps.pascalize(f"imp-fis-template-{name}")


def fis_target_name(name):
    return humps.pascalize(f"imp-fis-target-{name}")


def fis_experiment_name(name):
    return humps.pascalize(f"imp-{name}")
