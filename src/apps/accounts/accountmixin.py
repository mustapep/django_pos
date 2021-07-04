from django.contrib.auth.models import Group
from django.shortcuts import redirect


class IsAutenticated:

    def check_auth(self, request):

        if request.user.is_authenticated:
            if Group.objects.get(name='sales') in request.user.groups.all():
                return redirect('/transactions')
            elif Group.objects.get(name='admin') in request.user.groups.all():
                return redirect('/items')
            else:
                return redirect('/customer_landingpage')

    def test(self):
        print('Ini Methodnya class is_auth')
