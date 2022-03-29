from django.db import models

from accounts.models import UserModel


class Food(models.Model):
    food_item = models.CharField(max_length=100)
    hater_user = models.ManyToManyField(UserModel)

    def __str__(self):
        return self.food_item


class Poll(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    meal = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True, related_name='poll')
    out = models.BooleanField(null=True)
    orderer = models.BooleanField(null=True)
    note = models.TextField(null=True)

    def __str__(self):
        return self.user.username
