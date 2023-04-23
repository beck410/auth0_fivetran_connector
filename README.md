# Auth0 user data connector

## Fivetran Custom Connectors
Fivetran allows for building and scheduling custom function connectors using serverless compute services such as AWS Lambda if they don't have a connector for a specific integration in their library.

## Updating code in AWS Lambda Function
The Lambda function console allows you to update code in their editor and test changes easily. If you update code within the lambda function console please also update the corresponding connector code within this repo for transparency and reference.

# Deploying new runtime dependencies/libraries to AWS Lambda function (python env)
1. In connector folder (e.g. auth0_lambda_connector) create and source virtualenv
2. Run pip install requirements.txt --target - you should see all libraries in your folder
3. Run zip -r file_name.zip mydir/* from outside directory
You can either upload zip file to lambda function through AWS CLI or within the Lambda function console
