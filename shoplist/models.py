from django.db import models
from account.models import User


class UserSpace(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='space')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class ShopList(models.Model):
    space = models.ForeignKey(UserSpace, on_delete=models.CASCADE, related_name='lists')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name} ({self.space.name})'
    
    
class Item(models.Model):
    shopping_list = models.ForeignKey(ShopList, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=250)
    done = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.name} {self.done}'