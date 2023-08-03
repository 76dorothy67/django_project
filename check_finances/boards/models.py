from django.db import models
from datetime import date

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Post(models.Model):
    date = models.DateField(auto_now_add=False)
    sum = models.FloatField(max_length=30)
    category = models.ForeignKey(Category, null="none", on_delete=models.CASCADE)
