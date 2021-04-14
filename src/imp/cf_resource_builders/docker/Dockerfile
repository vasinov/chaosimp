FROM public.ecr.aws/lambda/python:3.8

RUN pip install boto3

COPY app.py ${LAMBDA_TASK_ROOT}

CMD ["app.handler"]