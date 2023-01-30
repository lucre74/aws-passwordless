# Test application for the aws-passwordless project

The test application initiates a passwordless authentication 
 - specify a valid email address
 - copy the challenge received at the provided email address
 - you are authenticated (as the provided email address)

It uses the resources created in the sibling SAM application.

## Configuration
The AWS region, the Cognito user pool id and the Cognito Web 
client id must be available in the environment. Either as variables
from your environment or in a file react/test-app/.env: 
```
REACT_APP_AWS_REGION=eu-west-1
REACT_APP_COGNITO_USER_POOL_ID=eu-west-1_xxxxxx
REACT_APP_COGNITO_WEBCLIENT_ID=xxxxxxxxxxxxxx
```

## Content
The interesting source is ./src/App.js.

## Useful Script
### `npm start`
Runs the app in the development mode.
