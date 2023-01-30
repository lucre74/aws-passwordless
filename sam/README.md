# aws-passwordless serverless application

This project contains source code and supporting files for the serverless 
application that is the backend of the passwordless authentication. 

## Content
- template.yaml - A template that defines the application's AWS resources.
- src - Code for the application's Lambda function.

## Deploy the application
To build and deploy the application, run the following in your shell:

```bash
sam build
sam package --output-template-file packaged.yaml --s3-bucket s3_bucket_name_ofyourchoice
sam deploy --template-file packaged.yaml --stack-name cloudformation_stack_name_ofyourchoice --capabilities CAPABILITY_IAM
```

## Tests
Manual tests of the application, using the react/test-app: 

User not existing in the user pool
- set email address
- set an invalid code
- submit
  —> should fail
- set the valid code (received at the email address)
- submit
  —> user should be authenticated


User not existing in the user pool
- set email address
- recopy the code
- submit
  —> user should be authenticated

User existing in the user pool
- set email address
- recopy the code
- submit
  —> user should be authenticated
