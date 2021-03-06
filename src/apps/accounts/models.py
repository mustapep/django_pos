from django.db import models
from django.contrib.auth.models import User


class CardMember(models.Model):
    name = models.CharField(max_length=45)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'card_members'


class Member(models.Model):
    customers = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customers')
    card_member = models.ForeignKey(CardMember, on_delete=models.CASCADE, related_name='members')
    gender = models.CharField(max_length=1)
    photo = models.ImageField(upload_to='profile/')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.customers)

    class Meta:
        db_table = 'members'


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    address = models.CharField(max_length=100)
    nik_numb = models.CharField(max_length=12)
    ktp_image = models.ImageField(upload_to='ktp/')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = 'employees'
