from __future__ import annotations
from django.db import models
from account.models import User


class UserSpace(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_space')
    users = models.ManyToManyField(User, related_name='space')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    
    
    def add_user(self, email: str, by_user: User) -> tuple[bool, str]:
        if by_user != self.owner:
            return False, "Только владелец может добавлять пользователей"
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return False, "Пользователь не найден"
        
        if self.users.filter(id=user.id).exists():
            return False, "Пользователь уже добавлен"
        
        self.users.add(user)
        return True, f"{user.nick_name} добавлен"
    
    
    def remove_user(self, user: User) -> tuple[bool, str]:
        if user == self.owner:
            return False, "Невозможно удалить владельца пространства!"
        if self.users.filter(id=user.id).exists():
            self.users.remove(user)
            return True, f"{user.nick_name} удалён"
        return False, "Пользователь не найден"
    
    
    def create_list(self, name: str) -> tuple[bool, str]:
        if not name:
            return False, "Название списка не может быть пустым"
        
        ShopList.objects.create(
            name=name,
            space=self
        )
        return True, f"Список {name} создан"


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