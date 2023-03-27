# AWS Lambda Docker Image

By Ian McKechnie


A program that watches for S3 files being added, get's a subscription list from a bucket, and copies to the new S3 object to all the buckets in that list. It also creates a log folder with what it has done.


## Put the Docker image on Lamda

docker build -t my-lambda-image .

docker buildx build --platform linux/amd64,linux/arm64 --push -t my-lambda-image:latest .

aws ecr create-repository --repository-name my-lambda-image --image-scanning-configuration scanOnPush=true

docker tag my-lambda-image:latest 774766912133.dkr.ecr.ca-central-1.amazonaws.com/my-lambda-image:latest

aws ecr get-login-password --region ca-central-1 | docker login --username AWS --password-stdin 774766912133.dkr.ecr.ca-central-1.amazonaws.com

docker push 774766912133.dkr.ecr.ca-central-1.amazonaws.com/my-lambda-image:latest

aws lambda create-function --function-name my-lambda-function --package-type Image --code ImageUri=774766912133.dkr.ecr.ca-central-1.amazonaws.com/my-lambda-image:latest --role arn:aws:iam::774766912133:role/service-role/nodePartA-role-le7kslnb