def do(event, context):
    # Event:
    # {
    #   'version': '1',
    #   'region': 'eu-west-1',
    #   'userPoolId': 'eu-west-1_k0qrUCrpz',
    #   'userName': '1a520a7b-ea76-4672-82d1-9514a7d1d0dc',
    #   'callerContext': {
    #     'awsSdkVersion': 'aws-sdk-unknown-unknown',
    #     'clientId': '23asg5c3oraje832ir678gtbnu'
    #   },
    #   'triggerSource': 'VerifyAuthChallengeResponse_Authentication',
    #   'request': {
    #     'userAttributes': {
    #       'sub': '1a520a7b-ea76-4672-82d1-9514a7d1d0dc',
    #       'cognito:email_alias': 'luc@lejoly.be',
    #       'cognito:user_status': 'CONFIRMED',
    #       'email_verified': 'true',
    #       'email': 'luc@lejoly.be'
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
