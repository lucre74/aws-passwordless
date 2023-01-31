import random
import boto3


def do(event, context):
    # {
    #   'version': '1',
    #   'region': 'eu-west-1',
    #   'userPoolId': 'eu-west-1_xxxxxx',
    #   'userName': 'cb387499-8e10-4f1c-8c8f-xxxxxxx',
    #   'callerContext': {
    #     'awsSdkVersion': 'aws-sdk-unknown-unknown',
    #     'clientId': 'xxxxxx'
    #   },
    #   'triggerSource': 'CreateAuthChallenge_Authentication',
    #   'request': {
    #     'userAttributes': {
    #       'sub': 'cb387499-8e10-4f1c-8c8f-xxxxxx',
    #       'cognito:email_alias': 'luc@zorglub.be',
    #       'cognito:user_status': 'CONFIRMED',
    #       'email_verified': 'true',
    #       'email': 'luc@zorglub.be'
    #     },
    #     'challengeName': 'CUSTOM_CHALLENGE',
    #     'session': []
    #   },
    #   'response': {
    #     'publicChallengeParameters': None,
    #     'privateChallengeParameters': None,
    #     'challengeMetadata': None
    #   }
    # }
    session = event["request"]["session"]
    email = event["request"]["userAttributes"]["email"]
    secretcode = str(random.randrange(100000, 999999))
    if session is None or len(session) == 0:
        # Send mail with the secretCode
        sendmail(email, secretcode)
    else:
        # Get the secret code from the session...
        previouschallenge = session[len(session) - 1]
        secretcode = decode(previouschallenge["challengeMetadata"])

    event["response"]["publicChallengeParameters"] = {"email": email}
    event["response"]["privateChallengeParameters"] = {"expected": secretcode}
    event["response"]["challengeMetadata"] = code(secretcode)
    return event


def code(digits):
    return "CODE-"+digits


def decode(string):
    return string[5:]


def sendmail(emailaddress, secret):
    ses = boto3.client("ses")
    ses.send_email(
        Source="nadheo@tetram.be",
        Destination={
            "ToAddresses": [emailaddress]
        },
        Message={
            "Subject": {
                "Data": "Votre code d'authentification",
                "Charset": "UTF-8"
            },
            "Body": {
                "Html": {
                    "Charset": "UTF-8",
                    "Data": """<html><body><p>Votre code d'authentification:</p>
                           <h3>{secret}</h3>
                           <p>Recopiez-le dans l'interface d'authentification pour vous confirmer votre 
                           adresse e-mail.</body></html>"""
                    .format(secret=secret)
                },
                "Text": {
                    "Charset": "UTF-8",
                    "Data": """Votre code d'authentification est {secret}. 
                         Recopiez-le dans l'interface d'authentification pour confirmer votre adresse e-mail."""
                    .format(secret=secret)
                }
            }
        })
