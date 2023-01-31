def do(event, context):
    # Event:
    # {
    #   'version': '1',
    #   'region': 'eu-west-1',
    #   'userPoolId': 'eu-west-1_xxxxx',
    #   'userName': '1a520a7b-ea76-4672-82d1-xxxxxx',
    #   'callerContext': {
    #     'awsSdkVersion': 'aws-sdk-unknown-unknown',
    #     'clientId': 'xxxxx'
    #   },
    #   'triggerSource': 'VerifyAuthChallengeResponse_Authentication',
    #   'request': {
    #     'userAttributes': {
    #       'sub': '1a520a7b-ea76-4672-82d1-xxxxx',
    #       'cognito:email_alias': 'luc@zorglub.be',
    #       'cognito:user_status': 'CONFIRMED',
    #       'email_verified': 'true',
    #       'email': 'luc@zorglub.be'
    #     },
    #     'privateChallengeParameters': {
    #       'expected': '902094'
    #     },
    #     'challengeAnswer': '902094'
    #   },
    #   'response': {
    #     'answerCorrect': None
    #   }
    # }
    event["response"]["answerCorrect"] = \
        event["request"]["challengeAnswer"] == event["request"]["privateChallengeParameters"]["expected"]
    return event
