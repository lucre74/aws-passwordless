import random
import boto3
from string import Template

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
    language = event["request"]["userAttributes"]["locale"]
    poolid = event["userPoolId"]
    secretcode = str(random.randrange(100000, 999999))
    if session is None or len(session) == 0:
        # Send mail with the secretCode
        sendmail(email, secretcode, language, poolid)
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


def sendmail(emailaddress, secret, language, poolid):
    ses = boto3.client("ses")
    ssm = boto3.client("ssm")
    fromAddress = getParameter(ssm, f"be.tetram.cognito.passwordfree.{poolid}.mailFromAddress")
    title = getTitle(ssm, poolid, language)
    body = getBody(ssm, poolid, language)
    bodyhtml = getBodyHtml(ssm, poolid, language)

    ses.send_email(
        Source=fromAddress,
        Destination={
            "ToAddresses": [emailaddress]
        },
        Message={
            "Subject": {
                "Data": Template(title).substitute(code=secret),
                "Charset": "UTF-8"
            },
            "Body": {
                "Html": {
                    "Charset": "UTF-8",
                    "Data": Template(bodyhtml).substitute(code=secret)
                },
                "Text": {
                    "Charset": "UTF-8",
                    "Data": Template(body).substitute(code=secret)
                }
            }
        })


def getLanguageDependentString(ssm, template, poolid, language, default):
    res = getParameter(ssm, Template(template).substitute(poolid=poolid, language=language))
    if (res is None):
        res = getParameter(ssm, Template(template).substitute(poolid=poolid, language="en"))
    if (res is None):
        res = default
    return res


def getTitle(ssm, poolid, language):
    return getLanguageDependentString(ssm, "be.tetram.cognito.passwordfree.$poolid.$language.mailTitle", poolid,
                                      language, "Your confirmation code")


def getBody(ssm, poolid, language):
    return getLanguageDependentString(ssm, "be.tetram.cognito.passwordfree.$poolid.$language.mailBody", poolid,
                                      language, "Your confirmation code is $code.")


def getBodyHtml(ssm, poolid, language):
    return getLanguageDependentString(ssm, "be.tetram.cognito.passwordfree.$poolid.$language.mailBodyHtml", poolid,
                                      language,
                                      "<html><body><p>Your confirmation code:</p><h3>$code</h3></body></html>")


def getParameter(ssm, key):
    try:
        response = ssm.get_parameter(Name=key)
        return response["Parameter"]["Value"];
    except Exception as e:
        print(e)
        return None
