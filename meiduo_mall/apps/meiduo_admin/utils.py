def jwt_response_playload_handler(token, user=None, request=None):
    return {
            'token': token,
            'username':user.username,
            'user_id':user.id
            }