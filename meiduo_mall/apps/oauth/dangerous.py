from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
s = Serializer(secret_key='123', expires_in=3600)
data = {
    'openid':'abc123'
}
s.dumps(data)