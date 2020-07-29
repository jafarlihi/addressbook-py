import jwt


def parse_token_user_id(func):
    def wrapper(*args, **kwargs):
        authorization = args[1].headers.get('Authorization')
        token = authorization.split()[1]
        tokenDecoded = jwt.decode(token, verify=False)
        return func(*args, user_id=tokenDecoded["user_id"], **kwargs)
    return wrapper
