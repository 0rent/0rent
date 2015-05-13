# Mixin : conditions pour accès aux pages
from django.http import HttpResponseForbidden
from django.shortcuts import render


class UserCanAccessProductMixin(object):

    def check_user_product(self, user):
        product = self.get_object()
        return product.is_public or user.groups.filter(
            id=product.private_group_id).exists()

    def dispatch(self, request, *args, **kwargs):
        if not self.check_user_product(request.user):
            return render(request, 'permission_denied.html', status=401)

        return super(UserCanAccessProductMixin,
                     self).dispatch(request, *args, **kwargs)
