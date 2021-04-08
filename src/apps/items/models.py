from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=50)
    sub_from = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='sub')
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class Items(models.Model):
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='cat')
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    item_img = models.ImageField(upload_to='items/', blank=True, null=True)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True, null=True)

    def __str__(self):
        return self.name
