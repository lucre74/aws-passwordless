def do(event, context):
    event["response"]["autoConfirmUser"] = True
    event["response"]["autoVerifyEmail"] = True
    return event
