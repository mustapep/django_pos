from django.contrib.auth.models import Group
from django.shortcuts import redirect

class IsAutenticate(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if Group.objects.get(name='sales').name in request.user.groups.all() or request.user.is_superuser:
                print()
                return redirect('/items')
            else:
                return redirect('/customer_landingpage')
        return super().dispatch(self, request, *args, **kwargs)

