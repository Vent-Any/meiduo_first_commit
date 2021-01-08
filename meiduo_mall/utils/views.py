from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class LoginRequiredJSONMixin(LoginRequiredMixin):
    """Verify that the current user is authenticated."""
    def handle_no_permission(self):

        return JsonResponse({'code': 400, 'errmsg': '用户未登录'})