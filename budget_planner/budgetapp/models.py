from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    username = models.CharField(max_length=25, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'username'], name='category of username')
        ]

    def __str__(self):
        return f"{self.username}:{self.user_id}"


class Expense(models.Model):
    name = models.CharField(max_length=25, unique=True, null=False)
    amount = models.IntegerField()
    category = models.ManyToManyField(Category)
    date_now = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}:{self.user_id}"
