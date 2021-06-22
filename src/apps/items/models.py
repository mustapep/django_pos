from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=50)
    sub_from = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'


class Items(models.Model):
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='cat')
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    item_img = models.ImageField(upload_to='items/')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = [('can_view_items', 'Can view items'),
                       ('can_add_items', 'Can add items'),
                       ('can_update_items', 'Can update items'),
                       ('can_delete_items', 'Can delete items'),
                       ]
        db_table = 'items'
