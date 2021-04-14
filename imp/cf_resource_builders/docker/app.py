import boto3


def handler(event, context):
    fis_client = boto3.client('fis')

    fis_client.start_experiment(
        tags={
            "Name": event["experiment_name"],
            "CreatedByImp": "true"
        },
        experimentTemplateId=event["template_id"]
    )

    return {
        "result": "complete"
    }
