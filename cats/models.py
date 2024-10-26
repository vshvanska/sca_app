from django.db import models


class Cat(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    years_of_experience = models.PositiveIntegerField()
    salary = models.PositiveIntegerField()

    def __str__(self):
        return self.name
