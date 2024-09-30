# AWS Bedrock Hosted using App Runner


This project demonstrates how to deploy an AI-powered application using AWS App Runner and Amazon Bedrock.

## Architecture Overview

![steamlitapp](https://github.com/rahulsing/aws-apprunner-bedrock/blob/main/AppRunnerCapture.PNG?raw=true)

This application uses the following AWS services and components:

1. **AWS App Runner**: A fully managed service that makes it easy to deploy containerized web applications and APIs.
2. **Amazon ECR (Elastic Container Registry)**: Stores and manages our Docker images.
3. **Amazon Bedrock**: Provides access to foundation models for AI capabilities.
4. **AWS IAM**: Manages permissions and access to AWS services.

The architecture flow is as follows:

1. The application is containerized and the image is stored in Amazon ECR.
2. AWS App Runner pulls the container image from ECR and deploys it.
3. The deployed application uses the AWS SDK to interact with Amazon Bedrock.
4. When a user interacts with the application, it invokes Bedrock models to generate AI responses.

## Prerequisites

Before setting up this project, ensure you have the following:

1. An AWS account with appropriate permissions to create and manage the required services.
2. AWS CLI installed and configured with your credentials.
3. Docker installed on your local machine.
4. Access to Amazon Bedrock (may require special access in some regions).
5. Git installed (for cloning the repository).


## Demo

1. **Clone the Repository**


```
git clone https://github.com/rahulsing/aws-apprunner-bedrock.git
```

2. **Build the Docker Image**

```
REPOSITORY_NAME=bedrock-app-runner


docker build -t $REPOSITORY_NAME .
```

Option: To host locally and validate: 
```
docker run -p 8080:8080 bedrock-app-runner
```

3. **Create an ECR Repository**

Set the variables: 
```
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=us-west-2
```

4. **Push the Image to ECR**

```
aws ecr create-repository --repository-name $REPOSITORY_NAME --region us-west-2

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com

docker tag bedrock-app-runner:latest $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/$REPOSITORY_NAME:latest

docker push $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/$REPOSITORY_NAME:latest
```

5. **Deploy Using CloudFormation**

```
ECR_IMAGE=$ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/$REPOSITORY_NAME:latest

CF_STATCK_NAME=bedrock-app-runner-stack

aws cloudformation create-stack --stack-name  $CF_STATCK_NAME --template-body file://apprunner-service.yaml  --parameters ParameterKey=ECRImageUri,ParameterValue=$ECR_IMAGE --region $AWS_REGION --capabilities CAPABILITY_IAM
```

6. **Monitor Stack Creation**
Check status and wait until status show CREATE_COMPLETE (ResourceStatus)
```
aws cloudformation describe-stack-events --stack-name $CF_STATCK_NAME --query "StackEvents[0]" --output table --region $AWS_REGION
```


7. **Access Your Application**
Once the CloudFormation stack is created, you can find the URL of your deployed application in the App Runner console or CloudFormation outputs.

## Updating the Application

To update your application after making changes:

1. Rebuild the Docker image
2. Push the new image to ECR
3. Update the CloudFormation stack:
```
aws cloudformation update-stack --stack-name  $CF_STATCK_NAME --template-body file://apprunner-service.yaml  --parameters ParameterKey=ECRImageUri,ParameterValue=$ECR_IMAGE --region $AWS_REGION --capabilities CAPABILITY_IAM
```

## Cleanup 
aws cloudformation delete-stack --stack-name  $CF_STATCK_NAME --region $AWS_REGION


Note: This will delete the App Runner service and associated resources. The ECR repository and its images will remain and need to be deleted separately if desired.
