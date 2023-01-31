def do(event, context):
    # {'version': '1',
    #  'region': 'eu-west-1',
    #  'userPoolId': 'eu-west-1_xxxxx',
    #  'userName': 'dc6b1bd6-4e51-4e2e-a853-xxxxxx',
    #  'callerContext':
    #   {'awsSdkVersion': 'aws-sdk-unknown-unknown',
    #    'clientId': 'xxxxxxxxx'
    #   },
    #  'triggerSource': 'DefineAuthChallenge_Authentication',
    #  'request':
    #   {'userAttributes':
    #     {'sub': 'dc6b1bd6-4e51-4e2e-a853-xxxxxxx',
    #      'cognito:email_alias': 'luc@zorglub.be',
    #      'cognito:user_status': 'CONFIRMED',
    #      'email_verified': 'true',
    #      'email': 'luc@zorglub.be'
    #     },
    #     # When no challenge has been answered, session is empty
    #     'session': []
    #     # When a challenge has been answered, session is not empty. It contains one element per try. Latest try is
    #     # the last of the array.
    #     'session': [
    #       {
    #         'challengeName': 'CUSTOM_CHALLENGE',
    #         'challengeResult': False,
    #         'challengeMetadata': 'CODE-983750'
    #       },
    #       {
    #         'challengeName': 'CUSTOM_CHALLENGE',
    #         'challengeResult': True,
    #         'challengeMetadata': 'CODE-983750'
    #       }
    #     ]
    #   },
    #  'response': {'challengeName': None, 'issueTokens': None, 'failAuthentication': None}
    # }

    # The following answer is correct when no session and when the challenge has not been answered correctly
    # The authentication will never fail (failAuthentication is always false). Can be changed (set failAuthentication
    # to true when a condition is met (e.g. number of retries reaches a given threshold)).
    event["response"]["issueTokens"] = "false"
    event["response"]["challengeName"] = "CUSTOM_CHALLENGE"
    event["response"]["failAuthentication"] = "false"
    session = event["request"]["session"]
    if session is not None and len(session) > 0 and \
            session[len(session)-1]["challengeName"] == "CUSTOM_CHALLENGE" and \
            session[len(session)-1]["challengeResult"]:
        event["response"]["issueTokens"] = "true"
    return event
