import boto3


def imp_handler(event, context):
    fis_client = boto3.client('fis')

    result = fis_client.start_experiment(
        tags={
            "Name": event.template_name
        },
        experimentTemplateId=event.template_id
    )

    return {
        "result": result
    }
