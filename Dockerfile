# FROM public.ecr.aws/lambda/python:3.9

# # Install dependencies
# RUN pip install boto3

# # Copy the Lambda function code into the container
# COPY app.py .

# # Set the CMD to run the Lambda function
# CMD ["app.lambda_handler"]

FROM public.ecr.aws/lambda/python:3.7
COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY app.py ${LAMBDA_TASK_ROOT}
COPY aws.conf ${LAMBDA_TASK_ROOT}
CMD ["app.lambda_handler"]