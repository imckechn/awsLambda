# awsLambda

## How to run the docker image
Commands to run this bad boy

docker build -t my-lambda-image .

aws ecr create-repository --repository-name my-lambda-image --image-scanning-configuration scanOnPush=true

docker tag my-lambda-image:latest 774766912133.dkr.ecr.ca-central-1.amazonaws.com/my-lambda-image:latest

aws ecr get-login-password --region ca-central-1 | docker login --username AWS --password-stdin 774766912133.dkr.ecr.ca-central-1.amazonaws.com

docker push 774766912133.dkr.ecr.ca-central-1.amazonaws.com/my-lambda-image:latest

aws lambda create-function --function-name my-lambda-function --package-type Image --code ImageUri=774766912133.dkr.ecr.ca-central-1.amazonaws.com/my-lambda-image:latest --role arn:aws:iam::774766912133:role/service-role/nodePartA-role-le7kslnb


OR

aws ecr get-login-password --region ca-central-1 | docker login --username AWS --password-stdin 774766912133.dkr.ecr.ca-central-1.amazonaws.com

docker tag my-lambda-function:latest 774766912133.dkr.ecr.ca-central-1.amazonaws.com/my-lambda-function:latest

docker push 774766912133.dkr.ecr.ca-central-1.amazonaws.com/my-lambda-function:latest
