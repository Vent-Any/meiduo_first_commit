from rest_framework_jwt.serializers import JSONWebTokenSerializer
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class AdminJSONWebTokenSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }
        if all(credentials.values()):
            user = authenticate(**credentials)
            if user:
                # if not user.is_active:
                #     msg = _('User account is disabled.')
                #     raise serializers.ValidationError(msg)
                # is_staff = False/0
                # if not False = if True
                if not user.is_staff:
                    msg = _('普通用户不可以!!!')
                    raise serializers.ValidationError(msg)
                payload = jwt_payload_handler(user)
                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


from rest_framework_jwt.views import JSONWebTokenAPIView


class AdminJSONWebTokenAPIView(JSONWebTokenAPIView):
    # 重写属性
    serializer_class = AdminJSONWebTokenSerializer


# 接收token备用
admin_obtain_token = AdminJSONWebTokenAPIView.as_view()
