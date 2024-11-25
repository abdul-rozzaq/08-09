from django.db import models


class FoodType(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name


class Food(models.Model):
    food_type = models.ForeignKey(FoodType, on_delete=models.CASCADE)
    nomi = models.CharField(max_length=128)
    tarkibi = models.TextField()
    narxi = models.IntegerField()

    def __str__(self) -> str:
        return self.nomi


class Comment(models.Model):
    text = models.TextField()
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text
