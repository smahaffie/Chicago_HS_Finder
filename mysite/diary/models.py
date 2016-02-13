from django.db import models

# Create your models here.

class Food(models.Model):
    name = models.CharField(max_length=64)
    calories = models.IntegerField()

    def __repr__(self):
        return 'Food({}, {})'.format(self.name, self.calories)