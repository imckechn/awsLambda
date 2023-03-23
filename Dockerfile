FROM public.ecr.aws/lambda/python:3.9

# Install dependencies
RUN pip install boto3

# Copy the Lambda function code into the container
COPY app.py .

# Set the CMD to run the Lambda function
CMD ["app.lambda_handler"]